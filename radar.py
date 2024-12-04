import numpy as np
import json
import os

class Radar:
    def __init__(self, config_file='radar_config.json'):
        if os.path.exists(config_file):
            config = json.load(config_file)
        else:
            raise Exception(f"Radar configuration file {config_file} does not exist")
        
if __name__ == "__main__":
    radar = Radar()
    radar2 = Radar('./test.json')
    print('done')