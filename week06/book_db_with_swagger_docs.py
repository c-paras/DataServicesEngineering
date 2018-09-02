#!/usr/bin/python3
#Written by Costa Paraskevopoulos in September 2018
#Flask RESTful API for managing a database of books
#Add, retrieve, remove and update book information
#List book information with desired sorting

import pandas as pd
from flask import *
from flask_restplus import *

#globals
df = pd.read_csv('Books.csv')
app = Flask(__name__)
api = Api(app, version='1.0', title='Book API', description=
	'Add, retrieve, remove and update book information')

#request parser for book list sorting parameters
sort_parser = api.parser()
sort_parser.add_argument('desc', type=inputs.boolean, required=True)
sort_parser.add_argument('column', type=str, required=True)

@api.route('/book/')
@api.param('desc', 'Whether sorting should be reversed')
@api.param('column', 'Name of the column to sort by')
@api.expect(sort_parser)
class List(Resource):
	@api.response(200, 'Success')
	@api.response(400, 'Invalid column name')
	@api.doc(description='Return list of all known books')
	def get(self):
		args = sort_parser.parse_args()
		desc = args['desc']
		column = args['column']
		num = 0
		json = []
		for index in df.iterrows():
			json.append(dict(df.loc[df.index[num]]))
			num += 1
		try:
			json.sort(key=lambda x: str(x[column]), reverse=desc)
			return {'size': num, 'results': json}
		except:
			return {column: 'invalid column'}, 400

@api.route('/book/<int:book_id>')
@api.param('book_id', 'The unique identifier for the book')
class Book(Resource):
	@api.response(200, 'Success')
	@api.response(404, 'Unknown book ID')
	@api.doc(description='Retrieve information about a book')
	def get(self, book_id):
		try:
			book = dict(df.query(str(book_id)))
			return book
		except:
			return {book_id: 'invalid book id'}, 404

	@api.response(200, 'Success')
	@api.response(404, 'Unknown book ID')
	@api.doc(description='Remove an existing book')
	def delete(self, book_id):
		try:
			book = df.loc[book_id]
			df.drop(book_id, inplace=True)
			return {book_id: 'book removed'}
		except:
			return {book_id: 'invalid book id'}, 404

	book_fields = {
		"PlaceofPublication": fields.String,
		"DateofPublication": fields.Integer,
		"Publisher": fields.String,
		"Title": fields.String,
		"Author": fields.String,
		"FlickrURL": fields.String
	}

	resource_fields = api.model('Resource', book_fields)

	@api.response(200, 'Success')
	@api.response(400, 'Invalid key field')
	@api.response(404, 'Unknown book ID')
	@api.doc(description='Update fields of an existing book')
	@api.expect(resource_fields)
	def put(self, book_id):
		try:
			book = df.loc[book_id]
			content = request.get_json(silent=True)
			for key, value in content.items():
				#alternative: if key in book_fields:
				valid = False
				for valid_key in ['PlaceofPublication', 'DateofPublication', 'Publisher', 'Title', 'Author', 'FlickrURL']:
					if key == valid_key:
						df.at[book_id, key] = value
						valid = True
				if valid == False:
					return {key: 'invalid key'}, 400
			return {book_id: 'book updated'}
		except:
			return {book_id: 'invalid book id'}, 404

	@api.response(200, 'Success')
	@api.response(400, 'Invalid key field or duplicate book ID')
	@api.doc(description='Insert a new book with an ID')
	@api.expect(resource_fields)
	def post(self, book_id):
		try:
			book = df.loc[book_id]
			return {book_id: 'book id exists'}, 400
		except:
			content = request.get_json(silent=True)
			new_book = []
			for key, value in content.items():
				#alternative: if key in book_fields:
				valid = False
				for valid_key in ['PlaceofPublication', 'DateofPublication', 'Publisher', 'Title', 'Author', 'FlickrURL']:
					if key == valid_key:
						new_book.append(value)
						valid = True
				if valid == False:
					return {key: 'invalid key'}, 400
			df.loc[book_id] = new_book
			return {book_id: 'book inserted'}

def clean_place_of_pub(place):
	if 'London' in place: place = 'London'
	place = place.replace('-', '')
	return place

def clean_date_of_pub(date):
	return date.str.extract(r'([0-9]{4})', expand=False)

def main():
	#drop unwanted columns
	to_drop = ['Edition Statement', 'Corporate Author',
		'Corporate Contributors', 'Former owner', 'Engraver', 'Contributors',
		'Issuance type', 'Shelfmarks']
	df.drop(columns=to_drop, inplace=True)

	#simplify place of publication
	df['Place of Publication'] = df['Place of Publication'].apply(clean_place_of_pub)

	#simplify date of publication
	df['Date of Publication'] = clean_date_of_pub(df['Date of Publication'])
	df['Date of Publication'] = pd.to_numeric(df['Date of Publication'])
	df['Date of Publication'] = df['Date of Publication'].fillna(0)

	#set the index to the book id
	df.set_index('Identifier', inplace=True)

	#remove all spaces from column names
	df.columns = df.columns.str.replace(' ', '')

	#now run the api
	app.run(debug=True)

if __name__ == '__main__':
	main()
