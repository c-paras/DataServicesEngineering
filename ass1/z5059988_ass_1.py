#!/usr/bin/python3
#Written by Costa Paraskevopoulos in August 2018
#Simple data cleansing and visualization of Olympic Games medal tallies

import re
import pandas as pd
import matplotlib.pyplot as plt

def main():
	#question_0() #sample question
	df = question_1()
	question_2(df)
	df = question_3(df) #hide rubish column in subsequent output
	df = question_4(df) #hide nan values in subsequent output
	question_5(df)
	question_6(df)
	df = question_7(df) #save result from sorting
	question_8(df)
	question_9(df)

def question_0():
	print_header('Question 0: Display first 5 rows of first dataset')
	df = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1)
	print('First 5 rows:\n\n')
	print(df.head(5))

def question_1():
	print_header('Question 1: Merge the datasests')
	df1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1)
	df2 = pd.read_csv('Olympics_dataset2.csv', index_col=0, skiprows=1)
	df = pd.concat([df1, df2], axis=1, join_axes=[df1.index])

	#rename columns for convenience
	col_names = ['Rubish', 'SummerGames', 'SummerGold', 'SummerSilver',
		'SummerBronze', 'SummerTotal', 'WinterGames', 'WinterGold',
		'WinterSilver', 'WinterBronze', 'WinterTotal', 'TotalGames',
		'TotalGold', 'TotalSilver', 'TotalBronze', 'TotalMedals']
	df.columns = col_names

	#clean country names - remove leading whitespace
	df.set_index(df.index.map((lambda x: re.sub(r'^\s*', '', x))), inplace=True)

	print('First 5 rows:\n\n')
	print(df.head(5))
	return df

def question_2(df):
	print_header('Question 2: Display the first country')

	#the country is already set as the index in question_1
	#the index could be renamed here explicitly for clarity
	#df.index.rename('Country', inplace=True)

	print('The first country is: ' + str(df.index[0]))
	print('\n' + str(df.index[0]) + "'s medals are:")
	print(df.loc[df.index[0]])

def question_3(df):
	print_header('Question 3: Remove the Rubish column')
	df.drop(columns=['Rubish'], inplace=True)
	print('First 5 rows:\n\n')
	print(df.head(5))
	return df

def question_4(df):
	print_header('Question 4: Remove rows with NaNs')
	df.dropna(inplace=True)
	print('Last 10 rows:\n\n')
	print(df.tail(10))
	df = make_numeric(df) #convert all data to numeric
	return df

def question_5(df):
	print_header('Question 5: Most gold medals in summer games')
	df = df.drop(['Totals'])
	max_medals = df.SummerGold.max()
	country_details = df[df.SummerGold == max_medals]
	country = country_details.index.values[0]
	msg = 'The country with the most summer gold medals is %s, with %d medals'
	print(msg %(country, int(max_medals)))
	print('\nDetails:\n\n' + str(country_details))

def question_6(df):
	print_header('Question 6: Comparing summer and winter gold medal counts')
	df = df.drop(['Totals'])
	max_diff = (abs(df.SummerGold - df.WinterGold)).max()
	country_details = df[abs(df.SummerGold - df.WinterGold) ==
		(abs(df.SummerGold - df.WinterGold)).max()]
	country = country_details.index.values[0]
	msg = 'The country with the biggest difference between summer and winter'
	msg += ' gold medal counts is %s, with a difference of %d medals'
	print(msg %(country, int(max_diff)))
	print('\nDetails:\n\n' + str(country_details))

def question_7(df):
	print_header('Question 7: Sorted countries')
	df = df.sort_values(by=['TotalMedals'], ascending=False)
	df = df.drop(['Totals'])
	print('First 5 rows:\n\n')
	print(df.head(5))
	print('\n\n\nLast 5 rows:\n\n')
	print(df.tail(5))
	return df

def question_8(df):
	print_header('Question 8: Top 10 countries bar chart')
	top10 = df[0:10]
	top10 = top10[['SummerTotal', 'WinterTotal']]
	top10.columns = ['Summer Games', 'Winter Games']
	top10 = clean_index(top10)
	print(top10)
	top10.plot.barh(stacked=True, title='Medals for Summer and Winter Games')
	plt.tight_layout() #do not cut off labels
	plt.show()

def question_9(df):
	print_header('Question 9: Country comparison bar chart')
	countries = df[['WinterBronze', 'WinterSilver', 'WinterGold']]
	countries.columns = ['Bronze', 'Silver', 'Gold']
	subset = ['United States', 'Australia', 'Great Britain',
		'Japan', 'New Zealand']
	countries = clean_index(countries)
	countries = countries.loc[subset]
	print(countries)
	countries.plot.bar(title='Winter Games Comparison')
	plt.tight_layout() #do not cut off labels
	plt.show()

def make_numeric(df):
	#convert all data to numeric
	df = df.astype(str)
	df = df.applymap(lambda x: x.replace(',', ''))
	df = df.apply(pd.to_numeric)
	return df

def clean_index(df):
	#clean country names - simplify names by removing country codes
	fn = lambda x: re.sub(r' \(.*', '', x)
	df.set_index(df.index.map(fn), inplace=True)
	return df

def print_header(header):
	#print question header with separators
	print('\n\n')
	print('#' * len(header))
	print(header)
	print('#' * len(header))
	print('\n\n')

if __name__ == '__main__':
	df = pd.DataFrame()
	pd.set_option('expand_frame_repr', False) #print rows on one line
	main()
