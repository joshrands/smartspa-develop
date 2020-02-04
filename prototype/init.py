"""@package init
Initialize SmartSpa real time monitoring. 
 
This module initializes all system for real time monitoring.  
 
Author: Josh Rands
Date: 2/3/2020 
Email: joshrands1@gmail.com
"""

class Config:
	"""Config base class.

	Stores basic configuration information for a given subsytem.
	A given configuration will read its configuration input file and created 
	a dictionary of the data stored. 
	Example usage could be storing pin numbers of motors, ip addresses of hosts, etc. 
	"""

	file_name = None
	file_type = "xml"
	data = {}	
	config_dir = "config/"
	

def init():
	"""SmartSpa initialize function. 

	This function initializes all systems.
	"""
	print("Initializing SmartSpa systems...")

	
def init_sensing():
	"""Initialize the sensing subsystem.
	"""
	pass 


def init_dispensing():
	"""Initialize the dispensing subsystem.
	"""
	pass 


def init_ui():
	"""Initialize the user interface.
	"""
	pass


def init_db():
	"""Initialize the database.
	"""
	pass

