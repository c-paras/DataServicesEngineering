#!/usr/bin/python3
#Written by Costa Paraskevopoulos in September 2018
#Perform a cross validation of various classifiers

import pandas as pd
from sklearn.neighbors import *
from sklearn.metrics import *
from sklearn.tree import *
from sklearn.svm import *
from sklearn.linear_model import *
from sklearn.naive_bayes import *
from sklearn.discriminant_analysis import *
from sklearn.model_selection import *

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
	train_samples = train[train.columns[0:4]].values
	train_labels = train[train.columns[4:5]].values.flatten()

	#extract test data and labels
	test_samples = test[test.columns[0:4]].values
	test_labels = test[test.columns[4:5]].values.flatten()

	algos = [
		'KNeighborsClassifier',
		'DecisionTreeClassifier',
		'LinearDiscriminantAnalysis',
		'LogisticRegression',
		'GaussianNB',
		'SVC',
	]
	scores = dict.fromkeys(algos, 0)

	for algo in algos:
		score = cross_val_score(eval(algo + '()'), train_samples, train_labels, cv=5)
		scores[algo] = score.mean()

	for k, v in sorted(scores.items(), key=lambda x: float(x[1]), reverse=True):
		print(str(k) + ':', round(v, 4))

if __name__ == '__main__':
	main()
