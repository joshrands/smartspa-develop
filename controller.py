"""@module control
Pull together the sensing and dispensing to adjust chemical levels.
 
Author: Josh Rands
Date: 2/3/2020 
Email: joshrands1@gmail.com
"""

import logging as log
import time

from sensing import get_error
from release_chemical import release_chemical 
import init

# Global params
spa_mix_time_s = 5


def balance_chemical(chemical, vis=False):
	"""Balance the given chemical
	"""

	log.info("Balancing %s" % chemical)

	# get error from sensing system
	error = get_error(chemical, vis)

	if error != None:
		log.info("%s error = %.4d" % (chemical, error))

	# release appropriate amount of chemical into system
	release_chemical(chemical, 0)

	# let jets and main line pump mix chemicals into spa 
	log.info("Mixing chemicals for %d seconds..." % spa_mix_time_s)
	time.sleep(spa_mix_time_s)

	# Turn off spa jets 
	init.hardware.set_pin('spa_jets', False)

	# Turn off main line pump
	init.hardware.set_pin('main_line_pump', False)

