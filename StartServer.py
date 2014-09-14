#!/usr/bin/env python

# WARNING: PYTHON 3.2 AND GREATER ONLY

# ===== IMPORTS =====
# standard modules
import socketserver
import socket
from threading import Thread, Lock
import sys
import struct
from array import array
import time
import struct
# custom objects
from inlocclasses import *
# import tcpip commands
from constants import communication
# import parameters
from constants import parameters

# ===== SAY HELLO =====
print("===============================================")
print("          iBeacon Localization Server          ")
print("===============================================")

# ===== LIST OF ACTIVE USERS & BEACONS =====
active_users = {}
active_beacons = []

# populate active beacons from parameter file
for b in parameters.BEACON_INFORMATION:
	tx = Transmitter( (b[0],b[1]), b[2], b[3], b[4])
	print("initializing transmitter: " + str(tx))

# ===== CLIENT HANDLER ===== 
class ClientHandler(socketserver.BaseRequestHandler):

	# function for handling new connections
	def handle(self):
		# only deal with 
		print("Client connected from " + str(self.client_address))
		# parse incoming data
		data = self.request.recv(1024)
		# packets contain at least command type and user id
		cmd = data[0]
		uid = data[1]
		payload = data[2:]

		# handle command appropriately
		handleClientCmd(self,cmd,uid,payload)

		print("Client exited from " + str(self.client_address))
		self.request.close()

# ===== HANDLE CLIENT COMMANDS =====
def handleClientCmd(socket, cmd, uid, payload):
	# switch on command type

	if cmd is communication.CMD_CLIENT_SENDBEACON:
		if len(payload) is not communication.CMD_CLIENT_SENDBEACON_PAYLOAD:
			# malformed packet
			return
		# client sent a beacon packet to the server
		major, minor, rssi = struct.unpack("!HHB", payload)
		print("user: " + str(uid) + " sent beacon with major: " + str(major) + " minor: " + str(minor) + " rssi: " + str(-rssi))

		# create beacon object
		beacon = Beacon(major,minor,rssi)
		# make sure we have a record of this user
		if uid not in active_users:
			active_users[uid] = User(uid)
		# pass beacon to user object
		active_users[uid].logBeaconRecord(beacon)

	if cmd is communication.CMD_CLIENT_REQUESTPOS:
		pass
	if cmd is communication.CMD_CLIENT_REQUESTPATH:
		pass
		



# ===== THREADED SERVER CLASS =====
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

# ===== FIRE UP THE SERVER ON GIVEN PORT =====
if len(sys.argv) < 2:
    print("Usage: python StartServer.py <port_num>")
else:
	print("Opening Server on port " + str(sys.argv[1]))
	myserver = ThreadedTCPServer(('',int(sys.argv[1])), ClientHandler)
	myserver.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	myserver.serve_forever()




