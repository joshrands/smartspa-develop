"""@package sensing
Perform SmartSpa chemical level sensing 
 
This module performs chemical level sensing by releasing a reagent into the mixing container,
driving a stirring motor. 
 
Author: Josh Rands
Date: 2/3/2020 
Email: joshrands1@gmail.com
"""

import logging as log
import matplotlib.image as image
import matplotlib.pyplot as plt
import numpy as np
from os import path
import pygame
import pygame.camera

import init
from helpers import get_distance_between_points_3d

def get_error(chemical, vis=False):
	"""Get the error for a given chemical 
	"""

	prepare_sample()

	img = get_img()

	if None == img.any():
		log.error("Invalid image.")
		return None

	r,g,b = get_average_rgb_from_img(img)

	scale = get_scale_map(chemical)

	if vis:
		visualize([r,g,b], scale)

	# get the distance from each point in the scale 
	closest = 255
	closest_key = ""
	for key in scale:
		rgb = scale[key]
		dist = get_distance_between_points_3d(rgb, [r,g,b])

		if dist < closest:
			closest = dist
			closest_key = key

	print("Closest to: %s" % closest_key)

	return dist


def prepare_sample():
	"""Prepare the sample by mixing the reagent in the sample tube.
	"""

	log.warning("Sample not prepared.")


def get_img():
	"""Return a 2-dimensional array of rgb pixels.
	"""	

	source = init.sensing_config.data['image_source'] 
	width = init.sensing_config.data['img_width']
	height = init.sensing_config.data['img_height']

	if source == 'file':
		log.info("Getting image from file.")

		image_file = input("Enter image name: ")
		img = image.imread("test/" + image_file)
		# save image to sample.png for debugging	
		image.imsave('raw-sample.png', img)

		return img

	elif source == 'usb':
		log.info("Getting image from camera.")
		cam_id = init.sensing_config.data['camera_id']

		pygame.camera.init()
		pygame.camera.list_cameras() #Camera detected or not
		cam = pygame.camera.Camera("/dev/video" + str(cam_id))
		cam.start()
		img = cam.get_image()
		img = pygame.transform.scale(img, (width, height))
		pixels = pygame.surfarray.array3d(img)
		pygame.image.save(img,"raw-sample.png")
		cam.stop()

		return pixels

	elif source == 'rpi':
		log.info("Getting image from RPi camera.")
		log.warning("RPi camera not implemented.")

	else:
		log.error("Invalid image source.")

	return None


def get_average_rgb_from_img(img):
	"""Clean the image 2-dimensional array into single rgb values.
	"""
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

	return scale


def visualize(rgb, scale):
	"""Visualize the scale and the final reading.
	"""

	log.warning("Visualize not implemented.")


