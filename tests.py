"""@module tests
Unit testing framework for SmartSpa develop

Author: Josh Rands
Date: 2/23/2020 
Email: joshrands1@gmail.com
"""

import unittest 

import init 
from sensing_playground import interpolate_rgb_values
from sensing import interpolate_chemical_property_from_img_rgb, interpolate_chemical_property_from_img_linear
from sensing import get_average_rgb_from_img, get_img, visualize, get_scale_map
from sensing import Metric
from helpers import running_on_rpi

# Global parameters
visualize_fails = True
test_accuracy = None
chemical_property = None

class TestTesting(unittest.TestCase):

	def test_equal(self):
		self.assertEqual(True, True)


class TestSensingHardware(unittest.TestCase):

	def setUpClass():
		arg_vals = init.get_args()

		init.init(arg_vals['verbose'])

	def test_reagent_solenoid_valve(self):
		pass


class TestSensingPh(unittest.TestCase):

	def setUpClass():
		global chemical_property 
		global test_accuracy
		chemical_property = 'pH'
		test_accuracy = 0.2

	def run_test(self, test_value, image_file):
		global chemical_property 

		test_file = 'unit/' + chemical_property + '/' + image_file
		img = get_img('file', test_file)
		value = interpolate_chemical_property_from_img_linear(chemical_property, img, Metric.HUE)

		print("[TEST]: Testing %f = %f" % (value, test_value))

		try:
			self.assertLess(abs(value - test_value), test_accuracy)
		except Exception:
			if visualize_fails:
				r,g,b = get_average_rgb_from_img(img)
				scale = get_scale_map(chemical_property)
				visualize([r,g,b], scale)

		return abs(value - test_value)

	def test_6_9(self):
		test_value = 6.9
		file_name = '6,9.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_7_2(self):
		test_value = 7.2 
		file_name = '7,2.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_7_5(self):
		test_value = 7.5 
		file_name = '7,5.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_7_6(self):
		test_value = 7.6 
		file_name = '7,6.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_7_9(self):
		test_value = 7.9 
		file_name = '7,9.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_7_35(self):
		test_value = 7.35 
		file_name = '7,35.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)


class TestSensingCl(unittest.TestCase):

	def setUpClass():
		global chemical_property 
		global test_accuracy
		chemical_property = 'Cl'
		test_accuracy = 0.5

	def run_test(self, test_value, image_file):
		global chemical_property 

		test_file = 'unit/' + chemical_property + '/' + image_file
		img = get_img('file', test_file)
		value = interpolate_chemical_property_from_img_rgb(chemical_property, img)

		print("[TEST]: Testing %f = %f" % (value, test_value))

		try:
			self.assertLess(abs(value - test_value), test_accuracy)
		except Exception:
			if visualize_fails:
				r,g,b = get_average_rgb_from_img(img)
				scale = get_scale_map(chemical_property)
				visualize([r,g,b], scale)

		return abs(value - test_value)

	def test_1_0(self):
		test_value = 1.0 
		file_name = '1,0.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_0_5(self):
		test_value = 0.5 
		file_name = '0,5.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_2_0(self):
		test_value = 2.0 
		file_name = '2,0.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_3_0(self):
		test_value = 3.0 
		file_name = '3,0.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_5_0(self):
		test_value = 5.0 
		file_name = '5,0.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)


class TestSensingCl_img(unittest.TestCase):

	def setUpClass():
		global chemical_property 
		global test_accuracy
		chemical_property = 'Cl_img' # currently testing Cl_img until a better picture is taken
		test_accuracy = 0.2

	def run_test(self, test_value, image_file):
		global chemical_property 

		test_file = 'unit/' + chemical_property + '/' + image_file
		img = get_img('file', test_file)
		value = interpolate_chemical_property_from_img_linear(chemical_property, img, Metric.SAT)

		print("[TEST]: Testing %f = %f" % (value, test_value))

		try:
			self.assertLess(abs(value - test_value), test_accuracy)
		except Exception:
			if visualize_fails:
				r,g,b = get_average_rgb_from_img(img)
				scale = get_scale_map(chemical_property)
				visualize([r,g,b], scale)

		return abs(value - test_value)

	def test_0_2(self):
		test_value = 0.2 
		file_name = '0,2.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_0_6(self):
		test_value = 0.6 
		file_name = '0,6.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_1_0(self):
		test_value = 1 
		file_name = '1,0.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_1_5(self):
		test_value = 1.5
		file_name = '1,5.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_3_0(self):
		test_value = 3 
		file_name = '3,0.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)
	

if __name__ == '__main__':
	arg_vals = init.get_args()

	init.init(arg_vals['verbose'])

	unittest.main()
		