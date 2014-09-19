import os
import time
import numpy as np

class Transmitter:
	# variables
	major = 0
	minor = 0
	xy_pos = (0,0)
	power = 0

	def __init__(self, pos, major, minor):
		self.major = major
		self.minor = minor
		self.xy = pos

	def getMajor(self):
		return self.major

	def getMinor(self):
		return self.minor

	def getPos(self):
		return self.xy

	def getDistanceTo(self,xy):
		return np.sqrt( (xy[0] - self.xy[0])**2 + (xy[1] - self.xy[1])**2 )

	def __str__(self):
		return "Transmitter at (%.1f, %.1f) with major (%d) and minor (%d)" % \
				(self.xy[0], self.xy[1], self.major, self.minor)

