#!/usr/bin/python3
#Written by Costa Paraskevopoulos in August 2018
#Load and manipulate a CSV file in a pandas dataframe

import pandas as pd

def main():
	#read csv file into pandas dataframe
	df = pd.read_csv('dataset.csv')

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

	#save the dataframe to a csv file
	df.to_csv('output.csv')

if __name__ == '__main__':
	main()
