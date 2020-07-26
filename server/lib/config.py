#!/usr/bin/python3
import configparser
import sys

#-----------------Server configuration parser-----------------#
#-------------------------------------------------------------#
def server_config():
  config = configparser.RawConfigParser()   
  config.read(r'config/server.ini')

  try:
  	passcode = config.get('config', 'PASSCODE')
  except configparser.NoSectionError:
  	exit('[!]I can\'t find the server configuration file')

  try:
    port = int(config.get('config', 'PORT'))
  except ValueError:
    exit('[!] Invalid port!')
      
  ngrok = config.get('config', 'NGROK')

  return port, passcode, ngrok