import numpy as np

import radar_models.basic_radar.basic_radar as radar
import target_models.basic_target.basic_target as target

def calcRange(radar: radar.Radar, target: target.Target):
    # Get transmitter and target positions
    tx_pos = radar.get_position()
    tgt_pos = target.get_position()
    # Calculate range between transmitter and target
    return np.sqrt(np.sum(np.square(tx_pos - tgt_pos)))

def calcPointing(radar: radar.Radar, target: target.Target):
    return {'Ltx': 1, 'Lrx': 1, 'Latm': 0.16, 'Ptx': 1, 'Gtx': 1, 'Grx': 1}