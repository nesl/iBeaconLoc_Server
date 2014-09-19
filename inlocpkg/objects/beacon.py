import os
import time
from ..services import *

class Beacon:
	# ibeacon variables
	major = 0
	minor = 0
	rssi = 0
	txpow = 0
	# reception variables
	time = 0
	rxnum = 1

	def __init__(self, major, minor, rssi, txpow):
		self.major = major
		self.minor = minor
		self.rssi = rssi
		self.txpow = txpow
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

	def avgRssi(self,newrssi):
		numold = self.rxnum
		numnew = numold+1
		self.rssi = self.rssi*(numold/numnew) + newrssi/numnew
		self.rxnum = numnew

	def getDistEst(self):
		return estimator.rxPowerToDistance(self.txpow, self.rssi)

	def __str__(self):
		return "Beacon from major (%d) and minor (%d) with RSSI (%d of %d), d_est = %.1f" % \
				(self.major, self.minor, self.rssi, self.txpow, self.getDistEst())

