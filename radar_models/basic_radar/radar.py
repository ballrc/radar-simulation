import numpy as np
import json
import os

class Radar:
    def __init__(self, config_file='radar_config.json'):
        if os.path.exists(config_file):
            self.__config = json.load(config_file)
        else:
            raise Exception(f"Radar configuration file {config_file} does not exist")
    
    def process(self):
        
        return
    def update_time(self,time):
        # Update position
        self._update_position(time-self.curTime)
        # Update internal time
        self.curTime = time

    def _update_position(self, delTime):
        if hasattr(self, '_position'):
            self._position += self._velocity * delTime
        else:
            self._position = self.__config['platform']['position']
            self._velocity = self.__config['platform']['velocity']

        
if __name__ == "__main__":
    radar = Radar()
    radar2 = Radar('./test.json')
    print('done')