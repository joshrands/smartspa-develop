"""@module control
Pull together the sensing and dispensing to adjust chemical levels.
 
Author: Josh Rands
Date: 2/3/2020 
Email: joshrands1@gmail.com
"""

import logging as log
from sensing import get_error

def balance_chemical(chemical, vis=False):
	"""Balance the given chemical
	"""

	log.info("Balancing %s" % chemical)

	error = get_error(chemical, vis)

	log.info("%s error = %0.4d" % (chemical, error))

