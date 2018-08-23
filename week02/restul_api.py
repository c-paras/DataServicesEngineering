#!/usr/bin/python3
#Written by Costa Paraskevopoulos in August 2018
#Load data from an API request into a pandas dataframe

import pandas as pd
from pandas.io.json import json_normalize
import json
import requests

def main():
	#download json data from api
	url = 'https://data.cityofnewyork.us/api/views/kku6-nxdu/rows.json'
	res = requests.get(url=url, params='')
	data = res.json()

	#load json into pandas dataframe
	df = json_normalize(data)
	json = data['data'] #ignore meta
	columns = []
	for c in data['meta']['view']['columns']:
		#get names of columns
		columns.append(c['name'])
	df = pd.DataFrame(data=json, columns=columns)

	#write new dataframe to file to check
	df.to_csv('output.csv')

if __name__ == '__main__':
	main()
