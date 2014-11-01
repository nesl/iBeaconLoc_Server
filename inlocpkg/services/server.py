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
import binascii

# ===== THREADED SERVER CLASS =====
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	cmdHandler = None

	def __init__(self, cmdHandler, *args, **kwargs):
		super(ThreadedTCPServer, self).__init__(*args, **kwargs)
		self.cmdHandler = cmdHandler

	def finish_request(self, request, client_address):
		"""Finish one request by instantiating RequestHandlerClass."""
		self.RequestHandlerClass(self.cmdHandler, request, client_address, self)

# ===== CLIENT HANDLER ===== 
class ClientHandler(socketserver.BaseRequestHandler):
	inlocCmdHandler = None

	def __init__(self, cmdHandler, *args, **kwargs):
		self.inlocCmdHandler = cmdHandler
		super(ClientHandler, self).__init__(*args, **kwargs)

	# function for handling new connections
	def handle(self):
		print("Client connected from " + str(self.client_address))		
		while True:
			# parse incoming data
			data = self.request.recv(1024)
			if not data: 
				break
			# decode this data as UTF-8
			#try:
			data_ascii = data.decode("UTF-8")
			#print(' --- read --- : ' + str(data_ascii))
			# we could've gotten multiple packets here, break them up
			packets = data_ascii.split('\n')
			for packet in packets:
				if len(packet) < 2:
					continue
				#print('received (ascii): ' + packet)
				# this is ascii data now, CSV. split up
				values = [int(strval) for strval in packet.split(',')]
				# packets contain at least command type and user id
				if len(values) < 2:
					return

				cmd = values[0]
				uid = values[1]
				payload = values[2:]
				# handle command appropriately
				self.inlocCmdHandler(self,cmd,uid,payload)
			#except:
			#	pass
			
		print("Client exited from " + str(self.client_address))
		self.request.close()


# ===== HIGH LEVEL SERVER =====
class InlocServer(threading.Thread):
	port = None
	threadedServer = None

	def __init__(self, port, cmdHandler):
		self.port = port
		self.threadedServer = ThreadedTCPServer(cmdHandler, ('',self.port), ClientHandler)
		self.threadedServer.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# initialize super thread
		super(InlocServer,self).__init__()

	def run(self):
		self.threadedServer.serve_forever()


