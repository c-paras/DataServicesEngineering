#!/usr/bin/python3
#Written by Costa Paraskevopoulos in August 2018
#Plot scatter charts of length and width of sepels and petals

import pandas as pd
import matplotlib.pyplot as plt

def main():
	#read csv file into pandas dataframe
	df = pd.read_csv('iris.csv')

	#split dataset into 3 dataframes based on the 3 species
	species1 = df.query('species == "setosa"')
	species2 = df.query('species == "versicolor"')
	species3 = df.query('species == "virginica"')

	#plot overlayed scatter charts of sepal length and sepal width
	ax = species1.plot.scatter(x = 'sepal_length',
		y = 'sepal_width', c = 'blue', label = 'setosa')
	ax = species2.plot.scatter(x = 'sepal_length',
		y = 'sepal_width', ax = ax, c = 'green', label = 'versicolor')
	ax = species3.plot.scatter(x = 'sepal_length',
		y = 'sepal_width', ax = ax, c = 'red', label = 'virginica')
	plt.show()

	#plot overlayed scatter charts of petal length and petal width
	ax = species1.plot.scatter(x = 'petal_length',
		y = 'petal_width', c = 'blue', label = 'setosa')
	ax = species2.plot.scatter(x = 'petal_length',
		y = 'petal_width', ax = ax, c = 'green', label = 'versicolor')
	ax = species3.plot.scatter(x = 'petal_length',
		y = 'petal_width', ax = ax, c = 'red', label = 'virginica')
	plt.show()

if __name__ == '__main__':
	main()
