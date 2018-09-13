#!/usr/bin/python3
#Written by Costa Paraskevopoulos in September 2018
#Client application for the Bokk API to test Basic Auth

import requests

def main():
	url = 'http://localhost:5000/books/206'
	res = requests.get(url, auth=('admin', 'admin'))

	print('Debugging:', res.url)
	print('Status code:', res.status_code)

	if res.status_code == 200:
		book = res.json()
		print('\n' + str(book))

	res = requests.get(url, auth=('hello', 'world'))

	if res.status_code == 401:
		print('Invalid credentials')

if __name__ == '__main__':
	main()
