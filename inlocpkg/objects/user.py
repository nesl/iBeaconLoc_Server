# IMPORTS
import time
from ..constants import parameters

class User:

	def __init__(self,uid,estimator):
		self.uid = uid
		self.estimator = estimator
		self.lastEstimateTime = time.time()
		# default state
		self.powerFilter = parameters.TXPOW_HIGH
		self.rateThrottle = 10

		# constants
		self.MAX_EST_HISTORY_LEN = 64
		self.MAX_BEACON_CACHE_LEN = 256
		# dynamic variables
		self.xy_history = []
		self.time_history = []
		self.beacon_cache = []
		# mobile-based filters
		self.powerFilter = -74
		self.rateThrottle = 20
		# reception statistics
		self.packetsPerSec = 0
		self.lastEstimateTime = 0

	def getUid(self):
		return self.uid

	def getPosEstimate(self):
		if len(self.xy_history) == 0:
			return (0.0,0.0)
		return self.xy_history[-1]

	def getPathEstimate(self, numpoints):
		if len(self.xy_history) == 0:
			return None
		if numpoints >= len(self.xy_history):
			return (self.xy_history, self.time_history)
		else:
			return (self.xy_history[-numpoints:], self.time_history[-numpoints:])

	def logBeaconRecord(self, beacon):
		self.beacon_cache.append(beacon)

		if len(self.beacon_cache) > self.MAX_BEACON_CACHE_LEN:
			self.beacon_cache.pop(0)

	def addPosEstimate(self, xy_new):
		self.xy_history.append(xy_new)
		self.time_history.append(time.time())

		if len(self.xy_history) > self.MAX_EST_HISTORY_LEN:
			self.xy_history.pop(0)
			self.time_history.pop(0)

	def estimateNewPosition(self):
		timeSinceLastEst = time.time() - self.lastEstimateTime
		xy_new = self.estimator.getNextEstimate(self)
		if xy_new is not None:
			self.addPosEstimate(xy_new)
		# update packets per sec stat
		self.packetsPerSec = len(self.beacon_cache)/timeSinceLastEst
		# clear cached beacons
		self.beacon_cache = []
		self.lastEstimateTime = time.time()

	def setPowerFilter(self, power):
		self.powerFilter = power

	def setRateThrottle(self, rate):
		self.rateThrottle = rate

	def getPowerFilter(self):
		return self.powerFilter

	def getRateThrottle(self):
		return self.rateThrottle

	def getPacketsPerSec(self):
		return self.packetsPerSec


	def __str__(self):
		return "User %d" % (self.uid)