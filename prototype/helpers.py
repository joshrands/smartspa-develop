"""@package helpers
Python helper functions for performing tedious work.
 
Author: Josh Rands
Date: 2/3/2020 
Email: joshrands1@gmail.com
"""

import xml.etree.ElementTree as ET
import logging as log


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
		else:	
			data[child.tag] = root[count].text	

	
		count += 1

	return data


