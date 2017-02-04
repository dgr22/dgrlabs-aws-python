#!/usr/bin/python3.4
import sys
import base64
#import boto3

def decrypt_data(encrypted_data):
   #decrypted = kms.decrypt(CiphertextBlob=encrypted_data)
   #decrypt = decrypted['Plaintext'].decode('utf-8')
   decrypt = base64.b64decode(encrypted_data)
   decrypt = decrypt.decode('utf-8')
   return decrypt

def grant ():
     sys.stdout.write( 'OK\n' )
     sys.stdout.flush()

def deny ():
     sys.stdout.write( 'ERR\n' )
     sys.stdout.flush()

#kms = boto3.client('kms')
while True:
	try:	
		line = sys.stdin.readline().strip()
		if decrypt_data(line) == 'YES':

			grant()
		else:
        		deny()
	except:
		deny()
