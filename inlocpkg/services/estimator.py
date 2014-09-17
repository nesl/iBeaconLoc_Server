# IMPORTS
import numpy
from numpy import linalg
from scipy.optimize import leastsq
#from pylab import *


# Rx power vs. distance model
def rxPowerToDistance(txpow,rxpow):
	p0 = 83
	p1 = 2.7
	return pow(10, -(rxpow + p0)/(10*p1) )

class PositionEstimator(object):
	# estimation variables
	weightingExponent = 0
	lowPassCoeff = 0
	# additional variables
	iBeaconList = None

	def __init__(self, iBeaconList, weighting_exponent=0, lowpassCoeff=0):
		self.iBeaconList = iBeaconList
		self.weighting_exponent = weighting_exponent
		self.lowpassCoeff = lowpassCoeff

	def getNextEstimate(self, user):
		# if the user's beacon cache is empty, we can't do anything
		if len(user.beacon_cache) == 0:
			return
		# if the user does have cached beacons, we'll average the ones from the same transmitters
		observedBeacons = {}
		for b in user.beacon_cache:
			MajMin = ( b.getMajor(), b.getMinor() )
			if MajMin not in observedBeacons:
				observedBeacons[MajMin] = b
			else:
				# running average of RSSI
				observedBeacons[MajMin].avgRssi(b.getRssi())
		# make sure we have enough unique beacons to get a good new estimate
		if len(observedBeacons) < 3:
			return

		# our first guess can be the middle of all observed beacons
		xy_observedBeacons = [self.iBeaconList[(major,minor)].xy for (major,minor) in observedBeacons]
		xy_guess = (numpy.mean([x for x,y in xy_observedBeacons]), numpy.mean([y for x,y in xy_observedBeacons]))
		# Now we'll find the instantaneous estimation based on the cached beacon information
		xy_inst = leastsq(self.lsqrError, xy_guess, args=(observedBeacons))
		return (xy_inst[0][0], xy_inst[0][1])
		
	def lsqrError(self, xy, observedBeacons):
		# calculate the proposed distances to the beacons
		proposedBeaconDistances = {(major,minor):self.iBeaconList[(major,minor)].getDistanceTo(xy)\
									 for (major,minor) in observedBeacons}
		# calculate the measured distances to the beacons based on RSSI
		measuredBeaconDistances = {(major,minor):observedBeacons[(major,minor)].getDistEst()\
									for (major,minor) in observedBeacons}
		# calculate difference between measured and proposed distances
		differences = [proposedBeaconDistances[(major,minor)]-measuredBeaconDistances[(major,minor)]\
									for (major,minor) in observedBeacons]
		return differences
