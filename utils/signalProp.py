import numpy as np
import constants as c

def oneWayProp(signal, scenParams, rng, fc, mode):
    """Perform one-way propagation of a signal with included attenuation from losses/gains and phase shift.
    
    Inputs
    ---
    scenParams (dictionary):
        Dictionary containing the gains/loss parameters required to calculate one-way propagation.
    signal (numpy array):
        Numpy array containing the complex signal samples.
    rng (float):
        Range between targets [meters]
    fc (float):
        Center frequency of signal [Hertz]
    mode (string):
        Mode of signal propagation ['Tx', 'Rx']

    Returns
    ---
    propSignal (numpy array):
        Numpy array containing the complex signal samples after applying attenuation/phase shift due to signal propagation.
    toa (float):
        Time of arrival for signal based on range [seconds]
    """
    match mode:
        case 'Tx':
            requiredParams = ['Ltx', 'Latm', 'Ptx', 'Gtx']
            loss = scenParams['Ltx']
            gain = scenParams['Ptx']*scenParams['Gtx']
        case 'Rx':
            requiredParams = ['Lrx', 'Latm', 'Grx']
            loss = scenParams['Lrx']
            gain = scenParams['Grx']
    for param in requiredParams:
        if param not in scenParams:
            raise Exception(f"Parameter {param} missing from scenParams!!")
    # Calculate one-way atmospheric loss
    latm = 10**(scenParams['Latm']*1e-3*rng/10)
    # Calculate phase shift due to propagation
    lam = c.c/fc
    k = 2*np.pi/lam
    phase = -k*rng
    # Apply gains/losses to signal
    propSignal = signal * np.sqrt(gain/((4*np.pi*rng)**2*loss*latm)) * np.exp(1j*phase)
    # Find echo time of arrival
    toa = rng/c.c
    return propSignal, toa

def twoWayProp(signal, scenParams, rng, fc):
    """Perform two-way propagation of a signal with included attenuation from losses/gains and phase shift.
    
    Inputs
    ---
    scenParams (dictionary):
        Dictionary containing the gains/loss parameters required to calculate two-way propagation.
    signal (numpy array):
        Numpy array containing the complex signal samples.
    rng (float):
        Range between targets [meters]
    fc (float):
        Center frequency of signal [Hertz]

    Returns
    ---
    propSignal (numpy array):
        Numpy array containing the complex signal samples after applying attenuation/phase shift due to signal propagation.
    toa (float):
        Time of arrival for signal based on range [seconds]
    """
    # Check if parameters are givem
    requiredParams = ['Ltx', 'Lrx', 'Latm', 'Ptx', 'Gtx', 'Grx']
    for param in requiredParams:
        if param not in scenParams:
            raise Exception(f"Parameter {param} missing from scenParams!!")
    # Calculate loss and gain based on scenario parameters
    loss = scenParams['Ltx'] * scenParams['Lrx']
    gain = scenParams['Ptx'] * scenParams['Gtx'] * scenParams['Grx']
    # Calculate two-way atmospheric loss
    latm = 10**(scenParams['Latm']*1e-3*rng*2/10)
    # Calculate phase shift due to propagation
    lam = c.c/fc
    k = 2*np.pi/lam
    phase = -k*rng*2
    # Apply gains/losses to signal
    propSignal = signal * np.sqrt(gain/((4*np.pi*rng**2)**2*4*np.pi*loss*latm)) * np.exp(1j*phase)
    # Find echo time of arrival
    toa = rng*2/c.c
    return propSignal, toa