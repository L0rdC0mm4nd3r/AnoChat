#!/usr/bin/python3
from threading import Thread
import time
import sys
#-------------------------------------------------------------#
from .recieve_key import recv_key

#----------------Accepts and handles requests-----------------#
#-------------------------------------------------------------#
def accept_requests(sock,clients,names,keys,passcode,buf,public_key,private_key):
	while True:
		client, client_address= sock.accept()
		print('[%s] [\033[1;94m+\033[m] %s:%s has connected.' % (time.strftime("%X"),client_address[0],client_address[1]))
		sys.stdout.write('\r[%s] [\033[1;92m~\033m] Sending public key to %s:%s' % (time.strftime("%X"),client_address[0],client_address[1]))
		sys.stdout.flush()
		client.send(bytes(public_key))
		Thread(target=recv_key, args=(client,client_address,clients,names,keys,passcode,buf,public_key,private_key)).start()
