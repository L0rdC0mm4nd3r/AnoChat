#!/usr/bin/python3
from pyngrok.ngrok import PyngrokConfig
from pyngrok import ngrok
import socket
import sys

# Forwards server port to be publicly accessed on the internet#
#-------------------------------------------------------------#
def port_forward(port):
	try:
		pyngrok_config = PyngrokConfig(monitor_thread = False)
		server_addr = ngrok.connect(port, 'tcp', pyngrok_config=pyngrok_config)
		
		server_addr = server_addr.split('//',1)[1]
		ip = server_addr.split(':',1)[0]
		port = server_addr.split(':',1)[1] 
		server_ip = socket.gethostbyname(ip)

		print('[\033[1;92m*\033[m] Server IP: \033[1;92m%s\033[m' % server_ip)
		print('[\033[1;92m*\033[m] Server Port: \033[1;92m%s\033[m' % port)

	except Exception as e:
		exit(e)
