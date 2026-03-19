import radar_models.basic_radar.basic_radar as radar
import target_models.basic_target.basic_target as target
import utils.scenarioCalcs as calcs
import utils.signalProp as prop
import argparse
import os
import matplotlib.pyplot as plt
# Parse input arguments
parser = argparse.ArgumentParser(prog='Scenario Controller')
parser.add_argument('-r', '--radar_config', default='./test_files/radar_config.json', help='File path to radar configuration file')
parser.add_argument('-t', '--target_config', default='./test_files/target_config.json', help='File path to target configuration file')
args = parser.parse_args()

# Configure Radar
radar_config = args.radar_config
tx = radar.Radar(os.path.abspath(radar_config))
# Configure Target
target_config = args.target_config
tgt = target.Target(os.path.abspath(target_config))

# Loop through sim
scenarioTime = tx._pri*tx._cpi

# Update target position
tx.update_position(0)
timePRI = tx.get_pulse_times(scenarioTime)
# Calculate pulse transmissions
for time in timePRI:
    # Transmit pulse
    pulse = tx.transmit_pulse(time)
    # Update time
    tx.update_position(pulse['time'])
    tgt.update_time(pulse['time'])
    # Calculate range between radar and target
    rng = calcs.calcRange(tx,tgt)
    # Calculate geometry params
    scenParams = calcs.calcPointing(tx,tgt)
    # Perform 2 way propagation
    propSig,toa = prop.twoWayProp(pulse['pulse'], scenParams, rng, pulse['centerFreq'])
    toa = toa + time
    # Update pulse and send back
    pulse['pulse'] = propSig
    pulse['time'] = toa
    tx.receive_pulse(pulse)