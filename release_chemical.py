"""@module release_chemical
Release chemicals into the system.
 
Author: Josh Rands
Date: 2/5/2020 
Email: joshrands1@gmail.com
"""

import logging as log
import time

import init 
from hardware_iface import open_chemical_dispensing_doors, close_chemical_dispensing_doors, spin_chemical_release_auger, stop_chemical_release_auger

def release_chemical(chemical_type, chemical_quantity_grams):
    log.info("Releasing %d grams of %s" % (chemical_quantity_grams, chemical_type))

    # open chemical dispensing doors using servo 
    open_chemical_dispensing_doors()

    # drive auger to release chemicals 
    spin_chemical_release_auger()

    # wait time to release chemical_quantity_grams 
    release_gain = init.control_config.data['chemical_release_gain']

    wait_time = release_gain
    log.info("Waiting %d seconds to release %d grams of %s" % (wait_time, chemical_quantity_grams, chemical_type))
    time.sleep(release_gain)

    # stop auger to stop releasing chemicals 
    stop_chemical_release_auger()

    # close dispensing door to separate chemicals from water 
    close_chemical_dispensing_doors()

    # the chemicals are properly mixed outside of this function.
