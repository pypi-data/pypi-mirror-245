import jax.numpy as jnp
from jax import config, jit, vmap
from functools import partial
import time
from .__init__ import um, cm
from .wave_optics import ScalarLight
from .vectorized_optics import VectorizedLight, vectorized_CZT_for_high_NA
from .toolbox import build_LCD_cell, rotate_mask

# Comment this line if float32 is enough precision for you. 
config.update("jax_enable_x64", True)

""" Contains optical elements:

    (1) Scalar light devices:
        - phase_scalar_SLM
        - SLM
    
    (2) Jones matrices:
        - jones_LP
        - jones_general_retarder
        - jones_sSLM
        - jones_LCD
    
    (3) Polarization-based devices:
        - sSLM
        - LCD
        - linear_polarizer
        - BS
        - high_NA_objective_lens
            + _high_NA_objective_lens_
    (3.1) Propagation methods through objective lenses:
        - VCZT_objective_lens
            + build_high_NA_VCZT_grid
    
    (4) General elements:
        - lens
        - circular_mask
        - triangular_mask
        - rectangular_mask
        - annular_aperture
        - forked_grating
    
    (5) Pre-built optical set-ups:
        - building_block
        - xl_setup
        - vSTED
        - sharp_focus
        - general_setup
"""

# ------------------------------------------------------------------------------------------------

""" (1) Scalar light devices: """

def phase_scalar_SLM(phase):
    """
    Phase for ScalarLight SLM. 
    
    Parameters:
        phase (float): Global phase (in radians).
   
    Returns phase (jnp.array).
    """
    return jnp.exp(1j * phase)

def SLM(input_field, phase_array, shape):
    """
    SLM (spatial light modulator) for ScalarLight: applies a phase mask [pixel-wise].
    
    Parameters:
        input_field (ScalarLight): Light to be modulated.
        phase_array (jnp.array): Phase to be applied (in radians). 
    
    Returns ScalarLight after applying the transformation.
    """
    slm = jnp.fromfunction(lambda i, j: phase_scalar_SLM(phase_array[i, j]),
                           (shape, shape), dtype=int)
    light_out = ScalarLight(input_field.x, input_field.y, input_field.wavelength)
    light_out.field = input_field.field * slm  # Multiplies element-wise
    
    return light_out, slm

# ------------------------------------------------------------------------------------------------

""" (2) Jones matrices: """

@jit
def jones_LP(alpha):
    """
    Define the Jones matrix of a Linear polarizer.

    Parameters:
        alpha (float): Transmission angle w.r.t. horizontal (in radians).
        
    Returns the Jones matrix (jnp.array).
    """
    return jnp.array([[jnp.cos(alpha) ** 2, jnp.cos(alpha) * jnp.sin(alpha)],
                      [jnp.cos(alpha) * jnp.sin(alpha), jnp.sin(alpha) ** 2]])

@jit
def jones_general_retarder(eta, theta, delta):
    """
    Define the Jones matrix of a general retarder.

    Parameters:
        eta (float): Phase difference between Ex and Ey (in radians).
        theta (float): Angle of the fast axis w.r.t. horizontal (in radians).
        delta (float): Ellipticity of the eigenvalues of the retarder.
        
    Returns the Jones matrix (jnp.array).
    """
    return jnp.array([[jnp.exp(-(eta / 2) * 1j) * jnp.cos(theta) ** 2 + jnp.exp((eta / 2) * 1j) * jnp.sin(theta) ** 2,
                      (jnp.exp(-(eta / 2) * 1j) - jnp.exp((eta / 2) * 1j)) * jnp.exp(-delta * 1j) * jnp.sin(
                          theta) * jnp.cos(theta)],
                     [(jnp.exp(-(eta / 2) * 1j) - jnp.exp((eta / 2) * 1j)) * jnp.exp(delta * 1j) * jnp.sin(
                         theta) * jnp.cos(theta),
                      jnp.exp(-(eta / 2) * 1j) * jnp.sin(theta) ** 2 + jnp.exp((eta / 2) * 1j) * jnp.cos(theta) ** 2]])

@jit
def jones_sSLM(alpha, phi):
    """
    Define the Jones matrix of the sSLM.

    Parameters:
        alpha (float): Phase mask for Ex (in radians).
        phi (float): Phase mask for Ey (in radians).
        
    Returns the Jones matrix (jnp.array).
    """
    return jnp.array([[jnp.exp(1j * alpha), 0], [0, jnp.exp(1j * phi)]])

@jit
def jones_LCD(eta, theta):
    """
    Define the Jones matrix of LCD (liquid crystal display).

    Parameters:
        eta (float): Phase difference between Ex and Ey (in radians).
        theta (float): Angle of the fast axis w.r.t. horizontal (in radians).

    Returns the Jones matrix (jnp.array).
    """
    return jones_general_retarder(eta, theta, delta=0)

# ------------------------------------------------------------------------------------------------

""" (3) Polarization-based devices: """

def sSLM(input_field, alpha_array=None, phi_array=None):
    """
    Define super-Spatial Light Modulator (sSLM): adds phase mask [pixel-wise] to Ex and Ey independently. 
    
    Illustrative scheme:
    (Ex, Ey) --> PBS --> Ex --> SLM(alpha) --> Ex' --> PBS --> (Ex', Ey')
                  |                                     ^ 
                  v                                     |
                  Ey ---------> SLM(phi) ----> Ey' -----/

    Parameters:
        input_field (VectorizedLight): Light to be modulated.
        alpha_array (jnp.array): Phase mask to be applied to Ex (in radians).
        phi_array (jnp.array): Phase mask to be applied to Ey (in radians).
        
    Returns VectorizedLight after applying the transformation.
    """
    # Consider Ex and Ey:
    input_field_xy = jnp.moveaxis(jnp.stack([input_field.Ex, input_field.Ey]), [0, 1, 2], [2, 0, 1])
    shape = jnp.shape(input_field_xy)[1]

    # Compute phase for each 
    sslm = jnp.fromfunction(lambda i, j: jones_sSLM(alpha_array[i, j], phi_array[i, j]),
                            (shape, shape), dtype=int)
    
    sslm = jnp.reshape(sslm, (shape ** 2, 2, 2))
    field = jnp.reshape(input_field_xy, (shape ** 2, 2, 1))
    field_out = sslm @ field
    field_out = field_out.reshape(shape, shape, 2)
    
    light_out = VectorizedLight(input_field.x, input_field.y, input_field.wavelength)
    light_out.Ex = field_out[:, :, 0]
    light_out.Ey = field_out[:, :, 1]
    # Maintain the input Ez.
    light_out.Ez = input_field.Ez
    
    return light_out

def LCD(input_field, eta, theta):
    """
    Liquid Crystal Device for VectorizedLight: builds any linear wave-plate.
    
    Parameters:
        input_field (VectorizedLight): Light to be modulated.
        eta (float): Retardance between Ex and Ey (in radians).
        theta (float): = Tilt of the fast axis w.r.t. the horizontal (in radians).
    
    Examples: tuning "eta" and "theta" one can achieve 
        HWP at 0º: eta = pi, theta = 0,
        HWP at 90º: eta = pi, theta = pi/2,
        QWP at 0º: eta = pi/2, theta = 0,
        QWP at 90º: eta = pi/2, theta = pi/2, etc. 
    
    Returns VectorizedLight after applying the transformation.
    """
    # Consider Ex and Ey:
    input_field_xy = jnp.moveaxis(jnp.stack([input_field.Ex, input_field.Ey]), [0, 1, 2], [2, 0, 1])
    shape = jnp.shape(input_field_xy)[1]
    
    # Define the constant eta and theta cell
    eta_array, theta_array = build_LCD_cell(eta, theta, shape)
    
    # Compute phase for each 
    lcd = jnp.fromfunction(lambda i, j: jones_LCD(eta_array[i, j], theta_array[i, j]),
                           (shape, shape), dtype=int)

    lcd = jnp.reshape(lcd, (shape ** 2, 2, 2))
    field = jnp.reshape(input_field_xy, (shape ** 2, 2, 1))
    field_out = lcd @ field
    field_out = field_out.reshape(shape, shape, 2)
    
    light_out = VectorizedLight(input_field.x, input_field.y, input_field.wavelength)
    light_out.Ex = field_out[:, :, 0]
    light_out.Ey = field_out[:, :, 1]
    # Maintain the input Ez.
    light_out.Ez = input_field.Ez    
    
    return light_out

def linear_polarizer(input_field, alpha):
    """
    Linear polarizer VectorizedLight.
    
    Parameters:
        input_field (VectorizedLight): Light to be modulated.
        alpha (jnp.array): Transmission angle w.r.t. horizontal (in radians).
    
    Returns VectorizedLight after applying the transformation.
    """
    # General function for linear polarizer.
    # Transmission angle alpha[i,j] from the horizontal.
    input_field_xy = jnp.moveaxis(jnp.stack([input_field.Ex, input_field.Ey]), [0, 1, 2], [2, 0, 1])
    shape = jnp.shape(input_field_xy)[1]

    E_reshape = jnp.reshape(input_field_xy, (shape ** 2, 2, 1))
    LP = jnp.fromfunction(lambda i, j: jones_LP(alpha[i, j]), (shape, shape), dtype=jnp.float64)
    LP_reshape = jnp.reshape(LP, (shape ** 2, 2, 2))
    E_out = LP_reshape @ E_reshape
    E_out = E_out.reshape(shape, shape, 2)
    
    light_out = VectorizedLight(input_field.x, input_field.y, input_field.wavelength)
    light_out.Ex = E_out[:, :, 0]
    light_out.Ey = E_out[:, :, 1]
    
    return light_out

def BS(a1, a2, R, T, phase):
    """
    Lossless two-mode beam splitter of reflectance R, and transmittance T. 
    
    If: 
        phase = 0 -> light in port b1
        phase = pi -> light in port b2
        phase = pi/2 -> light in ports b1, b2
    
    Scheme:
                 a1
                 |
                 v        
         a2 --> [\] --> b2 = a2_t + a1_r
                 | 
                 v
                 b1 = a1_t + a2_r
   
    ------------------------------------------------------------ 
    
    BS = [[     √T          e^(i*phase)*√R],
          [-e^(-i*phase)√R        √T      ]]
    
    b1 = [[√T * Ex_a1 + √R * e^(i*phase) * Ex_a2],
          [√T * Ey_a1 + √R * e^(i*phase) * Ey_a2]] 
               
    b2 = [[- √R * e^(-i*phase) * Ex_a1 + √T * Ex_a2],
          [- √R * e^(-i*phase) * Ey_a1 + √T * Ey_a2]]          
    
    ------------------------------------------------------------          
    
    Parameters: 
        a1 (VectorizedLight): electric field in port a1
        a2 (VectorizedLight): electric field in port a2
        R (float): Reflectance (between 0 and 1)
        T (float): Transmittance (between 0 and 1)
        phase (float): phase shift to apply.
    
    Returns b1 and b2 (VectorizedLight). 
    """
    # Define light at ports b1 and b2.
    b1 = VectorizedLight(a1.x, a1.y, a1.wavelength)
    b2 = VectorizedLight(a1.x, a1.y, a1.wavelength)
    
    b1.Ex = (jnp.sqrt(T) * a1.Ex) + (jnp.sqrt(R) * jnp.exp(1j*phase) * a2.Ex) 
    b1.Ey = (jnp.sqrt(T) * a1.Ey) + (jnp.sqrt(R) * jnp.exp(1j*phase) * a2.Ey)
    
    b2.Ex = (- jnp.sqrt(R) * jnp.exp(- 1j*phase) * a1.Ex) + (jnp.sqrt(T) * a2.Ex)
    b2.Ey = (- jnp.sqrt(R) * jnp.exp(- 1j*phase) * a1.Ey) + (jnp.sqrt(T) * a2.Ey) 
    
    return b1, b2


def high_NA_objective_lens(input_field, radius, f):
    """
    High NA objective lens for VectorizedLight - to be used with [VCZT_objective_lens].
    [Ref1: Opt. Comm. 283 (2010), 4859 - 4865].
    [Ref2: Hu, Y., et al. Light Sci Appl 9, 119 (2020)].
        
    Parameters:
        input_field (VectorizedLight): Light to be focused.
        radius (float): Radius of the objective lens (in microns).
        f (float): Focal length of the objective lens (in microns).
        
    Returns the field directly after applying the lens.
    """ 
    sin_theta_max = radius / jnp.sqrt(radius ** 2 + f ** 2)
    
    # Coordinates:
    X, Y = input_field.X, input_field.Y
    r = jnp.sqrt(X ** 2 + Y ** 2)
    phi = jnp.arctan2(Y, X)
    theta = r / f
    
    # Set the value of Ez:
    # r_field = jnp.sqrt(X** 2 + Y** 2 + z ** 2)
    Ez = jnp.array(input_field.Ex * X/ r + input_field.Ey * Y / r) 
    
    # Spatial frequencies
    # Eq. (6) - Opt. Comm. 283 (2010), 4859 - 4865.
    u = X / radius
    v = Y / radius

    # G(u,v) - Eq. (9) - Opt. Comm. 283 (2010), 4859 - 4865.
    pupil_mask = jnp.where((X ** 2 + Y ** 2) / radius ** 2 < 1, 1, 0)
    G = jnp.real(pupil_mask * (1 / jnp.sqrt(jnp.abs(1 - (u ** 2 + v ** 2) * sin_theta_max ** 2))))
    incoming_light = jnp.stack([input_field.Ex, input_field.Ey, Ez], axis=-1)
    
    # jit-compute Equation (7) from [Ref 2].
    out_field = _high_NA_objective_lens_(incoming_light, theta, phi, G)
    
    return out_field, sin_theta_max

@jit
def _high_NA_objective_lens_(incoming_light, theta, phi, G):
    """[From high_NA_objective_lens]: JIT function that applies the lens."""
    Ex = incoming_light[:, :, 0]
    Ey = incoming_light[:, :, 1]
    Ez = incoming_light[:, :, 2]
    
    # For matrix elements:
    c_theta = jnp.cos(theta)
    s_theta = jnp.sin(theta)
    c_phi = jnp.cos(phi)
    s_phi = jnp.sin(phi)
    
    # Apodization factor
    apod = jnp.sqrt(jnp.abs(c_theta))
    
    # Eq. (1) - Opt. Comm. 283 (2010), 4859 - 4865.
    # E0 = apod * RL * Ei 
    RL00 = c_theta * c_phi**2 + s_phi**2
    RL01 = c_theta * c_phi * s_phi - s_phi * c_phi
    RL02 = - c_phi * s_theta
    RL10 = s_phi * c_theta * c_phi - c_phi * s_phi
    RL11 = c_theta * s_phi**2 + c_phi**2
    RL12 = - s_phi * s_theta
    RL20 = s_theta * c_phi 
    RL21 = s_theta * s_phi
    RL22 = c_theta
    
    # Eq. (1) - Opt. Comm. 283 (2010), 4859 - 4865.
    E0_x = RL00 * Ex + RL01 * Ey + RL02 * Ez
    E0_y = RL10 * Ex + RL11 * Ey + RL12 * Ez
    E0_z = RL20 * Ex + RL21 * Ey + RL22 * Ez

    Ef_x = apod * G * E0_x
    Ef_y = apod * G * E0_y
    Ef_z = apod * G * E0_z

    # Stack the field in a (3, N, N).
    
    return jnp.stack([Ef_x, Ef_y, Ef_z], axis=0)

# ------------------------------------------------------------------------------------------------

""" (3.1) Propagation methods through objective lenses """

def VCZT_objective_lens(input_field, r, f, xout, yout):
    """
    Vectorial Chirp z-transform algorithm for high NA objective lens.
    [Ref 1] Hu, Y., et al. Light Sci Appl 9, 119 (2020).
    [Ref 2] Opt. Comm. 283 (2010), 4859 - 4865.
    
    Parameters:
        input_field (VectorizedLight): Light to be focused.
        r (float): Radius of the objective lens (in microns).
        f (float): Focal length of the objective lens (in microns).
        xout, yout (jnp.arrays): Desired output (high resolution) arrays in the focal plane.

    Returns the VectorizedLight in the focal plane sampled in the new arrays (xout, yout).
    """
    tic = time.perf_counter()
    
    # Apply high NA objective lens - returns (3, N, N) electric field. 
    field_in_lens, sin_theta_max = high_NA_objective_lens(input_field, r, f)

    # Define main set of parameters
    nx, ny, Dm, fy_1, fy_2, fx_1, fx_2 = build_high_NA_VCZT_grid(f, r, input_field.wavelength, input_field.x, xout, yout)

    # Apply VCZT [Ref 1] to propagate through the focus.
    # Pass to jit the input field in shape (3, N, N).
    U = vectorized_CZT_for_high_NA(field_in_lens, nx, ny, Dm, fy_1, fy_2, fx_1, fx_2)

    # Eq. (8) in [Ref 2]
    cte = -(1j * sin_theta_max**2 / (f * input_field.wavelength))
    
    field_at_z = cte * U 
    
    # Define the output light:
    light_out = VectorizedLight(xout, yout, input_field.wavelength)
    light_out.Ex = field_at_z[0, :, :]
    light_out.Ey = field_at_z[1, :, :]
    light_out.Ez = field_at_z[2, :, :]
    print("Time taken to perform one VCZT propagation through objective lens (in seconds):", time.perf_counter() - tic)
    
    return light_out

def build_high_NA_VCZT_grid(f, r, wavelength, xin, xout, yout):
    """
    [For VCZT_objective_lens]: Defines the resolution / sampling of initial and output planes.
    
    Parameters:
        f (float): Focal length of the objective lens (in microns).
        r (float): Radius of the objective lens (in microns).
        wavelength (float): Wavelength of the light beam (in microns).
        xin (jnp.array): Array with the x-positions of the input plane.
        xout (jnp.array): Array with the x-positions of the output plane.
        yout (jnp.array): Array with the y-positions of the output plane.
    
    Returns the set of parameters: nx, ny, Xout, Yout, dx, dy, delta_out, Dm, fy_1, fy_2, fx_1 and fx_2.
    """
    # Resolution of the output plane:
    nx = len(xout)
    ny = len(yout)
    
    # Resolution of the input plane:
    Din = len(xin)
    
    # For Bluestein method implementation: 
    # Dimension of the imaging plane
    Dm = f * wavelength * (Din - 1)/(2 * r)
    
    # (1) for FFT in Y-dimension:
    fy_1 = yout[0] + Dm / 2
    fy_2 = yout[-1] + Dm / 2
    # (1) for FFT in X-dimension:
    fx_1 = xout[0] + Dm / 2
    fx_2 = xout[-1] + Dm / 2
    
    return nx, ny, Dm, fy_1, fy_2, fx_1, fx_2

# ------------------------------------------------------------------------------------------------

""" (4) General elements: """

def lens(input_field, radius, focal):
    """
    Define a transparent lens of variable size (in microns) for ScalarLight / VectorizedLight.

    Parameters:
        radius (float, focal): Radius of the lens (in microns).
        focal (float, float): Focal length of the lens (in microns).

    Returns ScalarLight (or VectorizedLight) after applying the lens and the lens mask.
    """
    fx, fy = focal
    pupil = circular_mask(input_field.X, input_field.Y, radius)
    lens_ = pupil * jnp.exp(-1j * input_field.k * (input_field.X**2 / (2*fx) + input_field.Y**2 / (2*fy)))
    
    if input_field.info == 'Wave optics light' or input_field.info =='Wave optics light source':
        output = ScalarLight(input_field.x, input_field.y, input_field.wavelength)
        output.field = input_field.field * lens_
        
    elif input_field.info == 'Vectorized light' or input_field.info =='Vectorized light source':
        output = VectorizedLight(input_field.x, input_field.y, input_field.wavelength)
        output.Ex = input_field.Ex * lens_
        output.Ey = input_field.Ey * lens_
    else:
        raise ValueError(f"Invalid input. Please use ScalarLight or VectorizedLight object.")
   
    return output, lens_

def circular_mask(X, Y, r):
    """
    Define a circular mask of variable size (in microns).
    
    Parameters:
        X (float, float): X array.
        Y (float, float): Y array.
        r (float, float): Radius of the circle (in microns).
    
    Returns the circular mask (jnp.array)
    """
    rx, ry = r
    pupil = jnp.where((X**2 / rx**2 + Y**2 / ry**2) < 1, 1, 0)
    
    return pupil

def triangular_mask(X, Y, r, angle, m, height):
    """
    Define a triangular mask of variable size (in microns); equation to generate the triangle: y = -m (x - x0) + y0.
    
    Parameters:
        X (float, float): x array.
        Y (float, float): y array.
        center (float, float): Coordinates of the top corner of the triangle (in microns).
        angle (float): Rotation of the triangle (in degrees).
        m (float): Slope of the edges.
        height (float): Distance between the top corner and the basis (in microns).
    
    Returns the triangular mask (jnp.array).
    
    >> Diffractio-adapted function (https://pypi.org/project/diffractio/) << 
    """
    x0, y0 = r
    angle = angle * (jnp.pi/180)
    Xrot, Yrot = rotate_mask(X, Y, angle, r)
    Y = -m * jnp.abs(Xrot - x0) + y0
    return jnp.where((Yrot < Y) & (Yrot > y0 - height), 1, 0)

def rectangular_mask(X, Y, center, width, height, angle):
    """
    Apply a square mask of variable size. Can generate rectangles, squares and rotate them to create diamond shapes.
    
    Parameters:
        X (float, float): X array.
        Y (float, float): Y array.
        center (float, float): Coordinates of the center (in microns).
        width (float): Width of the rectangle (in microns).
        height (float): Height of the rectangle (in microns).
        angle (float): Angle of rotation of the rectangle (in degrees).
    
    Returns the rectangular mask (jnp.array). 
    """
    x0, y0 = center
    angle = angle * (jnp.pi/180)
    Xrot, Yrot = rotate_mask(X, Y, angle, center)
    return jnp.where((Xrot < (width/2)) & (Xrot > (-width/2)) & (Yrot < (height/2)) & (Yrot > (-height/2)), 1, 0)

def annular_aperture(di, do, X, Y):
    """
    Define annular aperture of variable size (in microns).
    
    Parameters:
        di (float): Radius of the inner circle (in microns).
        do (float): Radius of the outer circle (in microns).
        X (float, float): X array.
        Y (float, float): Y array.
    
    Returns the circular mask (jnp.array).
    """
    di = di/2
    do = do/2
    stop = jnp.where(((X**2 + Y**2) / di**2) < 1, 0, 1)
    ring = jnp.where(((X**2 + Y**2) / do**2) < 1, 1, 0)
    return stop*ring

def forked_grating(X, Y, center, angle, period, l, kind=''):
    """
    Defines a forked grating mask of variable size (in microns).
    
    Parameters:
        X (float, float): X array.
        Y (float, float): Y array.
        center (float, float): Coordinates of the center (in microns).
        angle (float): Angle of rotation of the grating (in degrees).
        period (float): Period of the grating.
        l (int): Number of lines inside the wrap.
        alpha (int): 
        kind (str): Set to 'Amplitude' or 'Phase'
    
    Returns the forked grating mask (jnp.array). 
    
    >> Diffractio-adapted function (https://pypi.org/project/diffractio/) <<
    """
    x0, y0 = center
    angle = angle * (jnp.pi/180)
    Xrot, Yrot = rotate_mask(X, Y, angle, center)

    theta = jnp.arctan2(Xrot, Yrot)
    alpha = 1 # Scaling factor 
    
    forked_grating = jnp.angle(jnp.exp(1j * alpha * jnp.cos(l * theta - 2 * jnp.pi / period * (Xrot))))

    forked_grating_phase = jnp.where(forked_grating < 0, 0, 1) 

    if kind == 'Amplitude':
        return forked_grating_phase 
    elif kind == 'Phase':
        return jnp.exp(1j * jnp.pi * forked_grating_phase)

# ------------------------------------------------------------------------------------------------

""" (5) Pre-built optical set-ups: """

def building_block(input_light, alpha, phi, z, eta, theta):
    """
    Basic building block for general setup construction. 
    
    Scheme:
    Light in --> sSLM (alpha, phi) -- VRS(z) -- LCD (eta, theta) --> Light out
    
    Parameters:
        input_light (VectorizedLight): Input light to the block (can be light source or light inside the system).
        alpha, phi (jnp.array): sSLM phase masks.
        z (jnp.array): Distance to propagate between sSLM and LCD. 
        eta, theta (jnp.array): Global retardance and tilt of LCD.
    
    Returns output light (VectorizedLight) from the block.
    """
    # Apply sSLM (alpha - Ex-, phi - Ey-)
    l_modulated = sSLM(input_light, alpha, phi)
    # Propagate (z)
    l_propagated, _ = l_modulated.VRS_propagation(z)
    # Apply LCD:
    return LCD(l_propagated, eta, theta)

def xl_setup(ls1, ls2, parameters, fixed_params):
    """
    Optical table with a more general set-up. Building blocks are [ls, sSLM, LCD], joint by BS. 
    
    Scheme:
    [See Fig. 7a in our paper: https://doi.org/10.48550/arXiv.2310.08408].
    
    Parameters:
        ls1, ls2, (VectorizedLight): Light sources of the same type (need for interference).
        parameters (list): Parameters to pass to the optimizer for sSLM, LCD and VRS.
        parameters[0 -> 4] = alpha, phi, z, eta, theta, for 1st block.
        parameters[5 -> 9] = alpha, phi, z, eta, theta, for 2nd block.
        parameters[10 -> 14] = alpha, phi, z, eta, theta, for 3rd block.
        parameters[15 -> 19] = alpha, phi, z, eta, theta, for 4th block.
        parameters[20 -> 22] = Distance to beam splitters.
        fixed_params (jnp.array): Parameters to maintain fixed during optimization [r, f]; that is radius and focal of the objective lens.
  
    Parameters in the optimizer are from (0,1). Conversion factor here are:
    
        1. Convert (0,1) to distance in cm -> Conversion factor for (offset, 100)*cm = (offset/100, 1).
        2. Convert (0,1) to phase (in radians) -> Conversion factor (-pi, pi) + pi = (0, 2pi) = (0, 1). 
    
    + From get_VRS_minimum_z(), estimate the 'offset'. 
  
    Returns intensity (jnp.array) in the focal plane and fields at stop ends.
    """
    offset = 8.9 
    
    # Apply building blocks:
    
    # Wavelength 1:
    light_path_a, _ = (building_block(ls1, parameters[0]* 2*jnp.pi - jnp.pi, parameters[1]* 2*jnp.pi - jnp.pi, (jnp.abs(parameters[2]) * 100 + offset)*cm, parameters[3]* 2*jnp.pi - jnp.pi, parameters[4]* 2*jnp.pi - jnp.pi)).VRS_propagation((jnp.abs(parameters[20]) * 100 + offset)*cm)
    light_path_b, _ = (building_block(ls1, parameters[5]* 2*jnp.pi - jnp.pi, parameters[6]* 2*jnp.pi - jnp.pi, (jnp.abs(parameters[7]) * 100 + offset)*cm, parameters[8]* 2*jnp.pi - jnp.pi, parameters[9]* 2*jnp.pi - jnp.pi)).VRS_propagation((jnp.abs(parameters[21]) * 100 + offset)*cm)
        # Join the building blocks of equal wavelength with BS: 
    ab_reflected, ab_transmitted = BS(light_path_b, light_path_a, 0.5, 0.5, jnp.pi)
    
    # Wavelength 2
    light_path_c, _ = (building_block(ls2, parameters[10]* 2*jnp.pi - jnp.pi, parameters[11]* 2*jnp.pi - jnp.pi, (jnp.abs(parameters[12]) * 100 + offset)*cm, parameters[13]* 2*jnp.pi - jnp.pi, parameters[14]* 2*jnp.pi - jnp.pi)).VRS_propagation((jnp.abs(parameters[22]) * 100 + offset)*cm)
    light_path_d, _ = (building_block(ls2, parameters[15]* 2*jnp.pi - jnp.pi, parameters[16]* 2*jnp.pi - jnp.pi, (jnp.abs(parameters[17]) * 100 + offset)*cm, parameters[18]* 2*jnp.pi - jnp.pi, parameters[19]* 2*jnp.pi - jnp.pi)).VRS_propagation((jnp.abs(parameters[23]) * 100 + offset)*cm)
        # Join the building blocks of equal wavelength with BS: 
    cd_reflected, cd_transmitted = BS(light_path_d, light_path_c, 0.5, 0.5, jnp.pi)
    
    # Propagate to focal plane and extract the intensity
    ls1_f = VCZT_objective_lens(ab_reflected, r=fixed_params[0], f=fixed_params[1], xout=fixed_params[2], yout=fixed_params[3])
    ls2_f = VCZT_objective_lens(cd_transmitted, r=fixed_params[0], f=fixed_params[1], xout=fixed_params[2], yout=fixed_params[3])
    
    # TOTAL (3D) intensity
    i_ls1 = jnp.abs(ls1_f.Ex)**2 + jnp.abs(ls1_f.Ey)**2 + jnp.abs(ls1_f.Ez)**2
    i_ls2 = jnp.abs(ls2_f.Ex)**2 + jnp.abs(ls2_f.Ey)**2 + jnp.abs(ls2_f.Ez)**2
    
    # Resulting STED function computed for 3D:
    beta = 1 # Efficiency in the depletion
    
    i_eff = i_ls2 * (1 - beta * (1- jnp.exp(-(i_ls1/i_ls2))))

    return i_eff, ls1_f, ls2_f
    
def vSTED(excitation_beam, depletion_beam, parameters, fixed_params):
    """
    Vectorial-based STED. 
    [Ref] D. Wildanger, E. Rittweger, L. Kastrup, and S. W. Hell, Opt. Express 16, 9614-9621 (2008).
    
    Scheme: 
    STED beam ---> Modulate: sSLM (phase mask) --> VRS(z) --> High NA lens 
    Excitation beam ----------------------------------------> High NA lens 
              
    Parameters:
        excitation_beam (object): input field for the excitation.
        depletion_beam (object): input field for the depletion.
        parameters (jnp.array): parameters to pass to the optimizer [phase 1] for sSLM.
        fixed_params (jnp.array): parameters to maintain fixed during optimization [r, f, xout and yout]; that is radius and focal length of the objective lens.
           
    Returns:
        i_eff (jnp.array) effective PSF of the system, 
        i_ex (jnp.array) excitation intensity in the focal plane,
        i_dep (jnp.array) depletion intensity in the focal plane,
        ex_f (object) excitation beam in the focal plane,
        dep_f (object) depletion beam in the focal plane.
        
    Parameters in the optimizer are from (0,1). Conversion factor here are: 
        
        Convert (0,1) to phase (in radians) -> Conversion factor (-pi, pi) + pi = (0, 2pi) = (0, 1). 
    """
    # Estimate the offset via get_VRS_minimum().
    offset = 24000 #microns
    
    # Apply phase mask to depletion beam. We use only the SLM in sSLM corresponding to the input polarization state. The other is set to zero.
    dep_modulated = sSLM(depletion_beam, parameters[0]* 2 * jnp.pi - jnp.pi, jnp.zeros((2048, 2048)))
    
    # Propagate:
    dep_propagated, _ = dep_modulated.VRS_propagation(z=offset)
    
    # Propagate to focal plane and extract the intensity
    ex_f = VCZT_objective_lens(excitation_beam, r=fixed_params[0], f=fixed_params[1], xout=fixed_params[2], yout=fixed_params[3])
    dep_f = VCZT_objective_lens(dep_propagated, r=fixed_params[0], f=fixed_params[1], xout=fixed_params[2], yout=fixed_params[3])
    
    # Ir intensity
    i_ex = jnp.abs(ex_f.Ex)**2 + jnp.abs(ex_f.Ey)**2
    i_dep = jnp.abs(dep_f.Ex)**2 + jnp.abs(dep_f.Ey)**2
    
    # Resulting STED-like beam
    beta = 1 # Efficiency in the depletion
    
    i_eff = i_ex * (1 - beta * (1- jnp.exp(-(i_dep/i_ex)))) 

    return i_eff, i_ex, i_dep, ex_f, dep_f


def sharp_focus(input_field, parameters, fixed_params):
    """
    Define an optical table for sharp focus. 
    
    Illustrative scheme:

    (Ex, Ey) --> PBS --> Ex --> Modulate: SLM(alpha) --> Ex' --> PBS --> (Ex', Ey') --> Modulate: LCD(eta, theta) 
                  |                                               |                               |
                  Ey ---------> Modulate: SLM(phi) ----> Ey' -----/                          (Ex'', Ey'') --> Propagate: VRS(z) --> objective_lens(r,f)

    Parameters:
        input_field (VectorizedLight): Light to be modulated.
        parameters (list): Parameters to pass to the optimizer [alpha, phi, eta, theta, z1 and z2] for sSLM, LCD and VRS.
        fixed_params (jnp.array): Parameters to maintain fixed during optimization [r, f] that is radius and focal of the high NA objective lens.
        
    Returns VectorizedLight in the focal plane.
    
    Parameters in the optimizer are from (0,1). Conversion factor here are:
    
        1. Convert (0,1) to distance in cm -> Conversion factor for (offset, 100)*cm = (offset/100, 1).
        2. Convert (0,1) to phase (in radians) -> Conversion factor (-pi, pi) + pi = (0, 2pi) = (0, 1). 
    """
    offset = 3.8 # cm 

    # 1. Apply super-SLM:
    modulated_light = sSLM(input_field, parameters[0]* 2 * jnp.pi - jnp.pi, parameters[1]* 2 * jnp.pi - jnp.pi)
    
    # 2. Propagate:
    propagated_1, _ = modulated_light.VRS_propagation(z=(jnp.abs(parameters[4])*100+offset)*cm)
    
    # 3. Apply LCD: 
    modulated_light_2 = LCD(propagated_1, parameters[2]* 2 * jnp.pi - jnp.pi, parameters[3]* 2 * jnp.pi - jnp.pi)
    
    # 4. Propagate:
    propagated_2, _ = modulated_light_2.VRS_propagation(z=(jnp.abs(parameters[5])*100+offset)*cm)
    
    # 5. Strong focus using high NA objective:
    focused_light = VCZT_objective_lens(propagated_2, r=fixed_params[0], f=fixed_params[1], xout=fixed_params[2], yout=fixed_params[3])
    
    return focused_light

def XL_Setup(ls1, ls2, ls3, z, phase, angle, r, f, xout, yout):
    """
    Optical table with the general set-up in Fig. 6a (https://arxiv.org/abs/2310.08408#):  
    Building blocks consist of [sSLM -- z --> LCD], joint by z and beam splitters (BS). 
    
    Parameters:
    ls1, ls2, ls3 (VectorizedLight objects): Light sources.
    z (float): Distance to propagate.
    phase (jnp.array): Array with phase masks for sSLM.
    angle (float): Angle for LCDs.
    r (float): Radius of the objective lens.
    f (float): Focal length of the objective lens.
    xout, yout (jnp.arrays): Size of the detection window. 
    
    Returns VectorizedLight objects at 6 detectors. 
    
    -------------------------------------------------------------------
    
    * Scheme of the setup (distance z, phase masks, angles, and objective lens specs are common - this setup is for testing, not optimizing):
    

                             ls1                     ls2                     ls3
                              |                       |                       |
                            [BB 2]                  [BB 4]                 [BB 6]
                              |                       |                       |
                              z                       z                       z             
                              |                       |                       |
                              v                       v                       v    
    ls1 --> [BB 1] -- z --> [BS] --> [BB 7] -- z --> [BS] --> [BB 8] -- z -> [BS] --> OL --> Detector
                              |                       |                       |
                              z                       z                       z             
                              |                       |                       |
                              v                       v                       v    
                           [BB 13]                 [BB 15]                 [BB 17]
                              |                       |                       |
                              z                       z                       z             
                              |                       |                       |
                              v                       v                       v    
    ls2 --> [BB 3] -- z --> [BS] --> [BB 9] -- z --> [BS] --> [BB 10] - z -> [BS] --> OL --> Detector
                              |                       |                       |
                              z                       z                       z             
                              |                       |                       |
                              v                       v                       v    
                           [BB 14]                 [BB 16]                 [BB 18]
                              |                       |                       |
                              z                       z                       z             
                              |                       |                       |
                              v                       v                       v  
    ls3 --> [BB 5] -- z --> [BS] --> [BB 11] -- z -> [BS] -> [BB 12] -- z -> [BS] --> OL --> Detector
                              |                       |                       |
                              z                       z                       z             
                              |                       |                       |
                              v                       v                       v    
                              OL                      OL                      OL
                              |                       |                       |
                              v                       v                       v    
                           Detector                Detector                Detector
    """
    tic = time.perf_counter()
    # Define empty object for single-input BS.
    empty = VectorizedLight(ls1.x, ls1.y, ls1.wavelength)
    
    # Apply initial building blocks:
    path_ls1_1, _ = (building_block(ls1, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls1_2, _ = (building_block(ls1, phase, phase, z, angle, angle)).VRS_propagation(z)

    path_ls2_1, _ = (building_block(ls2, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls2_2, _ = (building_block(ls2, phase, phase, z, angle, angle)).VRS_propagation(z)

    path_ls3_1, _ = (building_block(ls3, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls3_2, _ = (building_block(ls3, phase, phase, z, angle, angle)).VRS_propagation(z)

    # Compute the first row
    ls1_ref, ls1_tra = BS(path_ls1_2, path_ls1_1, 0.5, 0.5, jnp.pi)
    path_ls1_3, _ = (building_block(ls1_tra, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls1_3_ref, path_ls1_3_tra = BS(empty, path_ls1_3, 0.5,0.5, jnp.pi)
    path_ls1_4, _ = (building_block(path_ls1_3_tra, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls1_4_ref, path_ls1_4_tra = BS(empty, path_ls1_4, 0.5,0.5, jnp.pi)                 
    ls1_f1 = VCZT_objective_lens(path_ls1_4_tra, r=r, f=f, xout=xout, yout=yout)

    path_ls2_2_ref, path_ls2_2_tra = BS(path_ls2_2, empty, 0.5, 0.5, jnp.pi)                 
    path_ls2_3, _ = (building_block(path_ls2_2_ref, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls2_3_ref, path_ls2_3_tra = BS(empty, path_ls2_3, 0.5,0.5, jnp.pi)
    ls2_f1 = VCZT_objective_lens(path_ls2_3_tra, r=r, f=f, xout=xout, yout=yout)  

    path_ls3_2_ref, path_ls3_2_tra = BS(path_ls3_2, empty, 0.5, 0.5, jnp.pi)                     
    ls3_f1 = VCZT_objective_lens(path_ls3_2_ref, r=r, f=f, xout=xout, yout=yout)  

    # Compute 2nd row
    path_ls1_5, _ = (building_block(ls1_ref, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls1_6, _ = (building_block(path_ls1_3_ref, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls1_7, _ = (building_block(path_ls1_4_ref, phase, phase, z, angle, angle)).VRS_propagation(z)

    path_ls2_4, _ = (building_block(path_ls2_2_tra, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls2_5, _ = (building_block(path_ls2_3_ref, phase, phase, z, angle, angle)).VRS_propagation(z)  
    path_ls3_3, _ = (building_block(path_ls3_2_tra, phase, phase, z, angle, angle)).VRS_propagation(z)   

    # Compute 3rd row
    path_ls1_3_ref, path_ls1_3_tra = BS(path_ls1_3, empty, 0.5,0.5, jnp.pi)
    path_ls1_8, _ = (building_block(path_ls1_3_ref, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls1_8_ref, path_ls1_8_tra = BS(path_ls1_6, path_ls1_8, 0.5,0.5, jnp.pi)
    path_ls1_9, _ = (building_block(path_ls1_8_tra, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls1_9_ref, path_ls1_9_tra = BS(path_ls1_7, path_ls1_9, 0.5,0.5, jnp.pi)                 
    ls1_f2 = VCZT_objective_lens(path_ls1_9_tra, r=r, f=f, xout=xout, yout=yout)  

    path_ls2_1_ref, path_ls2_1_tra = BS(path_ls2_1, empty, 0.5,0.5, jnp.pi)
    path_ls2_6, _ = (building_block(path_ls2_1_tra, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls2_6_ref, path_ls2_6_tra = BS(path_ls2_4, path_ls2_6, 0.5,0.5, jnp.pi)
    path_ls2_7, _ = (building_block(path_ls2_6_tra, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls2_7_ref, path_ls2_7_tra = BS(path_ls2_5, path_ls2_7,0.5,0.5, jnp.pi)
    ls2_f2 = VCZT_objective_lens(path_ls2_7_tra, r=r, f=f, xout=xout, yout=yout)  

    path_ls3_3_ref, path_ls3_3_tra = BS(path_ls3_2_tra, empty, 0.5,0.5, jnp.pi)                 
    ls3_f2 = VCZT_objective_lens(path_ls3_3_ref, r=r, f=f, xout=xout, yout=yout)  

    # Compute 4th row
    path_ls1_10, _ = (building_block(path_ls1_3_tra, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls2_8, _ = (building_block(path_ls2_1_ref, phase, phase, z, angle, angle)).VRS_propagation(z)

    path_ls1_11, _ = (building_block(path_ls1_8_ref, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls2_9, _ = (building_block(path_ls2_6_ref, phase, phase, z, angle, angle)).VRS_propagation(z)

    path_ls1_12, _ = (building_block(path_ls1_9_ref, phase, phase, z, angle, angle)).VRS_propagation(z)      
    path_ls2_10, _ = (building_block(path_ls2_7_ref, phase, phase, z, angle, angle)).VRS_propagation(z)  
    path_ls3_4, _ = (building_block(path_ls3_3_tra, phase, phase, z, angle, angle)).VRS_propagation(z)   

    # Compute 5th row       
    path_ls1_10_ref, path_ls1_10_tra = BS(path_ls1_10, empty, 0.5,0.5, jnp.pi)  
    path_ls1_13, _ = (building_block(path_ls1_10_ref, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls1_13_ref, path_ls1_13_tra = BS(path_ls1_11, path_ls1_13,0.5,0.5, jnp.pi)                 
    path_ls1_14, _ = (building_block(path_ls1_13_tra, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls1_14_ref, path_ls1_14_tra = BS(path_ls1_12, path_ls1_14,0.5,0.5, jnp.pi)                    
    ls1_f3 = VCZT_objective_lens(path_ls1_14_tra, r=r, f=f, xout=xout, yout=yout)  

    path_ls2_8_ref, path_ls2_8_tra = BS(path_ls2_8, empty, 0.5,0.5, jnp.pi)  
    path_ls2_11, _ = (building_block(path_ls2_8_ref, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls2_11_ref, path_ls2_11_tra = BS(path_ls2_9, path_ls2_11,0.5,0.5, jnp.pi)                  
    path_ls2_12, _ = (building_block(path_ls2_11_tra, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls2_12_ref, path_ls2_12_tra = BS(path_ls2_10, path_ls2_12,0.5,0.5, jnp.pi)     
    ls2_f3 = VCZT_objective_lens(path_ls2_12_tra, r=r, f=f, xout=xout, yout=yout)  

    path_ls3_1_ref, path_ls3_1_tra = BS(empty, path_ls3_1, 0.5,0.5, jnp.pi)  
    path_ls3_5, _ = (building_block(path_ls3_1_tra, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls3_5_ref, path_ls3_5_tra = BS(empty, path_ls3_5, 0.5,0.5, jnp.pi)                  
    path_ls3_6, _ = (building_block(path_ls3_5_tra, phase, phase, z, angle, angle)).VRS_propagation(z)
    path_ls3_6_ref, path_ls3_6_tra = BS(path_ls3_4, path_ls3_6,0.5,0.5, jnp.pi)  
    ls3_f3 = VCZT_objective_lens(path_ls3_6_tra, r=r, f=f, xout=xout, yout=yout)              

    # Compute 6th row
    ls1_f4 = VCZT_objective_lens(path_ls1_10_tra, r=r, f=f, xout=xout, yout=yout)  
    ls2_f4 = VCZT_objective_lens(path_ls2_8_tra, r=r, f=f, xout=xout, yout=yout)  
    ls3_f4 = VCZT_objective_lens(path_ls3_1_ref, r=r, f=f, xout=xout, yout=yout)
    
    ls1_f5 = VCZT_objective_lens(path_ls1_13_ref, r=r, f=f, xout=xout, yout=yout)  
    ls2_f5 = VCZT_objective_lens(path_ls2_11_ref, r=r, f=f, xout=xout, yout=yout)  
    ls3_f5 = VCZT_objective_lens(path_ls3_5_ref, r=r, f=f, xout=xout, yout=yout)
    
    ls1_f6 = VCZT_objective_lens(path_ls1_14_ref, r=r, f=f, xout=xout, yout=yout)  
    ls2_f6 = VCZT_objective_lens(path_ls2_12_ref, r=r, f=f, xout=xout, yout=yout)  
    ls3_f6 = VCZT_objective_lens(path_ls3_6_ref, r=r, f=f, xout=xout, yout=yout) 
    print("Time taken for generate XL experiment - in seconds", time.perf_counter() - tic)
    
    return ls1_f1, ls1_f2, ls1_f3, ls1_f4, ls1_f5, ls1_f6, ls2_f1, ls2_f2, ls2_f3, ls2_f4, ls2_f5, ls2_f6, ls3_f1, ls3_f2, ls3_f3, ls3_f4, ls3_f5, ls3_f6