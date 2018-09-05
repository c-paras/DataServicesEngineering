#!/usr/bin/python3
#Written by Costa Paraskevopoulos in September 2018
#Delete an existing book in the book dataset

import requests

def main():
	url = 'http://127.0.0.1:5000/books/206'
	res = requests.get(url)
	print('Debugging:', res.url)
	print('Status code:', res.status_code)
	if res.status_code == 200:
		print(str(res.json()) + '\n')

	res = requests.delete(url)
	print('Debugging:', res.url)
	print('Status code:', res.status_code)
	if res.status_code == 200:
		print(str(res.json()) + '\n')

	res = requests.get(url)
	print('Debugging:', res.url)
	print('Status code:', res.status_code)
	if res.status_code == 404:
		print(res.json())

if __name__ == '__main__':
	main()
