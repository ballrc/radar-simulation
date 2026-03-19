import matplotlib.pyplot as plt
import numpy as np
import constants as c
import waveforms.waveform as wav

class rdmPlotter:

    def __init__(self, fp, cpi, waveform = wav.waveform):
        self.type = 'rdm'
        # Initialize Plot
        self.fig, self.ax = self.initializePlot(waveform, fp, cpi)
        

    def initializePlot(self, waveform, fp, cpi):
        plt.ion()
        fig, ax = plt.subplots()
        fs = waveform.get_sampleFreq()
        fc = waveform.get_centerFreq()
        rng = np.arange(0,1/fp,1/fs)*c.c/2*1e-3
        dop = np.linspace(fp/2,-fp/2,cpi)*c.c/(fc*2)
        meshrng, meshdop = np.meshgrid(rng, dop)
        self.quad = ax.pcolormesh(meshdop, 
                      meshrng, 
                      np.random.rand(len(dop),len(rng)),
                      shading='gouraud',
                      cmap='jet',
                      animated=True)
        ax.set_xlabel('Velocity [m/s]')
        ax.set_ylabel('Range [km]')
        plt.show(block=False)
        plt.pause(0.1)
        # Get copy of figure
        self.bg = fig.canvas.copy_from_bbox(fig.bbox)
        ax.draw_artist(self.quad) 
        fig.canvas.blit(fig.bbox)
        return fig, ax

    def updatePlot(self, data):
        self.fig.canvas.restore_region(self.bg)
        doppler = self._processData(data)
        self.quad.set_array(10*np.log10(abs(doppler.ravel())))
        vmax = 10*np.log10(abs(doppler.ravel())).max()
        self.quad.set_clim([vmax-20, vmax])
        self.ax.draw_artist(self.quad)
        self.fig.canvas.blit(self.fig.bbox)
        self.fig.canvas.flush_events()
    
    def _processData(self, data):
        return np.fft.fftshift(np.fft.fft(data,axis=0),axes=0)