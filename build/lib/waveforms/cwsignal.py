import numpy as np
from waveform import Waveform
class CWSignal(Waveform):
    def __init__(self, waveform_settings):
        super().__init__()
        # Configure waveform
        self.waveform_settings = waveform_settings

    def generate_waveform(self, settings):
        