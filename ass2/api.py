#!/usr/bin/python3
#Written by Costa Paraskevopoulos in September 2018
#RESTful API for country-specific economic indicator data
#Based on data provided by the World Bank API V2

import datetime
import requests
from pymongo import *
from flask_restplus import *
from flask import *

#connect to mongodb database hosted on mlab
connection = MongoClient('ds149742.mlab.com', 49742)
db = connection['worldbank']
db.authenticate('ass2', 'comp9321')
collection = db.stats

#initialize flask app
app = Flask(__name__)
api = Api(app, version='1.0',
	default='Collections',
	title='Economic Indicator API',
	description='''
	RESTful API for country-specific economic indicator data
	Based on data provided by the World Bank API V2
	''')

@api.route('/collections/')
class Collections(Resource):
	params = api.model(
		'Resource',
		{ 'indicator_id': fields.String }
	)

	@api.expect(params)
	@api.response(201, 'Imported collection successfully')
	@api.response(200, 'Collection already imported previously')
	@api.response(400, 'Unknown economic indicator')
	@api.response(503, 'Problem with World Bank API')
	@api.doc(description='Import economic indicator data from World Bank')
	def post(self):
		indicator_id = request.json['indicator_id']

		#check if document already exists
		stored = list(collection.find(
			{ 'collection_id': { '$eq': indicator_id } }
		))
		if debug: print('Debugging:', stored, '\n\n')
		if stored != []:
			time = stored[0]['creation_time']
			name = stored[0]['indicator_value']
			return response(time, indicator_id, name), 200

		#retrieve data from world bank api
		url = worldbank_url + indicator_id
		payload = {'date': '2012:2017', 'format': 'json'}
		res = requests.get(url, params=payload)
		if debug:
			print('Debugging:', res.url, res.status_code, '\n\n')

		#this should probably never happen
		if res.status_code != 200:
			return {'error': 'unknown error occurred'}, 503

		#handle invalid indicator ids naively
		try:
			res.json()[1]
		except:
			return {'indicator_id': 'unknown'}, 400

		data = res.json()[1]
		name = '' #name of the indicator, as extracted from data
		entries = []

		#reformat indicator info for each country before storing
		for dat in data:
			name = dat['indicator']['value']
			formatted = {
				'country': dat['country']['value'],
				'date': dat['date'],
				'value': dat['value']
			}
			if debug: print('Debugging:', formatted, '\n\n')
			entries.append(formatted)

		#TODO: pagination

		#construct document to store in db
		time = get_time()
		to_store = {
			'collection_id': indicator_id,
			'indicator': indicator_id,
			'indicator_value': name,
			'creation_time': time,
			'entries': entries
		}
		if debug: print('Debugging: ', to_store, '\n\n')

		#store document in mongodb collection
		collection.insert(to_store)

		return response(time, indicator_id, name), 201

#construct json response based on arguments
def response(creation_time, indicator_id, indicator_name):
	res = {
		'location': '/collections/' + indicator_id,
		'collection_id': indicator_id,
		'creation_time': creation_time,
		'indicator': indicator_name
	}
	return res

#return the current time in iso format
def get_time():
	curr_time = datetime.datetime.now()
	formatted = curr_time.strftime('%Y-%m-%dT%H:%M:%SZ')
	return formatted

if __name__ == '__main__':

	#globals
	worldbank_version = 'v2'
	worldbank_url = 'http://api.worldbank.org/' + \
		worldbank_version + '/countries/all/indicators/'

	debug = True
	app.run(debug=True)
