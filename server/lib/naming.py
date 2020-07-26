#!/usr/bin/python3
from .broadcaster import recieve_messages, broadcast
from .Crypto import generate_keys, encrypt, decrypt
from .sanitizer import message_sanitizer
from .banner import random_banner
from .colors import *
#-------------------------------------------------------------#
from threading import Thread
from base64 import b64encode
import random
import time

#-------------------Setting up names--------------------------#
#-------------------------------------------------------------#
def ask_name(client,client_address,key,clients,names,keys,passcode,buf,public_key,private_key):
	recieved_name = client.recv(buf)
	name = decrypt(private_key, recieved_name)
	name = message_sanitizer(name)

	if name in names:
		name = name+str(random.randint(1,9))
		client.send(bytes('%s%s!%s%s Name in use! Using %s instead%s' % (bold,red,reset,red,name,reset),'utf-8'))

	names.append(name)
	
	banner = random_banner().encode()
	banner = b64encode(banner)
	client.sendall(bytes(banner))
	clients[client] = name
	time.sleep(2)
	client.send(bytes(encrypt(key, '%s%s~ Hello %s,Welcome to AnoChat chatroom! Use !help for help%s\n' % (bold,blue,name,reset))))
	print('[\033[1;92m*\033[m] '+name+' Entered the chat room!')

	time.sleep(2)
	broadcast('%s%s+%s %s%s %sjoined the chat!%s'%(green,bold,reset,reset,name,blue,reset),clients,keys)
	time.sleep(2)
	for name in names:
		client.send(bytes(encrypt(key,"%s%s* %s%s%s is online.%s"% (bold,green,reset,name,green,reset))))
		time.sleep(2)
	

	Thread(target=recieve_messages, args=(name,client,client_address,key,clients,names,keys,passcode,buf,public_key,private_key)).start()