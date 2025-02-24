import numpy as np
import constants as c

def oneWayProp(signal, radarParams, rng, fc, mode):
    """Perform one-way propagation of a signal with included attenuation from losses/gains and phase shift.
    
    Inputs
    ---
    radarParams (dictionary):
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
            loss = radarParams['Ltx']
            gain = radarParams['Ptx']*radarParams['Gtx']
        case 'Rx':
            requiredParams = ['Lrx', 'Latm', 'Grx']
            loss = radarParams['Lrx']
            gain = radarParams['Grx']
    for param in requiredParams:
        if param not in radarParams:
            raise Exception(f"Parameter {param} missing from radarParams!!")
    # Calculate one-way atmospheric loss
    latm = 10**(radarParams['Latm']*1e-3*rng/10)
    # Calculate phase shift due to propagation
    lam = c.c/fc
    k = 2*np.pi/lam
    phase = -k*rng
    # Apply gains/losses to signal
    propSignal = signal * np.sqrt(gain/((4*np.pi*rng)**2*loss*latm)) * np.exp(1j*phase)
    # Find echo time of arrival
    toa = rng/c.c
    return propSignal, toa

def twoWayProp(signal, radarParams, rng, fc):
    """Perform two-way propagation of a signal with included attenuation from losses/gains and phase shift.
    
    Inputs
    ---
    radarParams (dictionary):
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
    requiredParams = ['Ltx', 'Lrx', 'Latm', 'Ptx', 'Gtx', 'Grx']
    loss = radarParams['Ltx'] * radarParams['Lrx']
    gain = radarParams['Ptx'] * radarParams['Gtx'] * radarParams['Grx']
    for param in requiredParams:
        if param not in radarParams:
            raise Exception(f"Parameter {param} missing from radarParams!!")
    # Calculate one-way atmospheric loss
    latm = 10**(radarParams['Latm']*1e-3*rng*2/10)
    # Calculate phase shift due to propagation
    lam = c.c/fc
    k = 2*np.pi/lam
    phase = -k*rng*2
    # Apply gains/losses to signal
    propSignal = signal * np.sqrt(gain/((4*np.pi*rng**2)**2*4*np.pi*loss*latm)) * np.exp(1j*phase)
    # Find echo time of arrival
    toa = rng*2/c.c
    return propSignal, toa