import numpy as np

class waveform:
    def __init__(self, sampleFreq, initTime, pulseDur, centerFreq, phaseOffset):
        # Store internal variables
        self.centerFreq = centerFreq
        self.sampleFreq = sampleFreq
        self.pulseDur = pulseDur
        self.phaseOffset = phaseOffset
        # Generate time array
        self.__create_time_array(sampleFreq, initTime, pulseDur)

    def __create_time_array(self, sampleFreq, initTime, pulseDur):
        self._pulseTime = np.arange(initTime, initTime+pulseDur, 1/sampleFreq)

    def update_pulse_params(self, params):
        for key in params.keys():
            match key:
                case 'centerFreq':
                    self.centerFreq = params[key]
                case 'sampleFreq':
                    self.sampleFreq = params[key]
                case 'pulseDur':
                    self.pulseDur = params[key]
                case 'phaseOffset':
                    self.phaseOffset = params[key]
        # Update time array and pulse
        self.__create_time_array(self.sampleFreq, self._pulseTime[0], self.pulseDur)
    
    def update_time(self, timeStart):
        delTime = np.abs(timeStart - self._pulseTime[0])
        self._pulseTime += delTime
        
    def get_pulse_time(self):
        return self._pulseTime
    
    def get_pulse(self, time):
        # Update waveform time
        self.update_time(time)
        # Store local values
        time = self.get_pulse_time()
        fc = self.get_centerFreq()
        # Generate baseband pulse
        pulse = 1*np.exp(1j*(2*np.pi*fc*time + self.phaseOffset))
        return pulse, fc, self.get_sampleFreq()
    
    def get_centerFreq(self):
        return self.centerFreq
    
    def get_sampleFreq(self):
        return self.sampleFreq