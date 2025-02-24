import numpy as np

class waveform:
    def __init__(self, sampleFreq, initTime, signalDur, centerFreq, phaseOffset):
        # Store internal variables
        self.centerFreq = centerFreq
        self.sampleFreq = sampleFreq
        self.signalDur = signalDur
        self.phaseOffset = phaseOffset
        # Generate time array
        self.__create_time_array(sampleFreq, initTime, signalDur)

    def __create_time_array(self, sampleFreq, initTime, signalDur):
        self._signalTime = np.arange(initTime, initTime+signalDur, 1/sampleFreq)

    def update_signal_params(self, params):
        for key in params.keys():
            match key:
                case 'centerFreq':
                    self.centerFreq = params[key]
                case 'sampleFreq':
                    self.sampleFreq = params[key]
                case 'signalDur':
                    self.signalDur = params[key]
                case 'phaseOffset':
                    self.phaseOffset = params[key]
        # Update time array and signal
        self.__create_time_array(self.sampleFreq, self._signalTime[0], self.signalDur)
    
    def update_time(self, timeStart):
        delTime = np.abs(timeStart - self._signalTime[0])
        self._signalTime += delTime
        
    def get_signal_time(self):
        return self._signalTime
    
    def get_signal(self):
        return 1*np.exp(1j*(2*np.pi*self.centerFreq*self.get_signal_time() + self.phaseOffset))