# IMPORTS
import time

class User:
	# constants
	MAX_EST_HISTORY_LEN = 64
	MAX_BEACON_CACHE_LEN = 256
	# dynamic variables
	uid = -1
	xy_history = []
	time_history = []
	beacon_cache = []
	estimator = None
	# mobile-based filters
	powerFilter = 0
	rateThrottle = 0


	def __init__(self,uid,estimator):
		self.uid = uid
		self.estimator = estimator

	def getUid(self):
		return self.identifier

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
			self.beacon_cache.pop()

	def addPosEstimate(self, xy_new):
		self.xy_history.append(xy_new)
		self.time_history.append(time.time())

		if len(self.xy_history) > self.MAX_EST_HISTORY_LEN:
			self.xy_history.pop()
			self.time_history.pop()

	def estimateNewPosition(self):
		xy_new = self.estimator.getNextEstimate(self)
		if xy_new is not None:
			self.addPosEstimate(xy_new)
			# clear cached beacons
			self.beacon_cache = []

	def setPowerFilter(self, power):
		self.powerFilter = power

	def setRateThrottle(self, rate):
		self.rateThrottle = rate

	def getPowerFilter(self):
		return self.powerFilter

	def getRateThrottle(self):
		return self.rateThrottle


	def __str__(self):
		return "User %d" % (self.uid)