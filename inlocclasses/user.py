class User:
	# variables
	identifier = ''
	xy_est = (0,0)


	def __init__(self,ident):
		self.identifier = ident

	def getID(self):
		return self.identifier

	def getPosEstimate(self):
		return self.xy_est

	def __str__(self):
		return "User (%d) at (%.1f, %.1f)" % (self.identifier, self.xy_est[0], self.xy_est[1])