import numpy as np
class Waveform:
    def __init__(self, waveform_settings=None):
        self.waveform = np.zeros(())
        if waveform_settings:
            self.initialize_waveform(waveform_settings)
    
    def initialize_waveform(self, settings):
        self.fs = settings['fs']
        self.time = settings['time']

    def get_waveform(self):
        return self.waveform