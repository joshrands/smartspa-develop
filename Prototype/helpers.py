# helpers.py
# functions to help other files
import cv2
import os

def getRGBOfImage(image_path):
	img = cv2.imread(image_path)

	total_blue = 0
	total_green = 0
	total_red = 0
	for i in range(0, len(img)):
			for j in range(0, len(img[i])):
					total_blue += img[i,j][0]
					total_green += img[i,j][1]
					total_red += img[i,j][2]

	b = total_blue / (len(img) * len(img))
	g = total_green / (len(img) * len(img))
	r = total_red / (len(img) * len(img))

	return r,g,b

def getScaleMap(scale_name):
	in_file = open(scale_name + "-config.csv","r")

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

import numpy as np
def getDistanceBetweenPoints(x,y):
	squared_dist = np.sum((np.array(x) - np.array(y))**2, axis=0)
	dist = np.sqrt(squared_dist)
	return dist

