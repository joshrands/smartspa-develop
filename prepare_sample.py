"""@module prepare_sample
Prepare sample for sensing 

Author: Josh Rands
Date: 2/9/2020 
Email: joshrands1@gmail.com
"""

import logging as log
import time

import init
from helpers import running_on_rpi
from hardware_iface import open_main_valve, close_main_valve_halfway

if running_on_rpi():
	import RPi.GPIO as GPIO

# Global params for timing stuff
test_chamber_fill_time_s = 4
reagent_drip_time_s = 1


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
	# TODO: Do we want to turn on the spa jets here? 
	log.warning("NOT TURNING ON SPA JETS.")
#	init.hardware.set_pin('spa_jets', True)

	# Turn on main line pump
	init.hardware.set_pin('main_line_pump', True)

	# Open reagent solenoid valve by sending power 
	init.hardware.set_pin('reagent_solenoid_valve', True)	

	# Close main valve halfway
	close_main_valve_halfway()

	# Wait for test chamber to fill 
	log.info("Waiting for test chamber to fill with water...")
	time.sleep(test_chamber_fill_time_s)

	# Open main line valve all the way 
	open_main_valve()

	# Close reagent solenoid valve 
	init.hardware.set_pin('reagent_solenoid_valve', False)

	# Turn on reagent peristaltic pump 
	init.hardware.set_pin(chemical + '_pump', True)

	# Wait until reagent drops are dispensed
	log.info("Waiting for reagent drops to be dispensed...")
	time.sleep(reagent_drip_time_s)

	# Turn off reagent peristaltic pump 
	init.hardware.set_pin(chemical + "_pump", False)

	# Mix reagent in sample tube 
	mix_reagent()

	# Done! 

	log.info("Sample prepared!")
