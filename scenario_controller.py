import argparse
import radar_models.basic_radar.basic_radar as basic_radar
import target_models.basic_target.basic_target as target
import utils
import os
import numpy as np
import matplotlib.animation as ani

import utils.scenarioCalcs as scen
import utils.signalProp as prop
# Parse input arguments
parser = argparse.ArgumentParser(prog='Scenario Controller')
parser.add_argument('-r', '--radar_config', default='./test_files/radar_config.json', help='File path to radar configuration file')
parser.add_argument('-t', '--target_config', default='./test_files/target_config.json', help='File path to target configuration file')
args = parser.parse_args()
# Input configuration files for scenario players
# Send update requests for every 0.1 seconds
# Show receiver scenario player

scenarioTime = 10
delTime = 1e-3
updates = np.arange(0,scenarioTime,delTime)
# Configure Radar
radar_config = args.radar_config
tx = basic_radar.Radar(os.path.abspath(radar_config))
# Configure Target
target_config = args.target_config
tgt = target.Target(os.path.abspath(target_config))

# Find radar plotters and create animation

# Loop through simulation 
for time in updates:
    # Get transmitter pulse times
    tx.update_position(time)
    timePRI = tx.get_pulse_times(delTime)
    # Calculate pulse transmissions
    for time in timePRI:
        # Transmit pulse
        pulse = tx.transmit_pulse(time)
        # Update position for radar and target
        tx.update_position(pulse['time'])
        tgt.update_position(pulse['time'])
        # Calculate range between radar and target
        rng = scen.calcRange(tx, tgt)
        # Calculate geometry parameters
        scenParams = scen.calcPointing(tx, tgt)
        # Perform two-way propagation
        propSig, toa = prop.twoWayProp(pulse['pulse'], scenParams, rng, pulse['centerFreq'])
        toa = toa + time
        # Update pulse and send back 
        pulse['pulse'] = propSig
        pulse['time'] = toa
        tx.receive_pulse(pulse)

