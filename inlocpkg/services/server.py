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
		# only deal with 
		#print("Client connected from " + str(self.client_address))
		# parse incoming data
		data = self.request.recv(1024)
		# packets contain at least command type and user id
		if len(data) < 2:
			return

		cmd = data[0]
		uid = data[1]
		payload = data[2:]

		# handle command appropriately
		self.inlocCmdHandler(self,cmd,uid,payload)

		#print("Client exited from " + str(self.client_address))
		self.request.close()


# ===== HIGH LEVEL SERVER =====
class InlocServer():
	port = None
	threadedServer = None

	def __init__(self, port, cmdHandler):
		self.port = port
		self.threadedServer = ThreadedTCPServer(cmdHandler, ('',self.port), ClientHandler)
		self.threadedServer.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def start(self):
		self.threadedServer.serve_forever()


