"""@module init
Initialize SmartSpa real time monitoring. 
 
This module initializes all system for real time monitoring.  
 
Author: Josh Rands
Date: 2/3/2020 
Email: joshrands1@gmail.com
"""

import logging as log
import argparse
from helpers import parse_xml, running_on_rpi
import matplotlib.image as image
import os

if running_on_rpi():
	import RPi.GPIO as GPIO

from sensing import get_average_rgb_from_img
from hardware_iface import Hardware

# Global Variables
hardware = None 
real_time_config = None
sensing_config = None
hardware_config = None

class Config:
	"""Config base class.

	Stores basic configuration information for a given subsytem.
	A given configuration will read its configuration input file and created 
	a dictionary of the data stored. 
	Example usage could be storing pin numbers of motors, ip addresses of hosts, etc. 
	"""

	def __init__(self, file_name, file_type='xml'):
		"""Initialize a configuration object.
		"""

		self.file_name = file_name
		self.file_type = file_type
		self.data = {}
		self.config_dir = "config/"

		self.parse_config_file()


	def parse_config_file(self):
		"""Parse configuration file and store data in data dictionary.
		"""
		
		log.info("Parsing configuration file: %s.%s" % (self.file_name, self.file_type))

		if 'xml' == self.file_type:
			path = self.config_dir + self.file_name + "." + self.file_type
			self.data = parse_xml(path)

			log.info(self.data)
	

def get_args():
	"""Parse command line arguments.
	"""

	parser = argparse.ArgumentParser()
	parser.add_argument("--vis", action='store_true', help="Visualize input")
	parser.add_argument("--verbose", action='store_true', help="Verbose messages")

	args = parser.parse_args()
	arg_vals = vars(args)

	return arg_vals


def init(verbose):
	"""SmartSpa initialize function. 

	This function initializes all systems.
	"""

	if verbose:
		log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
	else:
		log.basicConfig(format="%(levelname)s: %(message)s")

	log.info("Initializing SmartSpa subsystems.")

	global real_time_config
	real_time_config = Config("real_time")

	init_sensing()
	init_hardware()
	init_ui()
	init_db()


def calibrate_chemical(chemical):
	log.info("Calibrating %s" % chemical)

	directory = os.fsencode("calibrate/" + chemical)
	out_file = open("calibrate/" + chemical + "/cal.csv","w")

	for file in os.listdir(directory):
		file_name = os.fsdecode(file)
		file_path = "calibrate/" + chemical + "/" + file_name

		if file_path[-3:] != 'png':
			continue

		img = image.imread(file_path)
		r,g,b = get_average_rgb_from_img(img)

    # write to config file
    # get pH 
		nums = file_name.split(',')
		whole = nums[0]
		decimal = nums[1].split('.')[0]

		out_file.write(whole + "." + decimal + ",")
		out_file.write("(" + str(r) + " " + str(g) + " " + str(b) + ")\n")

	out_file.close()

	log.info("%s calibrated." % chemical)

	
def init_sensing():
	"""Initialize the sensing subsystem.
	"""
	
	global sensing_config

	log.info("Initializing sensing subsystem.")

	sensing_config = Config("sensing")

	if True == sensing_config.data['calibrate']:
		log.info("Calibrating sensing scale...")
		
		calibrate_dir = os.fsencode("calibrate")
		
		for file in os.listdir(calibrate_dir):
			calibrate_chemical(os.fsdecode(file))


def init_hardware():
	"""Initialize the dispensing subsystem.
	"""

	global hardware_config 
	global hardware

	# initialize hardware class 
	hardware = Hardware()

	log.info("Initializing hardware systems.")

	hardware_config = Config("hardware")

	# Get pin numbers from configuration file
	SENSING_LED_PIN = hardware_config.data['sensing_led_pin']
	SPA_JETS_PIN = hardware_config.data['spa_jets_pin']
	MAIN_LINE_PUMP_PIN = hardware_config.data['main_line_pump_pin']
	REAGENT_SOLENOID_VALVE_PIN = hardware_config.data['reagent_solenoid_valve_pin']
	PH_PERISTALTIC_PUMP_PIN = hardware_config.data['ph_reagent_peristaltic_pump_pin']

	OPEN_MAIN_LINE_VALVE_PIN = hardware_config.data['open_main_line_valve_pin']
	CLOSE_MAIN_LINE_VALVE_PIN = hardware_config.data['close_main_line_valve_pin']

	# this will likely be 4 pins to drive a stepper 
	MIXING_PROP_MOTOR_PIN = hardware_config.data['mixing_prop_motor_pin']

	# configure all rpi pins
	if running_on_rpi():
		hardware.add_pin("sensing_led", SENSING_LED_PIN, 'OUTPUT')
		hardware.add_pin("spa_jets", SPA_JETS_PIN, 'OUTPUT')
		hardware.add_pin("main_line_pump", MAIN_LINE_PUMP_PIN, 'OUTPUT')
		hardware.add_pin("reagent_solenoid_valve", REAGENT_SOLENOID_VALVE_PIN, 'OUTPUT')
		hardware.add_pin("ph_pump", PH_PERISTALTIC_PUMP_PIN, 'OUTPUT')
		hardware.add_pin("mixing_prop_motor", MIXING_PROP_MOTOR_PIN, 'OUTPUT')
		hardware.add_pin("open_main_line_valve", OPEN_MAIN_LINE_VALVE_PIN, 'OUTPUT')
		hardware.add_pin("close_main_line_valve", CLOSE_MAIN_LINE_VALVE_PIN, 'OUTPUT')

	log.warning("Dispensing hardware init incomplete.")


def init_ui():
	"""Initialize the user interface.
	"""

	log.warning("UI init incomplete.")


def init_db():
	"""Initialize the database.
	"""

	log.warning("Database init incomplete.")

