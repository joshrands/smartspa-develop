"""@module tests
Unit testing framework for SmartSpa develop

Author: Josh Rands
Date: 2/23/2020 
Email: joshrands1@gmail.com
"""

import unittest 

import init 
from sensing_playground import interpolate_rgb_values
from sensing import get_img, interpolate_chemical_property_from_img_rgb, visualize, get_average_rgb_from_img, get_scale_map, interpolate_chemical_property_from_img_hue

test_accuracy = 0.2
visualize_fails = True

class TestTesting(unittest.TestCase):

	def test_equal(self):
		self.assertEqual(True, True)

	def test_not_equal(self):
		self.assertNotEqual(True, False)


class TestSensingPh(unittest.TestCase):

	def setUpClass():
		arg_vals = init.get_args()

		init.init(arg_vals['verbose'])

	def run_test(self, test_value, test_file):
		img = get_img('file', test_file) 
		value = interpolate_chemical_property_from_img_hue('pH', img)

		print("[TEST]: Testing %f = %f" % (value, test_value))

		try:
			self.assertLess(abs(value - test_value), test_accuracy)
		except Exception:
			if visualize_fails:
				r,g,b = get_average_rgb_from_img(img)
				scale = get_scale_map('pH')
				visualize([r,g,b], scale)

		return abs(value - test_value)

	def test_6_9(self):
		test_value = 6.9
		file_name = 'unit/6,9.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_7_2(self):
		test_value = 7.2 
		file_name = 'unit/7,2.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_7_5(self):
		test_value = 7.5 
		file_name = 'unit/7,5.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_7_6(self):
		test_value = 7.6 
		file_name = 'unit/7,6.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_7_9(self):
		test_value = 7.9 
		file_name = 'unit/7,9.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)

	def test_7_35(self):
		test_value = 7.35 
		file_name = 'unit/7,35.png'
		self.assertLess(self.run_test(test_value, file_name), test_accuracy)


if __name__ == '__main__':
	unittest.main()
