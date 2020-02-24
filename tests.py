"""@module tests
Unit testing framework for SmartSpa develop

Author: Josh Rands
Date: 2/23/2020 
Email: joshrands1@gmail.com
"""

import unittest 

class TestTesting(unittest.TestCase):

	def test_equal(self):
		self.assertEqual(True, True)

	def test_not_equal(self):
		self.assertNotEqual(True, False)


if __name__ == '__main__':
	unittest.main()
