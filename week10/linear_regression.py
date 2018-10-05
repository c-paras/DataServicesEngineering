#!/usr/bin/python3
#Written by Costa Paraskevopoulos in October 2018
#Train and test a linear regression model on a diet dataset

import pandas as pd
from sklearn.linear_model import *
from sklearn.metrics import *

def main():
	#read in diet dataset
	df = pd.read_csv('diet.csv')

	#and split into two components
	split = int(0.7 * len(df))
	df = df.sample(frac=1, random_state=50).reset_index(drop=True)

	#one for training
	train = df[:split]

	#and one for testing
	test = df[split:]

	#extract training data
	x = train[train.columns[0:6]].values
	y = train[train.columns[6:7]].values.flatten()

	#train the linear regression model
	regression = LinearRegression().fit(x, y)

	#extract test data and labels
	x = test[test.columns[0:6]].values
	y = test[test.columns[6:7]].values.flatten()

	#test the model
	i = 0
	predictions = []
	for sample in x:
		prediction = str(round(regression.predict([sample])[0], 1)).ljust(12)
		predictions.append(float(prediction.strip()))
		actual = str(y[i]).ljust(12)
		print('predicted=%s actual=%s' %(prediction, actual), end='')
		diff = round(float(prediction.strip()) - float(y[i]), 1)
		print('diff=' + str(diff))
		i += 1

	print('Mean square error:', round(mean_squared_error(y, predictions), 2))

if __name__ == '__main__':
	main()
