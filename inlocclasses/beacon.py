import os
import time

class Beacon:
	# variables
	major = 0
	minor = 0
	rssi = 0
	time = 0

	def __init__(self, major, minor, power):
		self.major = major
		self.minor = minor
		self.rssi = power
		# time this beacon was received
		self.time = time.time()

	def getMajor(self):
		return self.major

	def getMinor(self):
		return self.minor

	def getRssi(self):
		return self.rssi

	def getTime(self):
		return self.time

	def __str__(self):
		return "Beacon from major (%d) and minor (%d) with RSSI (%d) @ t=%f" % \
				(self.major, self.minor, self.rssi, self.time)

