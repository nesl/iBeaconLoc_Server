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
	pass

# ===== HIGH LEVEL SERVER =====
class InlocServer():
	port = None
	threadedServer = None


	def __init__(self, port, handler):
		self.port = port
		self.threadedServer = ThreadedTCPServer(('',self.port), handler)
		self.threadedServer.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def start(self):
		self.threadedServer.serve_forever()


