#!/usr/bin/python3
from Crypto.Cipher.PKCS1_OAEP import PKCS1OAEP_Cipher                             # for encryption and decryption of messages
from Crypto.Random import get_random_bytes										  # for encryption and decryption of messages
from Crypto.Cipher import AES, PKCS1_OAEP										  # for encryption and decryption of messages
from Crypto.PublicKey import RSA 												  # for encryption and decryption of messages
from socket import AF_INET, socket, SOCK_STREAM	                                  # for creating connection to server
from threading import Thread                                                      # for sending and recieving messages at the same time
from base64 import b64decode                                                      # for decoding banner
import stdiomask                                                                  # passwords shouldn't be seen as regular input 
import readline                                                                   # for arrow keys to work
import signal                                                                     # for handling user interupttion
import sys                                                                        # for printing, and terminating
import time                                                                       # for viewing messae arrival time
import os                                                                         # for clearing the screen

#--------Passcode verification to join the chatroom-----------#
#-------------------------------------------------------------#
def verify_passcode():
	passcode = stdiomask.getpass(prompt='\nEnter passcode: ')
	client_socket.send(encrypt(server_key,passcode))
	response = client_socket.recv(buf)
	response = decrypt(private_key,response)

	if 'Wrong passcode!' in response:
		print(response)
		client_socket.close()
	else:
		tell_name()

#-------------------Setting nick name-------------------------#
#-------------------------------------------------------------#
def tell_name():
	name = input('Enter your nick name: ')
	client_socket.send(bytes(encrypt(server_key,name)))

	welcome = client_socket.recv(buf)
	welcome = b64decode(welcome)
	welcome = welcome.decode()
	os.system('clear')
	print(welcome)

	send_thread = Thread(target=send)
	send_thread.start()
	recv_thread = Thread(target=recv)
	recv_thread.start()
	recv_thread.join()
	send_thread.join()

#----------------------Sends Messages-------------------------#
#-------------------------------------------------------------#
def send():
	try:
		while True:
			msg = input('')
			if msg == '':
				pass

			elif msg == '!clear':
				os.system('clear')
				print('-'*50)
				pass

			elif msg == '!quit':
				print('[\033[1;91m!\033[m] Quitting...')
				client_socket.send(bytes(encrypt(server_key,msg)))
				client_socket.close() 
				break
				sys.exit()
					
				
			else:
				if len(msg) > 87:# to avoid value error on encryption
					print('[\033[1;91m!\033[m] Message too long')
					msg = msg[:87]
				
				client_socket.send(bytes(encrypt(server_key,msg)))
	
	# this is raised after user interruption  
	except ValueError:
		pass

#----------------------Recieve Messages-----------------------#
#-------------------------------------------------------------#
def recv():
	try:
		while True:
			msg = client_socket.recv(buf)
			
			msg = decrypt(private_key,msg)
			if msg == '':
				pass

			elif msg == None:
				print('[\033[1;91m!\033[m] Server Problem')
			
			else:
				print('[%s] %s' % (time.strftime("%X"),msg))
				
	except OSError:
			pass
	

#-------------------Crypto Operation--------------------------#
#-------------------------------------------------------------#
def exchange_keys():
	sys.stdout.write('\r[\033[1;97m~\033[m] Sending Public Key to Server')
	sys.stdout.flush()
	key = client_socket.recv(buf)
	client_socket.send(bytes(public_key))
	sys.stdout.write('\r[\033[1;92m*\033[m] Public Key has been sent to Server')
	sys.stdout.flush()

	return key


def generate_keys():
	sys.stdout.write('\r[\033[1;97m~\033[m] Generating keys')
	sys.stdout.flush()
	key = RSA.generate(2048)
	private_key, public_key = key.export_key(), key.publickey().export_key()
	sys.stdout.write('\r[\033[1;92m*\033[m] Keys Generated...\n')
	sys.stdout.flush()

	return public_key,private_key


def encrypt(public_key, msg):
	data = msg.encode('utf-8')
	public_key = RSA.import_key(public_key)
	cipher_rsa = PKCS1_OAEP.new(public_key)
	encrypted_data = cipher_rsa.encrypt(data)

	return encrypted_data


def decrypt(private_key,encrypted_data):
	private_key = RSA.import_key(private_key)
	cipher_rsa: PKCS1OAEP_Cipher = PKCS1_OAEP.new(private_key)
	try:
		data = cipher_rsa.decrypt(encrypted_data)
		return data.decode('utf-8')
	except ValueError:
		pass

#-----------------Handle User interrupt-----------------------#
#-------------------------------------------------------------#
def handle_interruption(signum, frame):
	client_socket.send(bytes(encrypt(server_key,'!quit')))
	client_socket.close()
	exit('[\033[1;91m!\033[m]Quitting...')

#-------------------------------------------------------------#
if __name__ == '__main__':
	if len(sys.argv) < 3:
		exit('usage: %s <host> <port>'% sys.argv[0])

	host = sys.argv[1]
	try:port = int(sys.argv[2])
	except ValueError:exit('[\033[1;91m!\033[m] Invalid port!')

	buf = 128000
	public_key,private_key = generate_keys()

	client_socket = socket(AF_INET, SOCK_STREAM)
	try:client_socket.connect((host,port))
	except ConnectionRefusedError:exit('[\033[1;91m!\033[m] I can\'t initiate a connection,Are you sure about the adress you provided?')
	except Exception:exit('[\033[1;91m!\033[m] Invalid adress!')
	
	server_key = exchange_keys()
	#handling ctrl-c
	signal.signal(signal.SIGINT, handle_interruption)
	#handling ctrl-z
	signal.signal(signal.SIGTSTP, handle_interruption)
	
	sys.exit(verify_passcode())