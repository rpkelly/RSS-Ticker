import os
import sys
import gzip
import random
import unittest
sys.path.insert(0,"../src")
import optionsModel

class TestOptionsModel(unittest.TestCase):
	def setUp(self):
		self.model = optionsModel.OptionsModel()
		self.assertTrue(self.model.getSpeed() == 50)
		self.assertTrue(self.model.getSync() == 3600)
		self.assertTrue(not self.model.getStop())
		self.assertTrue(self.model.getLaunch())
		self.assertTrue(self.model.getLeft())
	def testURL(self):
		l = []
		l.append("cat")
		self.model.getURLs().append("cat")
		self.assertTrue(self.model.getURLs() == l)

	def testLeft(self):
		self.model.setLeft(0)
		self.assertTrue(self.model.getLeft() == 0)

	def testLaunch(self):
		self.model.setLaunch(0)
		self.assertTrue(self.model.getLaunch() == 0)

	def testStop(self):
		self.model.setStop(1)
		self.assertTrue(self.model.getStop() == 1)

	def testSync(self):
		self.model.setSync(0)
		self.assertTrue(self.model.getSync() == 0)

	def testSpeed(self):
		self.model.setSpeed(50)
		self.assertTrue(self.model.getSpeed() == 50)
		self.model.setSpeed(150)
		self.assertTrue(self.model.getSpeed() == 100)
		self.model.setSpeed(-50)
		self.assertTrue(self.model.getSpeed() == 0)

if __name__ == "__main__":
	unittest.main()
