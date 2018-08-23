#!/usr/bin/python3
#Written by Costa Paraskevopoulos in August 2018
#Normalize rows in a pandas dataframe

import pandas as pd

def print_dataframe(df):
	#get all the headers in the dataset
	fields = list(df)

	#print the columns of the dataframe
	print(fields)
	print('')

	#print the rows of the dataframe
	for index, row in df.iterrows():
		for field in fields:
			print(row[field], ' ', end='')
		print('\n\n')

def clean_place_of_pub(place):
	if 'London' in place: place = 'London'
	place = place.replace('-', '')
	return place

def clean_date_of_pub(date):
	return date.str.extract(r'([0-9]{4})', expand = False)

def main():
	#read csv file into pandas dataframe
	df = pd.read_csv('Books.csv')
	print_dataframe(df)

	#simplify place of publication
	df['Place of Publication'] = df['Place of Publication'].apply(clean_place_of_pub)

	#simply date of publication
	df['Date of Publication'] = clean_date_of_pub(df['Date of Publication'])
	df['Date of Publication'] = pd.to_numeric(df['Date of Publication'])
	df['Date of Publication'] = df['Date of Publication'].fillna(0)

	#change all column names to use_ rather than ' ' for word separation
	df.columns = [col.replace(' ', '_') for col in df.columns]

	#query for those books published in london after 1866
	df.query('Place_of_Publication == "London" and Date_of_Publication > 1866', inplace = True)

	print_dataframe(df)

if __name__ == '__main__':
	main()
