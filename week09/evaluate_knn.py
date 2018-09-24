#!/usr/bin/python3
#Written by Costa Paraskevopoulos in September 2018
#Train and test a KNN classifer for the iris plant dataset
#Perform a basic evaluation the KNN classifier

import pandas as pd
from sklearn.neighbors import *
from sklearn.metrics import *

def main():
	#read in iris dataset
	df = pd.read_csv('iris.csv')

	#and split into two components
	split = int(0.7 * len(df))
	df = df.sample(frac=1, random_state=50).reset_index(drop=True)

	#one for training
	train = df[:split]

	#and one for testing
	test = df[split:]

	#extract training data and labels
	samples = train[train.columns[0:4]].values
	labels = train[train.columns[4:5]].values.flatten()

	#train the knn classifier
	neighbors = KNeighborsClassifier(n_neighbors=3)
	neighbors.fit(samples, labels)

	#extract test data and labels
	samples = test[test.columns[0:4]].values
	labels = test[test.columns[4:5]].values.flatten()

	#test the knn classifier
	i = 0
	predicted = []
	for sample in samples:
		prediction = neighbors.predict([sample])[0].ljust(15)
		predicted.append(prediction.strip())
		actual = labels[i].ljust(15)
		print('predicted=%s actual=%s' %(prediction, actual), end='')
		if prediction.strip() != labels[i]:
			print('Incorrect', end='')
		print('')
		i += 1

	#evaluate the knn classifier
	print('\nEvaluation:\n')
	print('Accuracy: ' + str(round(accuracy_score(labels, predicted), 2)))
	print('Confusion Matrix:')
	print(confusion_matrix(labels, predicted))
	print('Mean Precision: ' + str(round(precision_score(labels, predicted, average='macro'), 2)))
	print('Recall Score: ' + str(round(recall_score(labels, predicted, average='macro'), 2)))

if __name__ == '__main__':
	main()
