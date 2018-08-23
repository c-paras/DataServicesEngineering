#!/usr/bin/python3
#Written by Costa Paraskevopoulos in August 2018
#Plot side-by-side scatter charts of length and width of sepels and petals

import pandas as pd
import matplotlib.pyplot as plt

def main():
	#read csv file into pandas dataframe
	df = pd.read_csv('iris.csv')

	#split dataset into 3 dataframes based on the 3 species
	species1 = df.query('species == "setosa"')
	species2 = df.query('species == "versicolor"')
	species3 = df.query('species == "virginica"')

	#create subplots for the side-by-side scatter plots
	fig, axes = plt.subplots(nrows = 1, ncols = 2)

	#plot overlayed scatter charts of sepal length and sepal width
	species1.plot.scatter(x = 'sepal_length', y = 'sepal_width',
		ax = axes[0], c = 'blue', label = 'setosa')
	species2.plot.scatter(x = 'sepal_length', y = 'sepal_width',
		ax = axes[0], c = 'green', label = 'versicolor')
	species3.plot.scatter(x = 'sepal_length', y = 'sepal_width',
		ax = axes[0], c = 'red', label = 'virginica')

	#plot overlayed scatter charts of petal length and petal width
	species1.plot.scatter(x = 'petal_length', y = 'petal_width',
		ax = axes[1], c = 'blue', label = 'setosa')
	species2.plot.scatter(x = 'petal_length', y = 'petal_width',
		ax = axes[1], c = 'green', label = 'versicolor')
	species3.plot.scatter(x = 'petal_length', y = 'petal_width',
		ax = axes[1], c = 'red', label = 'virginica')

	#show the plot
	plt.show()

if __name__ == '__main__':
	main()
