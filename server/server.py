#!/usr/bin/python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import signal
import time
import sys
import os
#-------------------------------------------------------------#
from lib.request_handler import accept_requests
from lib.CtrlC import handle_interruption
from lib.Crypto import generate_keys
from lib.banner import server_banner
from lib.config import server_config
from lib.tunnel import port_forward
from lib.updater import check_update

#-------------------------------------------------------------#
#                        Main                                 #
#-------------------------------------------------------------#
#-------------------------------------------------------------#
if __name__ == '__main__':
	clients = {}
	names = []
	keys = []

	os.system('clear')
	print(server_banner())

	check_update()
	port, passcode, ngrok = server_config()
	buf = 128000
	
	sock = socket(AF_INET, SOCK_STREAM)
	try:sock.bind(('', port))
	except PermissionError:exit('[\033[1;91m!\033[m] Permission denied!Try sudo or another port above 1000.')
	except OSError:exit('[\033[1;91m!\033[m] Port in use!')
	sock.listen(10)

	if ngrok == 'TRUE':
		port_forward(port)
	else:
		print('[\033[1;92m*\033[m] Server running in port %s' % port)
		pass
	
	signal.signal(signal.SIGINT, handle_interruption)
	signal.signal(signal.SIGTSTP, handle_interruption)	
	
	public_key, private_key = generate_keys()
	# probably the most stupid and ugly thing you see but hey, it works :)
	sys.exit(Thread(target=accept_requests, args=(sock,clients,names,keys,passcode,buf,public_key,private_key)).start())
