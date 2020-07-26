#!/usr/bin/python3
from Crypto.Cipher.PKCS1_OAEP import PKCS1OAEP_Cipher
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64
import sys

#-------------------Crypto Operation--------------------------#
#-------------------------------------------------------------#
def generate_keys():
  sys.stdout.write('\r[\033[1;97m~\033[m] Generating keys')
  sys.stdout.flush()
  key = RSA.generate(2048)
  private_key, public_key = key.export_key(), key.publickey().export_key()
  sys.stdout.write('\r[\033[1;92m*\033[m] Keys Generated...\n')
  sys.stdout.flush()

  return public_key,private_key


def encrypt(public_key, data):
  data = data.encode('utf-8')
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
    return 'Can\'t decrypt message,Possible reasons: Man in the middle or server Error'