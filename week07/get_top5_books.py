#!/usr/bin/python3
#Written by Costa Paraskevopoulos in September 2018
#Get top 5 books ordered by publication date in ascending order

import requests

def main():
	url = 'http://localhost:5000/books'
	payload = {'order': 'Date_of_Publication', 'ascending': 'true'}
	res = requests.get(url, params=payload)

	print('Debugging:', res.url)
	print('Status code:', res.status_code)

	if res.status_code == 200:
		books = res.json()
		for book in books[0:5]:
			print('\n' + str(book))

if __name__ == '__main__':
	main()
