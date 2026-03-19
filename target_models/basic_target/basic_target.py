import numpy as np
import json
import os

class Target:
    def __init__(self, config_file):
        if os.path.exists(config_file):
            with open(config_file) as fid:
                config = json.load(fid)
            # Parse Target Config
            self._position = np.array(config['platform']['position'])
            self._velocity = np.array(config['platform']['velocity'])
            self._rcs = config['platform']['rcs']
            self._antenna = config['antenna']
            self.curTime = 0
        else:
            raise Exception(f"Target configuration file {config_file} does not exist")
        
    def update_time(self, time):
        # Update position
        self._update_position(time-self.curTime)
        # Update internal time
        self.curTime = time
    
    def _update_position(self, delTime):
        if hasattr(self, '_position'):
            self._position += np.multiply(delTime, self._velocity)
        else:
            self._position = [0, 0, 0] + np.multiply(self._velocity, delTime)

    def get_position(self):
        return self._position