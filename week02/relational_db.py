#!/usr/bin/python3
#Written by Costa Paraskevopoulos in August 2018
#Load and manipulate a CSV file in SQL

import pandas as pd
import sqlite3

def main():
	#read csv file into pandas dataframe
	df = pd.read_csv('dataset.csv')

	#store the datafram in an sqlite db
	conn = sqlite3.connect('output.db')
	df.to_sql('DemStats', conn, if_exists='replace')

	#query database and load daat into a new dataframe
	query = '''SELECT "JURISDICTION NAME"
		FROM DemStats
		WHERE "COUNT MALE" > 100;'''
	df = pd.read_sql_query(query, conn)
	conn.close()

	#print the resulting stats
	for location in df['JURISDICTION NAME']:
		print(location)
	
if __name__ == '__main__':
	main()
