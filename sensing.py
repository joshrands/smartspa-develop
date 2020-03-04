"""@module sensing
Perform SmartSpa chemical level sensing 
 
This module performs chemical level sensing by releasing a reagent into the mixing container,
driving a stirring motor. 
 
Author: Josh Rands
Date: 2/3/2020 
Email: joshrands1@gmail.com
"""

import time
import logging as log
import matplotlib.image as image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from os import path
import numpy.linalg as linalg
import colorsys

import init
from helpers import get_distance_between_points_3d, running_on_rpi

if running_on_rpi():
	import RPi.GPIO as GPIO
	import picamera
	import picamera.array
else:
    import pygame
    import pygame.camera


def interpolate_chemical_property_from_img_hue(chemical, img):
	""" Interpolate the value of a chemical property using
	linear interpolation from the scale and the hue of each image.
	"""

	r,g,b = get_average_rgb_from_img(img)
	
	scale = get_scale_map(chemical)

	# convert r,g,b to h,s,v 
	h,s,v = colorsys.rgb_to_hsv(r,g,b)

	if h > 0.5:
		h -= 1

	# get the distance from each point in the scale (converted to a hue)
	sorted_keys = sorted(scale.keys())
	distances = []
	hues = []

	for key in sorted_keys:
		rgb = scale[key]
		hue,sat,val = colorsys.rgb_to_hsv(*(rgb))

		if hue > 0.5:
			hue -= 1

		dist = abs(h - hue)
		distances.append(dist)
		hues.append(hue)

	closest_index = distances.index(min(distances))

	# interpolate 
	# if we are the lowest index in the example scale, figure out if it is less than lowest
	# or inbetween lowest and second lowest 
	if (0 == closest_index):

		if (distances[0] < distances[1]):
			# we are less than minimum
			log.warning("Value outside of scale range.")

		low_index = 0
		high_index = 1
	elif (len(sorted_keys) - 1 == closest_index):
		low_index = len(sorted_keys) - 2
		high_index = closest_index
	else:
		# check high and low 
		low_distance = distances[closest_index - 1]
		high_distance = distances[closest_index + 1]
		if (low_distance < high_distance):
			low_index = closest_index - 1
			high_index = closest_index
		else:
			low_index = closest_index
			high_index = closest_index + 1

	# interpolate the new value 
	high_hue,_,_ = colorsys.rgb_to_hsv(*(scale[sorted_keys[high_index]]))
	low_hue,_,_ = colorsys.rgb_to_hsv(*(scale[sorted_keys[low_index]]))

	h_distance = high_hue - h
	low_distance = high_hue - low_hue

	ratio = h_distance / low_distance

	# get the difference between high and low chemical property 
	range_difference = float(sorted_keys[high_index]) - float(sorted_keys[low_index])

	interpolated_value = float(sorted_keys[high_index]) - range_difference * ratio

	return interpolated_value


def interpolate_chemical_property_from_img_rgb(chemical, img):
	""" Interpolate the value of a chemical property using the 
	rgb values of the scale images. This is done by linearly interpolating
	between the values in 3D space after projecting the point 
	in question onto the closest line segment. 
	"""

	r,g,b = get_average_rgb_from_img(img)

	scale = get_scale_map(chemical)

	# get the distance from each point in the scale 
	sorted_keys = sorted(scale.keys())
	distances = []

	for key in sorted_keys:
		rgb = scale[key]
		dist = get_distance_between_points_3d(rgb, [r,g,b])

		distances.append(dist)

	# find the closest r,g,b value 
	closest_index = distances.index(min(distances))
	log.info("Closest to " + sorted_keys[closest_index])

	# find if high or low is closer 
	low_index = 0
	high_index = 0

	# if we are the lowest index in the example scale, figure out if it is less than lowest
	# or inbetween lowest and second lowest 
	if (0 == closest_index):

		if (distances[0] < distances[1]):
			# we are less than minimum
			log.warning("Value outside of scale range.")

		low_index = 0
		high_index = 1
	elif (len(sorted_keys) - 1 == closest_index):
		low_index = len(sorted_keys) - 2
		high_index = closest_index
	else:
		# check high and low 
		low_distance = distances[closest_index - 1]
		high_distance = distances[closest_index + 1]
		if (low_distance < high_distance):
			low_index = closest_index - 1
			high_index = closest_index
		else:
			low_index = closest_index
			high_index = closest_index + 1

	log.info("High: %s, Low: %s" % (sorted_keys[high_index], sorted_keys[low_index]))

	# interpolate the new value 
	# 1. Derive the vector between low and high index 
	high_rgb = scale[sorted_keys[high_index]]
	low_rgb = scale[sorted_keys[low_index]]

	vector = [high_rgb[0] - low_rgb[0], high_rgb[1] - low_rgb[1], high_rgb[2] - low_rgb[2]]

	# 2. Convert vector to unit vector 
	unit_vector = vector / linalg.norm(vector)

	# 3. Get projected r,g,b from unit vector dot product ((x,y,z).(a,b,c)*(a,b,c))
	projected_rgb = (unit_vector[0]*r + unit_vector[1]*g + unit_vector[2]*b)*np.asarray([r,g,b])

	# 4. Interpolate the chemical from the interpolated r,g,b
	# get the distance from the high_rgb 
	distance = get_distance_between_points_3d(high_rgb, projected_rgb)
	
	# get the difference between high and low chemical property 
	range_difference = float(sorted_keys[high_index]) - float(sorted_keys[low_index])

	interpolated_value = float(sorted_keys[low_index]) + range_difference * distance

	return interpolated_value


def set_sample_led(light_on, LED_PIN):
	"""Turn on the LEDs surrounding the sample so a picture can be taken
	"""

	if running_on_rpi():
		if None != LED_PIN:
			# light_on = True will turn on LED, False will turn off
			log.info("Setting sample LED to " + str(light_on))
			GPIO.output(LED_PIN, light_on)
		else:
			log.error("LED pin set to None.")
	else:
		log.error("Not running on RPi")


def get_img(source, file_name=None):
	"""Return a 2-dimensional array of rgb pixels.
	"""	

	width = init.sensing_config.data['img_width']
	height = init.sensing_config.data['img_height']

	if source == 'file':
		log.info("Getting image from file.")

		if None == file_name: 
			file_name = input("Enter image name: ")

		img = image.imread("imgs/" + file_name)
		# save image to sample.png for debugging	
		image.imsave('raw-sample.png', img)

		return img

	elif source == 'usb':
		log.info("Getting image from camera.")
		cam_id = init.sensing_config.data['camera_id']

		pygame.camera.init()
		pygame.camera.list_cameras() 
		cam = pygame.camera.Camera("/dev/video" + str(cam_id))
		cam.start()

		# Take the picture
		init.hardware.set_pin('sensing_led', True)
		img = cam.get_image()
		init.hardware.set_pin('sensing_led', False)

		img = pygame.transform.scale(img, (width, height))
		pixels = pygame.surfarray.array3d(img)
		pygame.image.save(img,"raw-sample.png")
		cam.stop()

		return pixels

	elif source == 'rpi':
		log.info("Getting image from RPi camera.")

		if running_on_rpi():
			with picamera.PiCamera() as camera:
				with picamera.array.PiRGBArray(camera) as stream:
					# Turn on LED 
					init.hardware.set_pin('sensing_led', True)

					# sleep to guarantee led is on...
					time.sleep(0.1)

					# adjust resolution for easier data processing 
					camera.resolution = (width, height)
					camera.capture(stream, format='rgb') # was 'bgr'
					# At this point the image is available as stream.array
					img = stream.array
					# save to file
					camera.capture('raw-sample.png')

					# Turn off LED 
					init.hardware.set_pin('sensing_led', False)

					return img
		else:
			log.error("Not running on RPi.")

	else:
		log.error("Invalid image source.")

	return None


def get_average_rgb_from_img(img):
	"""Clean the image 2-dimensional array into single rgb values.
	"""
	log.info("Cleaning image data...")

	num_deviations = init.sensing_config.data['std']

	total_blue = 0
	total_green = 0
	total_red = 0
	r = []
	g = []
	b = []
	for i in range(0, len(img)):
		for j in range(0, len(img[i])):
			total_blue += img[i,j][0]
			total_green += img[i,j][1]
			total_red += img[i,j][2]
			r.append(img[i,j][0])
			g.append(img[i,j][1])
			b.append(img[i,j][2])

	outlier = True
	clean_r = r
	clean_g = g
	clean_b = b
	while outlier:
    # look at data of image
		r_mean = np.mean(np.array(clean_r))
		r_std = np.std(np.array(clean_r))
		g_mean = np.mean(np.array(clean_g))
		g_std = np.std(np.array(clean_g))
		b_mean = np.mean(np.array(clean_b))
		b_std = np.std(np.array(clean_b))

		outlier = False
		new_r = []
		new_g = []
		new_b = []

		for i in range(0, len(clean_r)):
			if (abs(clean_r[i] - r_mean) > num_deviations * r_std) or (abs(clean_g[i] - g_mean) > num_deviations*g_std) or (abs(clean_b[i] - b_mean) > num_deviations*b_std):
				outlier = True
			else:
				new_r.append(clean_r[i])
				new_g.append(clean_g[i])
				new_b.append(clean_b[i])

		clean_r = new_r
		clean_g = new_g
		clean_b = new_b

	# standardize all output.
	if r_mean > 1 or g_mean > 1 or b_mean > 1:
		r_mean /= 255.0
		g_mean /= 255.0
		b_mean /= 255.0

	return r_mean, g_mean, b_mean 


def get_scale_map(chemical):
	"""Return a dictionary of values to average rgb.
	"""

	file_path = "calibrate/" + chemical + "/cal.csv"
	if not path.exists(file_path):
		log.error("No calibration exists for chemical: %s" % chemical)
		return

	in_file = open(file_path, 'r')

	lines = in_file.readlines()

	scale = {}
	for line in lines:
		split = line.split(',')
		rgb = (split[1][1:-2].split(' '))
		rgb[0] = float(rgb[0])
		rgb[1] = float(rgb[1])
		rgb[2] = float(rgb[2])
		scale[split[0]] = rgb

	in_file.close()

	return scale


def visualize(rgb, scale):
	"""Visualize the scale and the final reading.
	"""
	# 3D Plot
	fig = plt.figure()
	ax = Axes3D(fig)
    
	red = []
	green = []
	blue = []

    # turn keys into floats to sort 
	keys = sorted([float(val) for val in list(scale.keys())])
    # turn keys back into strings 
	keys = [str(val) for val in keys]
	previous_key = None 

	for key in keys: 

		if key == '0.0':
			key = '0'

		red.append(scale[key][0])
		green.append(scale[key][1])
		blue.append(scale[key][2])
		ax.text(red[-1],green[-1],blue[-1],key)

	red.append(rgb[0])
	green.append(rgb[1])
	blue.append(rgb[2])

	ax.scatter(red,green,blue)

	ax.set_xlabel("Red")
	ax.set_ylabel("Green")
	ax.set_zlabel("Blue")

	plt.show()


