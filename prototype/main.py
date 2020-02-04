"""@package main
Perform SmartSpa real time monitoring. 
 
This module pulls all subsystems together to properly perform real time chemical level
monitoring. 
 
Author: Josh Rands
Date: 2/3/2020 
Email: joshrands1@gmail.com
"""

import init
import time
import logging as log
#from sensing import get_error

if __name__ == '__main__':

	# Get command line arguments 

	arg_vals = init.get_args()

	init.init(arg_vals['verbose'])

	sample_interval_s = init.main_config.data['sample_interval_s']

	# Do everything
	while True:
		log.info("Checking system levels...")

		if (True == init.main_config.data['pH']):
			log.info("Checking pH level")

		# sleep for sample interval
		time.sleep(sample_interval_s)

