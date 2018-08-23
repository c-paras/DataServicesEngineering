#!/usr/bin/python3
#Written by Costa Paraskevopoulos in August 2018
#Remove unwanted columns from a pandas dataframe

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

def main():
	#read csv file into pandas dataframe
	df = pd.read_csv('Books.csv')
	print_dataframe(df)

	#get number of NaNs in each column of dataframe
	print(df.isnull().sum().to_string())

	#drop unwanted columns
	to_drop = ['Edition Statement', 'Corporate Author',
		'Corporate Contributors', 'Former owner', 'Engraver', 'Contributors',
		'Issuance type', 'Shelfmarks']
	df.drop(columns=to_drop, inplace = True)
	#or: df = df.drop(columns=to_drop, axis = 1)

	print_dataframe(df)

if __name__ == '__main__':
	main()
