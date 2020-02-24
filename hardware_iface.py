"""@module hardware_iface
Manage system hardware.

Author: Josh Rands
Date: 2/8/2020 
Email: joshrands1@gmail.com
"""

import logging as log
import time 

from helpers import parse_xml, running_on_rpi
import init

if running_on_rpi():
	import RPi.GPIO as GPIO

# Global variables 
close_halfway_time_s = 1


class Hardware:
	"""Hardware class.

	Stores PIN information for hardware components connected to our board.
	"""

	def __init__(self):
		"""Initialize the hardware class by configuring hardware setup.
		"""
		self.PINS = {}
		self.PIN_TYPES = {}

		# configure raspberry pi to BOARD mode 
		# this means all pin numbers should be the true pin number on the pi
		if running_on_rpi():
			GPIO.setmode(GPIO.BOARD)
			log.info("Raspberry pi set to GPIO.BOARD.")

		log.info("Hardware class created.")


	def add_pin(self, name, pin_number, pin_type):
		"""Add a pin to the pin map and initialize to pin_type.
		"""

		if None != pin_number:
			self.PINS[name] = pin_number
		else:
			log.warning("No pin number set for %s" % name)
			return

		if running_on_rpi():
			if pin_type == 'OUTPUT':
				GPIO.setup(pin_number, GPIO.OUT)
				self.PIN_TYPES[pin_number] = pin_type
			elif pin_type == 'INPUT':
				GPIO.setup(pin_number, GPIO.IN)
				self.PIN_TYPES[pin_number] = pin_type
			else:
				log.warning("Unknown pin type: %s" % pin_type)
				self.PIN_TYPES[pin_number] = None
		else:
			log.warning("Cannot initialize pin, not running on raspberry pi.")

		log.info("%s set to pin %d as type %s" % (name, pin_number, pin_type))


	def set_pin(self, name, state):
		"""Set the state of pin 'name' to state 'state'
		"""
		if not name in self.PINS:
			log.warning("No pin exists for %s." % name)
			return

		PIN = self.PINS[name]

		if running_on_rpi():
			if self.PIN_TYPES[PIN] == 'OUTPUT':
				GPIO.output(PIN, state)

			log.info("Set %s, pin %d, to %s" % (name, PIN, state))
		else:
			log.warning("Not running on RPi. Can't set pin.")


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


def close_main_valve():
	"""Use a timer to close the main valve all the way 
	"""
	# close the valve by powering the 'close' pin
	init.hardware.set_pin('close_main_line_valve', True)
	time.sleep(close_halfway_time_s*2)
	init.hardware.set_pin('close_main_line_valve', False)


def open_chemical_dispensing_doors():
	"""Drive the chemical dispensing doors servo to open them
	and allow chemicals to drop into the water.
	"""
	log.warning("Chemical dispensing door servo open not implemented.")


def close_chemical_dispensing_doors():
	"""Drive the chemical dispensing doors servo to close them
	"""
	log.warning("Chemical dispensing door servo close not implemented.")


def spin_chemical_release_auger():
	"""Turn on the stepper motor to spin the auger and release
	chemicals into the water.
	"""
	log.warning("Auger stepper motor not implemented.")


def stop_chemical_release_auger():
	"""Stop the auger stepper motor.
	"""
	log.warning("Auger stepper motor not implemented.")

