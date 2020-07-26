#!/usr/bin/python3
from .Crypto import generate_keys, encrypt, decrypt
from .naming import ask_name
from .broadcaster import broadcast
from .colors import *
#-------------------------------------------------------------#
from threading import Thread

#--------Passcode verification to join the chatroom-----------#
#-------------------------------------------------------------#
def verify_passcode(client,client_address,key,clients,names,keys,passcode,buf,public_key,private_key):
	passwd = client.recv(buf)
	passwd = decrypt(private_key, passwd)

	if passwd != passcode:
		try:
			client.send(bytes(encrypt(key,'%s%s!%s%s  Wrong passcode!%s' %(bold, red, reset, red, reset))))
			print('[\033[1;91m!\033[m] %s:%s entered wrong passcode!' % client_address)
			broadcast('%s%s!%s  %s %stried to join with wrong passcode!%s' %(bold,red, reset, client_address[0], red, reset), clients, keys)
			keys.remove(key)
			client.close()

		# if someone uses netcat or tries to connect without sending keys
		# this happens specially if ngrok is used
		except ValueError:
			print('[\033[1;91m!\033[m] %s:%s is trying to connect without sending keys!' % client_address)
			keys.remove(key)
			client.close()
			print('[\033[1;91m-\033[m] Kicked out %s:%s' % client_address)
	else:
		client.send(bytes(encrypt(key,'Correct passcode!')))
		clients[client] = client
		Thread(target=ask_name, args=(client,client_address,key,clients,names,keys,passcode,buf,public_key,private_key)).start()