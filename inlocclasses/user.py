class User:
	# variables
	identifier = ''
	xy_history = []
	time_history = []
	beacon_history = []
	MAX_EST_HISTORY_LEN = 64
	MAX_BEACON_HISTORY_LEN = 256


	def __init__(self,ident):
		self.identifier = ident

	def getID(self):
		return self.identifier

	def getPosEstimate(self):
		if len(self.xy_history) == 0:
			return None
		return (self.xy_history[-1], self.time_history[-1])

	def getPathEstimate(self, numpoints):
		if len(self.xy_history) == 0:
			return None
		if numpoints >= len(self.xy_history):
			return (self.xy_history, self.time_history)
		else:
			return (self.xy_history[-numpoints:], self.time_history[-numpoints:])

	def addPosEstimate(self, xy_new, time):
		self.xy_history.append(xy_new)
		self.time_history.append(time)

		if len(self.xy_history) > self.MAX_EST_HISTORY_LEN:
			self.xy_history.pop()
			self.time_history.pop()

	def logBeaconRecord(self, beacon):
		self.beacon_history.append(beacon)

		if len(self.beacon_history) > MAX_BEACON_HISTORY_LEN:
			self.beacon_history.pop()


	def __str__(self):
		return "User %s" % (self.identifier)