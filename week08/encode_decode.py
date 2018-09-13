#!/usr/bin/python3
#Written by Costa Paraskevopoulos in September 2018
#Encode and decode a username using JSON Web Signatures

import time
from itsdangerous import JSONWebSignatureSerializer

def encode(user, key):
	curr_time = str(time.time())
	json = {'username': user, 'creation_time': curr_time}
	s = JSONWebSignatureSerializer(key)
	encoded = s.dumps(json)
	return encoded

def decode(encoding, key):
	s = JSONWebSignatureSerializer(key)
	decoded = s.loads(encoding, return_header=False)
	print('Decoded:', decoded)
	curr_time = float(time.time())
	if float(decoded['creation_time']) + 10 >= curr_time:
		return decoded['username']
	else:
		raise Exception('expired')

def main():
	uuid = '741a8707-061d-4298-b8c1-abad94c54d2a' #private key
	encoded = encode('admin', uuid)
	print('Encoding:', encoded)

	#decode the valid token
	user = decode(encoded, uuid)
	print(user)

	#decode an expired token
	time.sleep(10)
	try:
		decode(encoded, uuid)
	except Exception as e:
		print(str(e))

	#decode an invalid token
	try:
		decode('blablabla', uuid)
	except Exception as e:
		print(str(e))

if __name__ == '__main__':
	main()
