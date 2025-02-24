import matplotlib.pyplot as plt
import numpy as np
import constants as c

def plot(sig_array, fs, fp):
    S = np.fft.fftshift(np.fft.fft(sig_array))
    rng = np.linspace(0,1/fp,1/fs)*c.c/2
    dop = np.linspace(fp/2,-fp/2,sig_array.shape[1])
    return