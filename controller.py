"""@module control
Pull together the sensing and dispensing to adjust chemical levels.
 
Author: Josh Rands
Date: 2/3/2020 
Email: joshrands1@gmail.com
"""

import logging as log
import time

from sensing import Metric, get_img 
from sensing import interpolate_chemical_property_from_img_linear, interpolate_chemical_property_from_img_rgb
from release_chemical import release_chemical 
from prepare_sample import prepare_sample
from hardware_iface import close_main_valve_halfway, open_main_valve, close_main_valve
import init

# Global params
spa_mix_time_s = 5


def balance_chemical(chemical, vis=False):
	"""Balance the given chemical
	"""

	log.info("Balancing %s" % chemical)

	# prepare the sample 
	prepare_sample(chemical.lower())

	source = init.sensing_config.data['image_source'] 
	img = get_img(source)

	if None == img.any():
		log.error("Invalid image.")
		return -1

	# get interpolated value 
	sensed_value = None

	if 'pH' == chemical:
		log.info("Interpolating pH using hue values.")
		sensed_value = interpolate_chemical_property_from_img_linear(chemical, img, Metric.HUE)
	else:
		log.error("Interpolating unknown chemical.")
		return None

	error = None

	if None != sensed_value:
		desired_value = init.control_config.data['ph_target']
		log.info("Desired value = " + str(desired_value))
		log.info("Sensed value = " + str(sensed_value))

		error = float(desired_value) - float(sensed_value)

		log.info("%s error = %.4f" % (chemical, error))
	else:
		log.error("No sensed value.")
		return -2

	# convert the error into grams released 
	spa_volume_gal = init.system_config.data['spa_volume_gal']

	chemical_type, chemical_quantity_g = get_release_quantity_g(chemical, spa_volume_gal, error)

	# picture processed, open reagent solenoid valve to flush system 
	init.hardware.set_pin('reagent_solenoid_valve', True)

	# close main line valve halfway to force water into sensing system
	close_main_valve_halfway()

	# wait for reagent sensing system to flush out 
	flush_interval_s = init.real_time_config.data['sensor_flush_interval_s']
	log.info("Waiting %d seconds for sensing system to flush out." % flush_interval_s)
	time.sleep(flush_interval_s)	

	# turn off main line pump
	init.hardware.set_pin('main_line_pump', False)

	# close main line valve all the way 
	close_main_valve()

	# system ready to release chemicals!
	log.info("System ready for chemical granule release.")

	# release appropriate amount of chemical into system
	if None != chemical_type and chemical_quantity_g > 0:
		# release the chemicals 
		release_chemical(chemical_type, chemical_quantity_g)

		# open main line valve to flow water 
		open_main_valve()

		# turn on main line pump 
		init.hardware.set_pin('main_line_pump', True)

		# turn on the spa jets to help mix chemicals 
		init.hardware.set_pin('spa_jets', True)

		# let jets and main line pump mix chemicals into spa 
		log.info("Mixing chemicals for %d seconds..." % spa_mix_time_s)
		time.sleep(spa_mix_time_s)

		# Turn off spa jets 
		init.hardware.set_pin('spa_jets', False)

		# Turn off main line pump 
		init.hardware.set_pin('main_line_pump', False)


def get_release_quantity_g(chemical, spa_volume_gal, error):
	""" Get what chemical should be released and the quantity of 
	the chemical that should be released from this error and spa size. 
	Returns chemical_type, chemical_quantity (in grams)
	"""

	if 'pH' == chemical:
		log.info("Determining chemical release for pH error %.4f" % error)
		ph_gain = init.control_config.data['ph_gain']

		# if the error is less than 0.2, release none
		if 0.2 > abs(error): 
			log.info("No chemicals needed. pH balanced.")
			return None, 0
		elif error > 0:
			# the error is > 0, the desired is higher than the sensed add pH up
			chemical_type = 'ph_up'
			chemical_quantity = spa_volume_gal * abs(error) * ph_gain

			return chemical_type, chemical_quantity
		elif error < 0:
			# the error is < 0, the desired is less than the sensed, add pH down
			chemical_type = 'ph_down'
			chemical_quantity = spa_volume_gal * abs(error) * ph_gain

			return chemical_type, chemical_quantity
	else:
		log.error("System not calibrated to release %s" % chemical)

	# by default return chemical type None with quantity 0 grams
	return None, 0
