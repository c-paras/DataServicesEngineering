#!/usr/bin/python3
#Written by Costa Paraskevopoulos in October 2018
#Perform a Agglomerative Clustering on a diet dataset

import pandas as pd
import numpy as np
from sklearn.cluster import *
import matplotlib.pyplot as plt

def main():
	#read in diet dataset
	df = pd.read_csv('diet.csv')

	#extract data without labels
	samples = df.drop('Diet', axis=1)

	#perform agglomerative clustering
	clustering = AgglomerativeClustering(n_clusters=3).fit(samples)

	#plot the clusters in different colors on a scatterplot
	colors = list(map(choose_color, list(clustering.labels_)))
	fig, ax = plt.subplots()
	x = np.array(df['pre.weight'].values)
	y = np.array(df['weight6weeks'].values)
	i = 0
	for c in np.unique(colors):
		indexes = []
		for j in range(0, len(colors)):
			if colors[j] == c: indexes.append(j)
		ax.scatter(x[indexes], y[indexes], label='Cluster ' + str(i))
		i += 1
	ax.legend()

	#label data points with actual label
	df['Diet'] = df['Diet'].apply(lambda x: 'Diet ' + str(x))
	df[['pre.weight', 'weight6weeks', 'Diet']].apply(lambda x: ax.text(*x), axis=1)

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
