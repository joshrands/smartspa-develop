"""@package sensing
Perform SmartSpa chemical level sensing 
 
This module performs chemical level sensing by releasing a reagent into the mixing container,
driving a stirring motor. 
 
Author: Josh Rands
Date: 2/3/2020 
Email: joshrands1@gmail.com
"""

from init import sensing_config

def get_chemical_reading(scale):
	"""Get a chemical reading from the given scale.
	"""

	img = get_img()

	r,g,b = get_average_rgb_from_img(img)

	scale = get_scale_map(scale)

	pass


def get_img():
	"""Return a 2-dimensional array of rgb pixels.
	"""	

	pass


def get_average_rgb_from_img(img):
	"""Clean the image 2-dimensional array into single rgb values.
	"""

	pass


def get_scale_map(scale):
	"""Return a dictionary of values to average rgb.
	"""

	pass




