#!/usr/bin/python3
#Written by Costa Paraskevopoulos in September 2018
#Flask RESTful API for managing a database of books
#Secured with basic authentication

import json
import pandas as pd
from flask import *
from functools import *
from flask_restplus import *

app = Flask(__name__)
api = Api(
	app,
	version='1.0',
	default='Books',
	title='Book API',
	description='Add, retrieve, remove and update book information.'
)

#the book schema
book_model = api.model('Book', {
	'Flickr_URL': fields.String,
	'Publisher': fields.String,
	'Author': fields.String,
	'Title': fields.String,
	'Date_of_Publication': fields.Integer,
	'Identifier': fields.Integer,
	'Place_of_Publication': fields.String
})

parser = reqparse.RequestParser()
parser.add_argument('order', choices=list(column for column in book_model.keys()))
parser.add_argument('ascending', type=inputs.boolean)

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization

		if not auth:
			print('Debugging: no header set')
			abort(401)

		if auth.username != 'admin' or auth.password != 'admin':
			print('Debugging: invalid user')
			abort(401)

		return f(*args, **kwargs)
	return decorated

@api.route('/books')
class BooksList(Resource):
	@api.response(200, 'Successful')
	@api.doc(description='Get all books')
	@requires_auth
	def get(self):
	    #get books as json string
	    args = parser.parse_args()

	    #retrieve the query parameters
	    order_by = args.get('order')
	    ascending = args.get('ascending', True)

	    if order_by:
	        df.sort_values(by=order_by, inplace=True, ascending=ascending)

	    json_str = df.to_json(orient='index')

	    #convert the string json to a real json
	    ds = json.loads(json_str)
	    ret = []

	    for idx in ds:
	        book = ds[idx]
	        book['Identifier'] = int(idx)
	        ret.append(book)

	    return ret

	@api.response(201, 'Book Created Successfully')
	@api.response(400, 'Validation Error')
	@api.doc(description='Add a new book')
	@api.expect(book_model, validate=True)
	@requires_auth
	def post(self):
	    book = request.json

	    if 'Identifier' not in book:
	        return {'message': 'Missing Identifier'}, 400

	    id = book['Identifier']

	    #check if the given identifier does not exist
	    if id in df.index:
	        return {'message': 'A book with Identifier={} is already in the dataset'.format(id)}, 400

	    #put the values into the dataframe
	    for key in book:
	        if key not in book_model.keys():
	            #unexpected column
	            return {'message': 'Property {} is invalid'.format(key)}, 400
	        df.loc[id, key] = book[key]

	    #df.append(book, ignore_index=True)
	    return {'message': 'Book {} is created'.format(id)}, 201

@api.route('/books/<int:id>')
@api.param('id', 'The Book identifier')
class Books(Resource):
	@api.response(404, 'Book was not found')
	@api.response(200, 'Successful')
	@api.doc(description='Get a book by its ID')
	@requires_auth
	def get(self, id):
	    if id not in df.index:
	        api.abort(404, 'Book {} does not exist'.format(id))

	    book = dict(df.loc[id])
	    return book

	@api.response(404, 'Book was not found')
	@api.response(200, 'Successful')
	@api.doc(description='Delete a book by its ID')
	@requires_auth
	def delete(self, id):
	    if id not in df.index:
	        api.abort(404, 'Book {} does not exist'.format(id))

	    df.drop(id, inplace=True)
	    return {'message': 'Book {} is removed'.format(id)}, 200

	@api.response(404, 'Book was not found')
	@api.response(400, 'Validation Error')
	@api.response(200, 'Successful')
	@api.expect(book_model, validate=True)
	@api.doc(description='Update a book by its ID')
	@requires_auth
	def put(self, id):

	    if id not in df.index:
	        api.abort(404, 'Book {} does not exist'.format(id))

	    #get the payload and convert it to json
	    book = request.json

	    #book id cannot be changed
	    if 'Identifier' in book and id != book['Identifier']:
	        return {'message': 'Identifier cannot be changed'.format(id)}, 400

	    #update the values
	    for key in book:
	        if key not in book_model.keys():
	            #unexpected column
	            return {'message': 'Property {} is invalid'.format(key)}, 400
	        df.loc[id, key] = book[key]

	    df.append(book, ignore_index=True)
	    return {'message': 'Book {} has been successfully updated'.format(id)}, 200

if __name__ == '__main__':
	columns_to_drop = ['Edition Statement',
	                   'Corporate Author',
	                   'Corporate Contributors',
	                   'Former owner',
	                   'Engraver',
	                   'Contributors',
	                   'Issuance type',
	                   'Shelfmarks'
	                   ]
	csv_file = 'Books.csv'
	df = pd.read_csv(csv_file)

	#drop unnecessary columns
	df.drop(columns_to_drop, inplace=True, axis=1)

	#clean the date of publication & convert it to numeric data
	new_date = df['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
	new_date = pd.to_numeric(new_date)
	new_date = new_date.fillna(0)
	df['Date of Publication'] = new_date

	#replace spaces in the name of columns
	df.columns = [c.replace(' ', '_') for c in df.columns]

	#set the index column; this will help us to find books with their ids
	df.set_index('Identifier', inplace=True)

	#run the application
	app.run(debug=True)
