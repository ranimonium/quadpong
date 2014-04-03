#!/usr/bin/python

import socket
import traceback

BUFFER_SIZE = 1024

class _myConnection(object):	
	
	def __init__(self, s):
		self.s = s #socket

	def sendMessage(self, msg):
		try:
			numBytes = self.s.send(msg)
		except socket.error as serr:
			print serr, serr.errno
			traceback.print_exc()
			return False
		return numBytes > 0

	def getMessage(self):
		return self.s.recv(BUFFER_SIZE)
		


def connection(s):
	return _myConnection(s)

