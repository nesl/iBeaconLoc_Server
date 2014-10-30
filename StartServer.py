#!/usr/bin/env python3

# WARNING: PYTHON 3.2 AND GREATER ONLY

# ===== IMPORTS =====
# standard modules
import threading
import sys
from array import array
import time
import struct
# custom services
from inlocpkg.services import *
# custom objects
from inlocpkg.objects import *
# import constants
from inlocpkg.constants import parameters
from inlocpkg.constants import communication

# ===== SAY HELLO =====
print("===============================================")
print("          iBeacon Localization Server          ")
print("===============================================")

# ===== LIST OF ACTIVE USERS & BEACONS =====
active_users = {}
active_ibeacons = {}
# populate active beacons from parameter file
for b in parameters.BEACON_INFORMATION:
	major = b[0]
	minor = b[1]
	pos = (b[2], b[3])
	tx = Transmitter( pos, major, minor)
	print("initializing transmitter: " + str(tx))
	active_ibeacons[(major, minor)] = tx

# user interface and server objects
server = None
ui = None

# ===== HANDLE CLIENT COMMANDS =====
def handleClientCmd(socket, cmd, uid, payload):
	# ensure we have this user in our list
	if uid not in active_users:
			posEstimator = PositionEstimator(active_ibeacons,\
				weightingExponent=parameters.WEIGHT_COEFFICIENT,\
				lowPassCoeff=parameters.LOWPASS_COEFFICIENT)
			active_users[uid] = User(uid, posEstimator)
			ui.addUser(uid, "images/user_01.png")

	# switch on command type
	if cmd is communication.CMD_CLIENT_SENDBEACON:
		if len(payload) is not communication.CMD_CLIENT_SENDBEACON_PAYLOAD:
			return
		# client sent a beacon packet to the server
		major, minor, rssi, txpow = struct.unpack("!hhbb", payload)
		# if this isn't a beacon we recognize, give a warning and skip it
		if (major,minor) not in active_ibeacons:
			print('warning: client sending unrecognized beacon')
			return
		# create beacon object
		beacon = Beacon(major,minor,rssi,txpow)
		#print("User " + str(uid) + " sent: " + str(beacon))
		# make sure we have a record of this user. If not, make a new user with 
		# a position estimator service
		
		# pass beacon to user object
		active_users[uid].logBeaconRecord(beacon)

	if cmd is communication.CMD_CLIENT_REQUESTPOS:
		if len(payload) is not communication.CMD_CLIENT_REQUESTPOS_PAYLOAD:
			return
		# find the latest estimate of this user (default is 0,0)
		xy_latest = (0.0,0.0)
		if uid in active_users:
			xy_latest = active_users[uid].getPosEstimate()
		# send latest xy to user
		print("User " + str(uid) + " requesting pos., sending: " + str(xy_latest))
		response = struct.pack("!ff", xy_latest[0], xy_latest[1])
		socket.request.sendall(response)

	if cmd is communication.CMD_CLIENT_REQUESTPATH:
		# currently unhandled
		pass

	if cmd is communication.CMD_CLIENT_SENDSTATE:
		if len(payload) is not communication.CMD_CLIENT_SENDSTATE_PAYLOAD:
			return
		power, rate = struct.unpack("!bb", payload)
		active_users[uid].setPowerFilter(power)
		active_users[uid].setRateThrottle(rate)
		print("User " + str(uid) + " set power to " + str(power) + " and rate to " + str(rate))
		
# ===== PERIODICALLY ESTIMATE POSITIONS =====
def performEstimation(): 
	# sleep
	threading.Timer(parameters.ESTIMATION_PERIOD, performEstimation).start(); 
	# estimate for all users
	for uid in active_users:
		active_users[uid].estimateNewPosition()
		ui.moveUserMeters( uid, active_users[uid].getPosEstimate() )
		# update user stats
		#pow_est = estimatePowerConsumption(active_users[uid].getPowerFilter(), \
		#								   active_users[uid].getRateThrottle() )
		#life_est = estimateLifetimeMonths( BATTERYCAP_2AA, pow_est)
		#ui.updateUserStats( uid, pow_est, life_est )

# ===== FIRE UP THE GUI =====
ui = UserInterface(parameters.UI_MONITORSIZE, parameters.UI_MAPSIZE,\
			active_ibeacons, active_users, "images/background.png")

# ===== FIRE UP THE SERVER =====
server = InlocServer(communication.TCPIP_PORT, handleClientCmd)
server.start()

# ===== FIRE UP THE ESTIMATOR =====
performEstimation()

# add in the transmitters
for MajMin in active_ibeacons:
	b = active_ibeacons[MajMin]
	ui.addTransmitter(b.getMajor(), b.getMinor(), b.getPos(), "images/transmitter.png")
ui.start()
