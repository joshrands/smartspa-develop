"""@module hardware_iface
Manage system hardware.

Author: Josh Rands
Date: 2/8/2020 
Email: joshrands1@gmail.com
"""

import logging as log
from helpers import parse_xml, running_on_rpi

if running_on_rpi():
	import RPi.GPIO as GPIO


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
