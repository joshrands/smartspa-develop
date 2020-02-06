"""@module helpers
Python helper functions for performing tedious work.
 
Author: Josh Rands
Date: 2/3/2020 
Email: joshrands1@gmail.com
"""

import xml.etree.ElementTree as ET
import logging as log
import numpy as np
import os.path as path

def parse_xml(file_name):
	"""Parse an xml file into a python dictionary
	"""

	root = ET.parse(file_name).getroot()

	data = {}

	count = 0
	for child in root:

		if (root[count].text == 'true'):
			data[child.tag] = True
		elif (root[count].text == 'false'):
			data[child.tag] = False 
		elif (True == (root[count].text).isdigit()):
			data[child.tag] = int(root[count].text)
		elif (root[count].text == 'None'):
			data[child.tag] = None
		else:	
			data[child.tag] = root[count].text	

	
		count += 1

	return data


def get_distance_between_points_3d(x, y):
	"""Get the 3-dimensional distance between these two points
	"""
	squared_dist = np.sum((np.array(x) - np.array(y))**2, axis=0)
	dist = np.sqrt(squared_dist)

	return dist


def running_on_rpi():
	if path.exists('/proc/cpuinfo'):
		# read file and look at model 
		info_file = open("/proc/cpuinfo")
		lines = info_file.readlines()

		for line in lines:
			if line.__contains__("Raspberry"):
				return True

	return False
