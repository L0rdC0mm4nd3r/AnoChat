#!/usr/bin/python3
#------------Removing unwanted things from messge-------------#
#-------------------------------------------------------------#

# This function sanitizes messages before broadcasting them so messages
# like \t\n\r\x0b\x0c and \x1b\x5b\x33\x3b\x4a\x1b\x5b\x48\x1b\x5b\x32\x4a
# are encoded here before broadcast which prevents clients sending raw bytes
# though this method is simple it have drawback which is, other characters that
# are not english (like Arabic) will not be broadcasted rather if client send 
# non english character it will be broadcasted as encoded bytes

def message_sanitizer(text):

  text = text.encode()
  text = str(text)
  text = text[2:-1]
  text = text.replace('\\','')

  return text

