#!/usr/bin/python3
#Written by Costa Paraskevopoulos in August 2018
#Plot a pie chart of book publication locations

import pandas as pd
import matplotlib.pyplot as plt

def clean_place_of_pub(place):
	if 'London' in place: place = 'London'
	place = place.replace('-', '')
	return place

def main():
	#read csv file into pandas dataframe
	df = pd.read_csv('Books.csv')

	#simplify place of publication
	df['Place of Publication'] = df['Place of Publication'].apply(clean_place_of_pub)

	#plot the counts of publication cities on a pie chart
	counts = df['Place of Publication'].value_counts()
	counts.plot.pie()
	plt.show()

if __name__ == '__main__':
	main()
