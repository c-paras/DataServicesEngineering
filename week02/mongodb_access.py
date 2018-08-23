#!/usr/bin/python3
#Written by Costa Paraskevopoulos in August 2018
#Load and manipulate a CSV file in MongoDB

import pandas as pd
from pymongo import MongoClient
import json

def main():
	#read csv file into pandas dataframe
	df = pd.read_csv('dataset.csv')

	#connect to the mongodb
	client = MongoClient()
	db = client.DemStats
	collection = db.stats

	#write dataframe to mongodb
	records = json.loads(df.T.to_json()).values()
	db.stats.insert(records)

	#query the db and load the data into a new dataframe
	df2 = pd.DataFrame(list(collection.find()))

	#write new dataframe to file to check
	df2.to_csv('output.csv')

if __name__ == '__main__':
	main()
