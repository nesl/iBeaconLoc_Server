#!/usr/bin/env python

# WARNING: PYTHON 3.2 AND GREATER ONLY

# ===== IMPORTS =====
# standard modules
import socketserver
import socket
from threading import Thread, Lock
import threading
import sys
import struct
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
	pos = (b[0], b[1])
	major = b[2]
	minor = b[3]
	power = b[4]
	tx = Transmitter( pos, major, minor, power)
	print("initializing transmitter: " + str(tx))
	active_ibeacons[(major, minor)] = tx

# ===== HANDLE CLIENT COMMANDS =====
def handleClientCmd(socket, cmd, uid, payload):
	# switch on command type

	if cmd is communication.CMD_CLIENT_SENDBEACON:
		if len(payload) is not communication.CMD_CLIENT_SENDBEACON_PAYLOAD:
			# malformed packet
			return
		# client sent a beacon packet to the server
		major, minor, rssi, txpow = struct.unpack("!HHBB", payload)
		# create beacon object
		beacon = Beacon(major,minor,-rssi,txpow)
		print("User " + str(uid) + " sent: " + str(beacon))
		# make sure we have a record of this user. If not, make a new user with 
		# a position estimator service
		if uid not in active_users:
			posEstimator = PositionEstimator(active_ibeacons, weighting_exponent=0, lowpassCoeff=0)
			active_users[uid] = User(uid, posEstimator)
		# pass beacon to user object
		active_users[uid].logBeaconRecord(beacon)

	if cmd is communication.CMD_CLIENT_REQUESTPOS:
		pass
	if cmd is communication.CMD_CLIENT_REQUESTPATH:
		pass
		
# ===== PERIODICALLY ESTIMATE POSITIONS =====
def performEstimation(): 
	# sleep
	threading.Timer(1, performEstimation).start(); 
	# estimate for all users
	for uid in active_users:
		active_users[uid].estimateNewPosition()

# ===== FIRE UP THE ESTIMATOR =====
performEstimation()

# ===== FIRE UP THE SERVER =====
server = InlocServer(communication.TCPIP_PORT, handleClientCmd)
server.run()







