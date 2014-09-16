import os
import time
import numpy as np

class Transmitter:
	# variables
	major = 0
	minor = 0
	xy_pos = (0,0)
	power = 0

	def __init__(self, pos, major, minor, power):
		self.major = major
		self.minor = minor
		self.power = power
		self.xy = pos

	def getMajor(self):
		return self.major

	def getMinor(self):
		return self.minor

	def getPower(self):
		return self.power

	def getPos(self):
		return self.xy

	def getDistanceTo(self,xy):
		return np.sqrt( (xy[0] - self.xy[0])**2 + (xy[1] - self.xy[1])**2 )

	def __str__(self):
		return "Transmitter at (%.1f, %.1f) with Power at (%d), major (%d), and minor (%d)" % \
				(self.xy_pos[0], self.xy_pos[1], self.power, self.major, self.minor)

