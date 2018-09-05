#!/usr/bin/python3
#Written by Costa Paraskevopoulos in September 2018
#Update an existing book in the book dataset

import requests

def main():
	url = 'http://127.0.0.1:5000/books/206'
	res = requests.get(url)
	print('Debugging:', res.url)
	print('Status code:', res.status_code)
	if res.status_code == 200:
		print(str(res.json()) + '\n')

	payload = res.json()
	payload['Author'] = 'Nobody'
	res = requests.put(url, json=payload)
	print('Debugging:', res.url)
	print('Status code:', res.status_code)
	if res.status_code == 200:
		print(str(res.json()) + '\n')

	res = requests.get(url)
	print('Debugging:', res.url)
	print('Status code:', res.status_code)
	if res.status_code == 200:
		print(res.json())

if __name__ == '__main__':
	main()
