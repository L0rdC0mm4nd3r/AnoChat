#!/usr/bin/python3
from .Crypto import generate_keys, encrypt, decrypt
from .sanitizer import message_sanitizer
from .colors import *
#-------------------------------------------------------------#
from threading import Thread
import time

#--------------Recieve messages and broadcast-----------------#
#-------------------------------------------------------------#

def recieve_messages(name,client,client_address,key,clients,names,keys,passcode,buf,public_key,private_key):
	while True:
		try:
			incoming_msg = client.recv(buf)
		except OSError:
			continue

		incoming_msg = decrypt(private_key,incoming_msg)
		incoming_msg = message_sanitizer(incoming_msg)

		if incoming_msg == '!quit':
			print('[%s] [\033[1;91m-\033[m] %s left the chatroom' % (time.strftime("%X"),name))
			broadcast('%s%s-%s %s%s %sleft the chatroom%s' % (bold,red,reset,reset,name,red,reset),clients,keys)
			client.close()
			del clients[client]			
			keys.remove(key)
			names.remove(name)
			break
		
		elif incoming_msg == '!online':
			for name in names:
				client.send(bytes(encrypt(key,"%s%s* %s%s%s is online.%s"% (bold,green,reset,name,green,reset))))
				time.sleep(2)

		elif incoming_msg == '!help':
			help_msg = '\n%s Commands%s\n >_ !online\n >_ !quit\n >_ !clear\n >_ !contact' % (bold,reset)
			client.send(bytes(encrypt(key,help_msg)))

		elif incoming_msg == '!contact':
			contact = '\n%sContact the Author%s\n Telegram : t.me/L0rdComm4nd3r\n Github : github.com/L0rdC0mm4nd3r : @yahoo.com' % (bold,reset)
			client.send(bytes(encrypt(key,contact)))
			
		else:
			messages = str('<%s> : %s' % (name,incoming_msg))
			broadcast(messages,clients,keys)


def broadcast(msg,clients,keys):
	count = 0
	for client in clients:
		key = (keys[count])
		message = encrypt(key,msg)
		client.send(bytes(message))
		count+=1
