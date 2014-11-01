# IMPORTS
import numpy
from numpy import linalg
from scipy.optimize import leastsq
#from pylab import *
from ..constants import parameters

# settings to power consumption estimation
def estimatePowerConsumption(beaconPower, beaconTxRate):
	idle_pow = 0.07e-3 # watts
	if beaconPower == parameters.TXPOW_LOW:
		tx_energy = 0.04e-3 # joules
	elif beaconPower == parameters.TXPOW_HIGH:
		tx_energy = 0.084e-3 # joules
	else:
		print('   WARNING: txpow unrecognized (' + str(beaconPower) +\
			  '), power est. may be inaccurate')
		tx_energy = 0.084e-3 # joules (default)

	# estimate power consumption (in Watts)
	pow_cons = idle_pow + beaconTxRate*tx_energy
	return pow_cons

def estimateLifetimeYears(batteryCapacity, powerConsumption):
	# capacity should be in Watt*Hours
	lifetime_hours = batteryCapacity/powerConsumption
	return lifetime_hours/(24.0*365.25)


# Rx power vs. distance model
def rxPowerToDistance(txpow,rxpow, id):
	# currently runs a switch case on txpow to switch models
	# =============== CLIENT 2 =================
	if id == 2:
		if txpow == parameters.TXPOW_LOW:
			p0 = -0.1086
			p1 = -9.00
			p2 = -0.3720
		elif txpow == parameters.TXPOW_HIGH:
			#p0 = -0.0873
			#p1 = -5.4624
			#p2 = -0.4738
			p0 = -0.0873
			p1 = -5.7200
			p2 = -0.4738
		else:
			print('   WARNING: txpow unrecognized (' + str(txpow) + \
				  '), model may be inaccurate')
			# default params (high):
			p0 = -0.0873
			p1 = -5.4624
			p2 = -0.4738
	else:
	# =============== CLIENT 1 =================
		if txpow == parameters.TXPOW_LOW:
			p0 = -0.1038
			p1 = -7.3010
			p2 = -0.7042
		elif txpow == parameters.TXPOW_HIGH:
			p0 = -0.0920
			p1 = -4.7989
			p2 = -0.2779
		else:
			print('   WARNING: txpow unrecognized (' + str(txpow) + \
				  '), model may be inaccurate')
			# default params (high):
			p0 = -0.0920
			p1 = -4.7989
			p2 = -0.2779

	dist_est = max(0.10, numpy.exp(p0*rxpow + p1) + p2)
	return dist_est

class PositionEstimator(object):

	def __init__(self, iBeaconList, weightingExponent=0, lowPassCoeff=0):
		self.iBeaconList = iBeaconList
		self.weighting_exponent = weightingExponent
		self.lowPassCoeff = lowPassCoeff

	def getNextEstimate(self, user):
		print(" --- User " + str(user.getUid()) + " getting new estimate: ---" )
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
		for MajMin in observedBeacons:
			#print("     >  " + str(observedBeacons[MajMin]))
			pass
		if len(observedBeacons) < 3:
			return

		# our first guess can be the middle of all observed beacons
		xy_observedBeacons = [self.iBeaconList[(major,minor)].xy for (major,minor) in observedBeacons]
		xy_guess = (numpy.mean([x for x,y in xy_observedBeacons]), numpy.mean([y for x,y in xy_observedBeacons]))
		# Now we'll find the instantaneous estimation based on the cached beacon information
		solution = leastsq(self.lsqrError, xy_guess, args=(observedBeacons))
		xy_inst = (solution[0][0], solution[0][1])
		

		# we got the instantaneous position, now let's do our low pass filter
		xy_filt = numpy.add( numpy.multiply(self.lowPassCoeff, user.getPosEstimate()),\
							 numpy.multiply((1-self.lowPassCoeff), xy_inst) )

		# ensure new location is within bounds
		xy_filt[0] = max( 0, min(xy_filt[0], parameters.UI_MAPSIZE[0]))
		xy_filt[1] = max( 0, min(xy_filt[1], parameters.UI_MAPSIZE[1]))

		#print("          inst: " + str(user.getPosEstimate()) + "-->" + str(xy_inst) + ", filt: " + str(xy_filt))
		print("      pos (filt): " + str(xy_filt))
		return xy_filt
		
	def lsqrError(self, xy, observedBeacons):
		# calculate the proposed distances to the beacons
		proposedBeaconDistances = {MajMin:self.iBeaconList[MajMin].getDistanceTo(xy)\
									for MajMin in observedBeacons}
		# calculate the measured distances to the beacons based on RSSI
		measuredBeaconDistances = {MajMin:observedBeacons[MajMin].getDistEst()\
									for MajMin in observedBeacons}
		# calculate difference between measured and proposed distances
		differences = {MajMin:(proposedBeaconDistances[MajMin]-measuredBeaconDistances[MajMin])\
									for MajMin in observedBeacons}
		# calculate weights (max at 1)
		weights = {MajMin:( min(100, 1/(measuredBeaconDistances[MajMin]**self.weighting_exponent)) )\
									for MajMin in observedBeacons} 

		# calculate weighted errors
		weightedErrors = [weights[MajMin]*differences[MajMin] for MajMin in observedBeacons]

		return weightedErrors

		# calculate weighted errors
		#weightedErrors = [self.]
		#return differences
















