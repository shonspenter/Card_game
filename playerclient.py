#!/usr/bin/env python3
#
# Polymero
#

# Imports
import _thread
from socket import *
import os, sys, json


if len(sys.argv) < 2:
	print('Missing input.')
	exit()

elif sys.argv[1] == "-player1":

	recv_socket = socket(AF_INET, SOCK_STREAM)
	recv_socket.bind(('', 12000))
	recv_socket.listen()

	# send_socket = socket(AF_INET, SOCK_STREAM)
	# send_socket.bind(('', 12001))

	connection, address = recv_socket.accept()	

	print(connection.recv(1024))

	connection.send(b'Kalifornja?')

elif sys.argv[1] == "-player2":

	# recv_socket = socket(AF_INET, SOCK_STREAM)
	# recv_socket.bind(('', 12001))
	# recv_socket.listen()

	connection = socket(AF_INET, SOCK_STREAM)
	connection.connect((sys.argv[2], int(sys.argv[3])))

	connection.send(b'Wahoo!')

	print(connection.recv(1024))

else:
	print('Invalid input.')
	exit()


