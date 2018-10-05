#!/usr/bin/python3
#Written by Costa Paraskevopoulos in October 2018
#Perform a K-Means Clustering on the iris plant dataset

import pandas as pd
import numpy as np
from sklearn.cluster import *
import matplotlib.pyplot as plt

def main():
	#read in iris dataset
	df = pd.read_csv('iris.csv')

	#extract data without labels
	samples = df[df.columns[0:4]].values

	#perform k-means clustering
	kmeans = KMeans(n_clusters=3, random_state=0).fit(samples)

	#plot the clusters in different colors on a scatterplot
	colors = list(map(choose_color, list(kmeans.labels_)))
	#ax = df.plot.scatter(x='petal_length', y='petal_width', c=colors)
	fig, ax = plt.subplots()
	x = np.array(df['petal_length'].values)
	y = np.array(df['petal_width'].values)
	i = 0
	for c in np.unique(colors):
		indexes = []
		for j in range(0, len(colors)):
			if colors[j] == c: indexes.append(j)
		ax.scatter(x[indexes], y[indexes], label='Cluster ' + str(i))
		i += 1
	ax.legend()

	#label data points with actual label
	df['species'] = df['species'].apply(lambda x: x[:4])
	df[['petal_length', 'petal_width', 'species']].apply(lambda x: ax.text(*x), axis=1)

	plt.show()

#map each cluster name to a different color
def choose_color(c):
	if c == 0:
		return 'red'
	elif c == 1:
		return 'green'
	else:
		return 'blue'

if __name__ == '__main__':
	main()
