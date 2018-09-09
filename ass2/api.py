#!/usr/bin/python3
#Written by Costa Paraskevopoulos in September 2018
#RESTful API for country-specific economic indicator data
#Based on data provided by the World Bank API V2

import datetime
import requests
from flask import *
from pymongo import *
from flask_restplus import *

#globals
WORLDBANK_VERSION = 'v2'
WORLDBANK_BASE = 'http://api.worldbank.org/' + WORLDBANK_VERSION
MIN_YR = 2012
MAX_YR = 2017

#connect to mongodb database hosted on mlab
connection = MongoClient('ds149742.mlab.com', 49742)
db = connection['worldbank']
db.authenticate('ass2', 'comp9321')
collection = db.stats

#initialize flask app
app = Flask(__name__)
api = Api(app,
	version='1.0',
	default='Collections',
	title='Economic Indicator API',
	description='''
	RESTful API for country-specific economic indicator data
	Based on data provided by the World Bank API V2
	'''
)

@api.route('/collections/')
class Collections(Resource):
	params = api.model(
		'Resource',
		{ 'indicator_id': fields.String }
	)

	@api.expect(params)
	@api.response(201, 'Imported collection successfully')
	@api.response(200, 'Collection already imported previously')
	@api.response(400, 'Missing or unknown economic indicator')
	@api.response(503, 'Problem with World Bank API')
	@api.doc(description='Import economic indicator data from World Bank')
	def post(self):
		try:
			indicator_id = request.json['indicator_id']
		except:
			return {'error': 'missing parameter: indicator_id'}, 400

		#check if document for specified indicator already exists
		stored = list(collection.find(
			{ 'collection_id': { '$eq': indicator_id } }
		))
		if debug: print('Debugging:', stored, '\n\n')
		if stored != []:
			time = stored[0]['creation_time']
			name = stored[0]['indicator_value']
			return response(time, indicator_id, name), 200

		try:
			name, entries = get_world_bank_data(indicator_id)
		except Exception as err:
			#most likely error: unknown indicator_id
			err_type, err_msg, err_code = err.args
			return {err_type: err_msg}, err_code

		#construct document to store in db
		#some responses require different names for some fields
		#so store all field names and remove unwanted ones later
		time = get_time()
		to_store = {
			'location': '/collections/' + indicator_id,
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

	@api.response(200, 'Collections returned successfully')
	@api.doc(description='Return all available collections')
	def get(self):
		all_stats = []
		all_collections = list(collection.find())
		for c in all_collections:
			c.pop('_id')
			c.pop('entries')
			c.pop('indicator_value')
			all_stats.append(c)
		return all_stats, 200

@api.route('/collections/<string:collection_id>/')
@api.param('collection_id', 'An economic indicator, ' + \
	'chosen from ' + WORLDBANK_BASE + '/indicators/')
class Collection(Resource):
	@api.response(200, 'Collection successfully deleted')
	@api.response(404, 'Collection does not exist')
	@api.doc(description='Remove an existing collection')
	def delete(self, collection_id):
		query = { 'collection_id': { '$eq': collection_id } }

		#check if collection actually exists first
		indicators = list(collection.find(query))
		if indicators == []:
			return {collection_id: 'unknown collection'}, 404

		collection.delete_one(query)
		return {collection_id: 'collection removed'}, 200

	@api.response(200, 'Collection returned successfully')
	@api.response(404, 'Collection does not exist')
	@api.doc(description='Return data from a collection')
	def get(self, collection_id):
		query = { 'collection_id': { '$eq': collection_id } }

		#check if collection actually exists first
		indicators = list(collection.find(query))
		if indicators == []:
			return {collection_id: 'unknown collection'}, 404

		indicators[0].pop('_id')
		indicators[0].pop('location')
		return indicators[0], 200

@api.route('/collections/<string:collection_id>/<int:year>/<string:country>/')
@api.param('collection_id', 'An economic indicator, ' + \
	'chosen from ' + WORLDBANK_BASE + '/indicators/')
@api.param('year', 'Year of interest, between ' + \
	str(MIN_YR) + ' and ' + str(MAX_YR))
@api.param('country', 'Country of interest, ' + \
	'chosen from ' + WORLDBANK_BASE + '/countries/')
class Country(Resource):
	@api.response(200, 'Data returned successfully')
	@api.response(404, 'Collection does not exist')
	@api.response(400, 'Invalid parameters')
	@api.doc(description='Return indicator value for a country and year')
	def get(self, collection_id, year, country):
		query = { 'collection_id': { '$eq': collection_id } }

		#check if collection actually exists first
		indicators = list(collection.find(query))
		if indicators == []:
			return {collection_id: 'unknown collection'}, 404

		#then validate the provided year
		if year < MIN_YR or year > MAX_YR:
			return {year: 'invalid year'}, 400

		#now extract relevant info from the collection
		indicators[0].pop('_id')
		indicators[0].pop('location')
		indicators[0]['indicator'] = indicators[0].pop('indicator_value')
		indicators[0].pop('creation_time')

		#find the country and year requested
		found = False
		for entry in indicators[0]['entries']:
			if entry['country'] == country and entry['date'] == str(year):
				indicators[0]['country'] = country
				indicators[0]['year'] = str(year)
				indicators[0]['value'] = entry['value']
				found = True
				break
		if not found:
			return {country: 'unknown country'}, 400
		indicators[0].pop('entries')
		return indicators[0], 200

@api.route('/collections/<string:collection_id>/<int:year>/')
@api.param('collection_id', 'An economic indicator, ' + \
	'chosen from ' + WORLDBANK_BASE + '/indicators/')
@api.param('year', 'Year of interest, between ' + \
	str(MIN_YR) + ' and ' + str(MAX_YR))
class Year(Resource):
	@api.response(200, 'Data returned successfully')
	@api.response(404, 'Collection does not exist')
	@api.response(400, 'Invalid parameters')
	@api.doc(description='Return sorted indicator values for a specified year')
	def get(self, collection_id, year):
		query = { 'collection_id': { '$eq': collection_id } }

		#check if collection actually exists first
		indicators = list(collection.find(query))
		if indicators == []:
			return {collection_id: 'unknown collection'}, 404

		#then validate the provided year
		if year < MIN_YR or year > MAX_YR:
			return {year: 'invalid year'}, 400

		#now extract relevant info from the collection
		indicators[0].pop('_id')
		indicators[0].pop('location')
		indicators[0].pop('creation_time')
		indicators[0].pop('collection_id')

		#find the year requested
		entries = []
		for entry in indicators[0]['entries']:
			if entry['date'] == str(year):
				entries.append(entry)

		entries.sort(key = (lambda x: x['value']))
		#TODO: top10/bottom10 param
		indicators[0]['entries'] = entries
		return indicators[0], 200

#retrieve indicator data for all countries from world bank api
#return a list of indicator data for each country in the form:
#{'country': '', 'date': '', 'value': ''}
def get_world_bank_data(indicator_id):
	#human-readable name of indicator
	#extracted from response and returned to caller for storing
	name = ''

	#world bank paginates responses, assume 3 pages initially
	#update to real number of pages after 1st request
	num_pages = 3

	#retrieve data from world bank api page by page
	url = WORLDBANK_BASE + '/countries/all/indicators/' + indicator_id
	entries = []
	page_number = 1
	while page_number <= num_pages:
		payload = {
			'date': str(MIN_YR) + ':' + str(MAX_YR),
			'format': 'json',
			'page': page_number
		}
		res = requests.get(url, params=payload)
		if debug:
			print('Debugging:', res.url, res.status_code, '\n\n')

		#this should probably never happen
		if res.status_code != 200:
			raise Exception('error', 'unknown error occurred', 503)

		#handle invalid indicator ids naively
		try:
			res.json()[1]
		except:
			raise Exception('indicator_id', 'unknown', 400)

		#speed up while debugging, by only processing a subset
		if not debug:
			num_pages = res.json()[0]['pages']
		data = res.json()[1]

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

		page_number += 1
	return name, entries

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
	debug = True #TODO: disable debug flag
	app.run(debug=True)
