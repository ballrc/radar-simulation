import numpy as np
import pandas as pd
import json
import os
import waveforms.waveform as wav
import utils.plotters.rdmPlotter as rdm
import matplotlib.animation as ani

model_dir = os.path.dirname(os.path.abspath(__file__))
class Radar:
    def __init__(self, config_file='radar_config.json'):
        if os.path.exists(config_file):
            with open(config_file) as fid:
                config = json.load(fid)
            # Parse Radar Config
            self._sampFreq = config['sampleFreq']
            self._position = np.asarray(config['platform']['position'],dtype='float64')
            self._velocity = config['platform']['velocity']
            # Read mode file
            mode_file = os.path.join(model_dir,'modes',config['mode']+'.csv')
            waveform_params = pd.read_csv(mode_file, skipinitialspace=True).iloc[0].to_dict()
            # Load parameters
            self._pri = waveform_params['pri']
            self._cpi = int(waveform_params['cpi'])
            self._waveform = wav.waveform(self._sampFreq, 0, waveform_params['pw'], waveform_params['freq'], 0)
            self._refSig,_,_ = self._waveform.get_pulse(0)
            # Set up time variables
            self.curTime = 0
            self._extraTime = 0
            self._timeProc = np.arange(0, self._cpi*self._pri, 1/self._sampFreq)
            # Set up received stream
            self._rxStream = np.zeros(self._timeProc.shape, dtype='complex128')
            # Set up plotters
            self.plotters = [
            rdm.rdmPlotter(1/self._pri, self._cpi, self._waveform)
            ]
        else:
            raise Exception(f"Radar configuration file {config_file} does not exist")
    
    def process(self):
        # Match filter pulses
        mfSig = self._apply_matched_filter()
        # Reshape match filtered signals
        mfSig = np.reshape(mfSig, [self._cpi, int(len(mfSig)/self._cpi)])
        # Update plotters
        self.plotters[0].updatePlot(mfSig)
        
    
    def get_pulse_times(self, tStep):
        # Check for extra time
        if self._extraTime:
            # Calculate pulse time start
            tLastPulse = self.curTime - self._extraTime
            tNextPulse = tLastPulse + self._pri
            # Calculate pulse times
            txTime = np.arange(tNextPulse, self.curTime+tStep, self._pri)
            # Calculate extra time
            self._extraTime = (self.curTime+tStep - tNextPulse)%self._pri
        else:
            txTime = np.arange(self.curTime, self.curTime+tStep, self._pri)
            # Calculate extra time
            self._extraTime = (tStep)%self._pri
        return txTime
    
    def transmit_pulse(self, time):
        # Create waveform
        pulse, fc, fs = self._waveform.get_pulse(time)
        return {'pulse': pulse, 'centerFreq': fc, 'sampleFreq': fs, 'time': time}

    def receive_pulse(self, pulse):
        # Check if pulse is within current buffer
        done = False
        while not done:
            if pulse['time'] < self._timeProc[-1]:
                # Add pulse to buffer
                # Find index to add pulse
                indtR = np.where((pulse['time'] <= self._timeProc[:] + 1/(self._sampFreq*2)) & (pulse['time'] > self._timeProc[:] - 1/(self._sampFreq*2)))[0][0]
                # Find samples in buffer
                nSaPW = min(len(pulse['pulse']), len(self._timeProc[indtR:]))
                # Add pulse to buffer
                self._rxStream[indtR:indtR+nSaPW] = self._rxStream[indtR:indtR+nSaPW] + pulse['pulse']
                # TODO: Check for samples to be added to next buffer
                done = True
            else:
                # Process the signals 
                self.process()
                # Update process time
                self._update_proc_time()
                # Clear signal buffer
                self._rxStream[:] = 0

    def update_position(self,time):
        # Check if position is initialized
        if not hasattr(self, '_position'):
            # Initialize position
            self._position = [0, 0, 0]
        # Update position based on difference since last time
        self._position += np.multiply(self._velocity, time - self.curTime)
        # Update internal time
        self.curTime = time

    def _update_proc_time(self):
        self._timeProc += self._cpi*self._pri

    def _apply_matched_filter(self):
        """Applies matched filter to signals in rx stream based on reference signal.
        
        Parameters
        ---
        _rxStream: numpy.ndarray
            Complex samples received by radar system
        _refSig: numpy.ndarray
            Complex samples containing signal transmitted by radar system
        Returns
        ---
        mfSignal: numpy.ndarray
            Complex signal array containing matched filtered result of signals stored in """
        return np.fft.ifft(np.fft.fft(self._rxStream)*np.conjugate(np.fft.fft(np.pad(self._refSig, pad_width=(self._rxStream.shape[0] - len(self._refSig), 0)))))

    def get_position(self):
        return self._position