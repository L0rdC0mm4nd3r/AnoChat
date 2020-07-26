#!/usr/bin/python3
from .passcode import verify_passcode
#-------------------------------------------------------------#
from threading import Thread
import time
import sys

#------------------Recieve Public Key-------------------------#
#-------------------------------------------------------------#
def recv_key(client,client_address,clients,names,keys,passcode,buf,public_key,private_key):
	sys.stdout.write('\r[%s] [\033[1;97m~\033[m] Recieving Public key from %s:%s' % (time.strftime("%X"),client_address[0],client_address[1]))
	sys.stdout.flush()
	key = client.recv(buf)
	keys.append(key)
	sys.stdout.write('\r[%s] [\033[1;92m*\033[m] Recieved Public key from %s:%s...\n' % (time.strftime("%X"),client_address[0],client_address[1]))
	sys.stdout.flush()

	Thread(target=verify_passcode, args=(client,client_address,key,clients,names,keys,passcode,buf,public_key,private_key)).start()
