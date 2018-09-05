#!/usr/bin/python3
#Written by Costa Paraskevopoulos in September 2018
#Add a new book to the book dataset

import requests

def main():
	payload = {
		"Date_of_Publication": 1999,
		"Publisher": "S. Smith Ltd.",
		"Author": "S. Smith",
		"Title": "Hello World",
		"Flickr_URL": "https://www.example.com",
		"Identifier": 123,
		"Place_of_Publication": "Somewhere"
	}

	url = 'http://localhost:5000/books'
	res = requests.post(url, json=payload)

	print('Debugging:', res.url)
	print('Status code:', res.status_code)

	if res.status_code == 201:
		print(res.json())

if __name__ == '__main__':
	main()
