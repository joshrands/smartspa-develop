"""@package init
Initialize SmartSpa real time monitoring. 
 
This module initializes all system for real time monitoring.  
 
Author: Josh Rands
Date: 2/3/2020 
Email: joshrands1@gmail.com
"""

import logging as log
import argparse
from helpers import parse_xml


# Global Variables
main_config = None
sensing_config = None


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

	global main_config
	main_config = Config("main")

	init_sensing()
	init_dispensing()
	init_ui()
	init_db()

	
def init_sensing():
	"""Initialize the sensing subsystem.
	"""
	
	global sensing_config

	log.info("Initializing sensing subsystem.")

	sensing_config = Config("sensing")


def init_dispensing():
	"""Initialize the dispensing subsystem.
	"""
	
	log.warning("Dispensing init incomplete.")


def init_ui():
	"""Initialize the user interface.
	"""

	log.warning("UI init incomplete.")


def init_db():
	"""Initialize the database.
	"""

	log.warning("Database init incomplete.")

