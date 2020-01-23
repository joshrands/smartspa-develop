# helpers.py
# functions to help other files
import cv2
import os
import numpy as np
import time

from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

def getRGBOfImage(image_path, vis=False, num_deviations=2):
	if (num_deviations == None):
		num_deviations = 2

	img = cv2.imread(image_path)

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
					b.append(img[i,j][0])
					g.append(img[i,j][1])
					r.append(img[i,j][2])

	outlier = True
	clean_r = r
	clean_g = g
	clean_b = b
	while outlier:
		print("Cleaning input image...")

		# look at data of image
		r_mean = np.mean(np.array(clean_r))
		r_std = np.std(np.array(clean_r))
		g_mean = np.mean(np.array(clean_g))
		g_std = np.std(np.array(clean_g))
		b_mean = np.mean(np.array(clean_b))
		b_std = np.std(np.array(clean_b))

		print("Red: mu=" + str(r_mean) + ", sigma=" + str(r_std))
		print("Green: mu=" + str(g_mean) + ", sigma=" + str(g_std))
		print("Blue: mu=" + str(b_mean) + ", sigma=" + str(b_std))

		outlier = False
		new_r = []
		new_g = []
		new_b = []
		for i in range(0, len(clean_r)):
			if (abs(clean_r[i] - r_mean) > num_deviations * r_std) or (abs(clean_g[i] - g_mean) > num_deviations*g_std) or (abs(clean_b[i] - b_mean) > num_deviations*b_std):
				outlier = True
#				clean_r.append(r_mean)
			else:
				new_r.append(clean_r[i])
				new_g.append(clean_g[i])
				new_b.append(clean_b[i])

		clean_r = new_r
		clean_g = new_g
		clean_b = new_b
	
	# look at 3d plot of points 
	if vis:
		fig = pyplot.figure()
		ax = Axes3D(fig)
		ax.scatter(r,g,b,color="blue")

		pyplot.show()	

		fig = pyplot.figure()
		ax = Axes3D(fig)
		ax.scatter(clean_r,clean_g,clean_b,color="red")
		pyplot.show()	

#	b = total_blue / (len(img) * len(img))
#	g = total_green / (len(img) * len(img))
#	r = total_red / (len(img) * len(img))

	# used cleaned image
	r = r_mean
	g = g_mean
	b = b_mean

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


def getDistanceBetweenPoints(x,y):
	squared_dist = np.sum((np.array(x) - np.array(y))**2, axis=0)
	dist = np.sqrt(squared_dist)
	return dist

