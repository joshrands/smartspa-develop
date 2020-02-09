"""@module run_real_time
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
from controller import balance_chemical


if __name__ == '__main__':

	# Get command line arguments 

	arg_vals = init.get_args()

	init.init(arg_vals['verbose'])

	sample_interval_s = init.real_time_config.data['sample_interval_s']

	# Do everything
	while True:
		log.info("Checking system levels...")

		if (True == init.real_time_config.data['pH']):
			balance_chemical('pH', arg_vals['vis'])
		if (True == init.real_time_config.data['Cl']):
			balance_chemical('Cl', arg_vals['vis'])
		if (True == init.real_time_config.data['alkalinity']):
			balance_chemical('alkalinity', arg_vals['vis'])
		if (True == init.real_time_config.data['calcium']):
			balance_chemical('calcium', arg_vals['vis'])

		# sleep for sample interval
		time.sleep(sample_interval_s)

