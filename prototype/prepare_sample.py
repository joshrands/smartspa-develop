"""@module prepare_sample
Prepare sample for sensing 

Author: Josh Rands
Date: 2/9/2020 
Email: joshrands1@gmail.com
"""

import logging as log
import init
from helpers import running_on_rpi
import time

if running_on_rpi():
	import RPi.GPIO as GPIO

# Global params for timing stuff
close_halfway_time_s = 1
test_chamber_fill_time_s = 4
reagent_drip_time_s = 1


def close_main_valve_halfway():
	"""Use a timer to close the main valve halfway
	"""
	# close the valve by powering the 'close' pin
	init.hardware.set_pin('close_main_line_valve', True)
	time.sleep(close_halfway_time_s)
	init.hardware.set_pin('close_main_line_valve', False)


def open_main_valve():
	"""Use a timer to open the main valve all the way 
	"""
	# open the valve by powering the 'open' pin
	init.hardware.set_pin('open_main_line_valve', True)
	time.sleep(close_halfway_time_s)
	init.hardware.set_pin('open_main_line_valve', False)


def mix_reagent():
	"""Drive the stepper motor to mix the reagent in the sample tube
	"""
	log.warning("Reagent not being mixed.")

	# TODO: Turn on mixing prop motor with stepper pins...

	# TODO: Wait until mixed 

	# TODO: Turn off mixing prop motor 


def prepare_sample(chemical):
	"""Prepare the sample by mixing the reagent in the sample tube.
	"""

	# Turn on spa jets 
	init.hardware.set_pin('spa_jets', True)

	# Turn on main line pump
	init.hardware.set_pin('main_line_pump', True)

	# Open reagent solenoid valve by sending power 
	init.hardware.set_pin('reagent_solenoid_valve', True)	

	# Close main valve halfway
	close_main_valve_halfway()

	# Wait for test chamber to fill 
	time.sleep(test_chamber_fill_time_s)

	# Open main line valve all the way 
	open_main_valve()

	# Close reagent solenoid valve 
	init.hardware.set_pin('reagent_solenoid_valve', False)

	# Turn on reagent peristaltic pump 
	init.hardware.set_pin(chemical + '_pump', True)

	# Wait until reagent drops are dispensed
	time.sleep(reagent_drip_time_s)

	# Turn off reagent peristaltic pump 
	init.hardware.set_pin(chemical + "_pump", False)

	# Mix reagent in sample tube 
	mix_reagent()

	# Done! 

	log.info("Sample not prepared!")
