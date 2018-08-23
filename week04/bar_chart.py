#!/usr/bin/python3
#Written by Costa Paraskevopoulos in August 2018
#Plot a bar chart of average length and width of sepals and petals

import pandas as pd
import matplotlib.pyplot as plt

def main():
	#read csv file into pandas dataframe
	df = pd.read_csv('iris.csv')

	#group the data based on the species & calculate the means
	means = df.groupby(by = 'species').mean()

	#plot a bar chart of the average lengths and widths
	means.plot.bar()
	plt.show()

if __name__ == '__main__':
	main()
