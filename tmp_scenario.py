import radar_models.basic_radar.radar as rad
import matplotlib.pyplot as plt
import numpy as np
import waveforms.waveform as wav
# Initialize radar
msTokms = 1e-3
Ptx = 150e3
Gtx = 10**(45.25/10)
Ltx = 10**(3.1/10)
Lrx = 10**(2.4/10)
Lsp = 10**(3.2/10)
Latm = 0.16
Fc = 9.4e9
tau = 1e-6
Fp = 2e4
CPI = 50
Tp = 1/Fp
lam = 3e8/Fc
k = 2*np.pi/lam
Ts = tau/40
Fs = 1/Ts
SNR = 20
waveform = wav.waveform(Fs, 0, tau, Fc, 0)
# Get noise power level
noiseAmp = np.sqrt(Ptx*Gtx**2*lam**2*2/((4*np.pi)**3*(5e3)**4*Ltx*Lrx*Lsp*10**(Latm*2*1e-3*5e3/10)))

# Generate Noise Signal 
timePRI = np.arange(0,Tp,Ts)
timeCPI = np.arange(0,Tp*CPI,Tp)
timePW = np.arange(0,tau,Ts)
nSaPW = len(timePW)
nSaPRI = len(timePRI)
signal = noiseAmp/10**(SNR/10) * np.random.randn(CPI, nSaPRI) * np.exp(1j*(2*np.pi*Fc*timePRI + 2*np.pi*np.random.rand(CPI,nSaPRI)))
# target params
tgt_pos = [3e3, 0, 0]
tgt_vel = [120, 0, 0]
tgt_rcs = 10
for pidx in range(CPI):
    # Update target position
    tgt_pos += np.multiply(tgt_vel,Tp)
    tgt_phase = -2*k*np.sqrt(np.sum(np.square(tgt_pos)))
    # Get signal return
    waveform.update_time(timeCPI[pidx])
    sig = waveform.get_signal()
    # Apply phase shift
    sig = sig *np.exp(1j*tgt_phase)
    # Find time of radar echo
    tR = 2*np.sqrt(np.sum(np.square(tgt_pos)))/3e8
    # Find index of radar echo
    indtR = np.where((tR <= timePRI[:] + Ts/2) & (tR >= timePRI[:] - Ts/2))[0][0]
    # Add samples to signals vector
    signal[pidx, indtR:indtR+len(sig)] += sig
S = np.fft.fftshift(np.fft.fft(signal,CPI,0),0)+1e-12
rng = timePRI*3e8/2
freq = np.linspace(Fp/2,-Fp/2,CPI)*lam/2
plt.pcolor(rng*msTokms, freq, 10*np.log10(abs(S)))
plt.show()
