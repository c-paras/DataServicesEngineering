#!/usr/bin/python3
#Written by Costa Paraskevopoulos in September 2018
#RESTful API for country-specific economic indicator data
#Based on data provided by the World Bank API V2

import datetime
import requests
from pymongo import *
from flask_restplus import *
from flask import *

connection_params = {
	'user': 'ass2',
	'password': 'comp9321',
	'host': 'ds149742.mlab.com',
	'port': 49742,
	'namespace': 'worldbank',
}

connection = MongoClient('ds149742.mlab.com', 49742)
db = connection['worldbank']
db.authenticate('ass2', 'comp9321')
collection = db.stats

app = Flask(__name__)
api = Api(app, version='1.0',
	default='Collections',
	title='Economic Indicator API',
	description='''
	RESTful API for country-specific economic indicator data
	Based on data provided by the World Bank API V2
	''')

def get_time():
	curr_time = datetime.datetime.now()
	formatted = curr_time.strftime('%Y-%m-%dT%H:%M:%SZ')
	return formatted

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
	@api.doc(description='Import economic indicator data from World Bank')
	def post(self):
		params = request.json

		url = worldbank_url + params['indicator_id']
		payload = {'date': '2012:2017', 'format': 'json'}
		res = requests.get(url, params=payload)

		if debug:
			print('Debugging:', res.url, res.status_code, '\n\n')

		#TODO: if invalid indicator id - 400
		data = res.json()[1]
		indicator_name = ''
		entries = []
		for dat in data:
			indicator_name = dat['indicator']['value']
			formatted = {
				'country': dat['country']['value'],
				'date': dat['date'],
				'value': dat['value']
			}
			if debug: print('Debugging:', formatted, '\n\n')
			entries.append(formatted)

		#TODO: pagination

		i = params['indicator_id']
		creation_time = get_time()
		to_store = {
			'collection_id': str(i),
			'indicator': params['indicator_id'],
			'indicator_value': indicator_name,
			'creation_time': creation_time,
			'entries': entries
		}
		if debug: print('Debugging: ', to_store, '\n\n')

		collection.insert(to_store)
		stored = list(collection.find())
		print('Debugging:', stored, '\n\n')

		res = {
			'location': '/collections/' + str(i),
			'collection_id': str(i),
			'creation_time': creation_time,
			'indicator': params['indicator_id']
		}
		if debug: print('Debugging:', res)
		return res, 201 #TODO: if already exists - 200

def main():
	pass

if __name__ == '__main__':
	main()
	worldbank_version = 'v2'
	worldbank_url = 'http://api.worldbank.org/' + \
		worldbank_version + '/countries/all/indicators/'
	debug = True
	app.run(debug=True)
