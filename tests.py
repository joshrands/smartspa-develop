"""@module tests
Unit testing framework for SmartSpa develop

Author: Josh Rands
Date: 2/23/2020 
Email: joshrands1@gmail.com
"""

import unittest 
from statistics import mean

import init 
from sensing_playground import interpolate_rgb_values
from sensing import interpolate_chemical_property_from_img_rgb, interpolate_chemical_property_from_img_linear
from sensing import get_average_rgb_from_img, get_img, visualize, get_scale_map
from sensing import Metric
from helpers import running_on_rpi

# Global parameters
visualize_fails = False
test_accuracy = None
chemical_property = None
interpolation_metric = None

class TestTesting(unittest.TestCase):

	def test_equal(self):
		self.assertEqual(True, True)


class TestSensingHardware(unittest.TestCase):

	def setUpClass():
		arg_vals = init.get_args()

		init.init(arg_vals['verbose'])

	def test_reagent_solenoid_valve(self):
		pass


class TestSensingProperty(unittest.TestCase):

	results = {} 
	errors = []

	@classmethod
	def tearDownClass(self):
		""" Write testing results to a file 
		"""

		print("Average error of " + chemical_property + " = " + str(mean(self.errors)))

		out_file = open("testing/" + chemical_property + "_results.txt","w") 

		out_file.write(chemical_property + " Test Results\n")
		out_file.write("average_error=" + str(mean(self.errors)) + "\n")

		# write predictions 
		out_file.write("actual=predicted\n")
		for key in self.results.keys():
			out_file.write("\t" + str(key) + "=" + str(self.results[key]) + "\n")

		out_file.close()

	def run_test(self, test_value, image_file):
		global chemical_property 
		global interpolation_metric

		test_file = 'unit/' + chemical_property + '/' + image_file
		img = get_img('file', test_file)

		value = None

		if interpolation_metric == Metric.RGB:
			value = interpolate_chemical_property_from_img_rgb(chemical_property, img)
		else:
			value = interpolate_chemical_property_from_img_linear(chemical_property, img, interpolation_metric)

		print("[TEST]: Testing %f = %f" % (value, test_value))

		try:
			self.errors.append(abs(value - test_value))
			self.results[test_value] = value
			self.assertLess(abs(value - test_value), test_accuracy)
		except Exception:
			if visualize_fails:
				r,g,b = get_average_rgb_from_img(img)
				scale = get_scale_map(chemical_property)
				visualize([r,g,b], scale)

		return abs(value - test_value)

class TestSensingPh(TestSensingProperty):

	def setUpClass():
		global chemical_property 
		global test_accuracy
		global interpolation_metric
		chemical_property = 'pH'
		test_accuracy = 0.2
		interpolation_metric = Metric.HUE

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


class TestSensingCl(TestSensingProperty):

	def setUpClass():
		global chemical_property 
		global test_accuracy
		global interpolation_metric
		chemical_property = 'Cl'
		test_accuracy = 0.5
		interpolation_metric = Metric.RGB

	"""
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
	"""

class TestSensingCl_img(TestSensingProperty):

	def setUpClass():
		global chemical_property 
		global test_accuracy
		global interpolation_metric
		chemical_property = 'Cl_img' # currently testing Cl_img until a better picture is taken
		test_accuracy = 0.25
		interpolation_metric = Metric.SAT

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
		