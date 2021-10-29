#!/usr/bin/env python3
#
# Polymero
#

# Imports
from socket import *
import os, sys, pickle


if len(sys.argv) < 2:
	print('Missing some inputs here.... Hello?')
	exit()


if sys.argv[1] in ['-h', '--host']:

	recv_socket = socket(AF_INET, SOCK_STREAM)

	try: recv_socket.bind(('', int(sys.argv[2])))
	except: recv_socket.bind(('', 12000))

	recv_socket.listen()
	print('Hosting on', recv_socket.getsockname())
	print('Waiting for other player to connect...')

	connection, address = recv_socket.accept()

	print('Player connected from', address)


if sys.argv[1] in ['-j', '--join']:

	connection = socket(AF_INET, SOCK_STREAM)

	try: connection.connect((sys.argv[2], int(sys.argv[3])))
	except: print('Failed to join game...'); exit()

	print('Joined game at', connection.getpeername())