import pandas as pd
import json, requests
from MySQLdb import *

movies = {}

cnx = connect(user='testprojects', password='Testing123!',host='den1.mysql4.gear.host',database='testprojects')
cursor = cnx.cursor()

def savetodb(dct):
	add_movie = 'INSERT INTO movies \
	(title, year, runtime, genre, rating) \
	VALUES ("{}", "{}",\
	"{}", "{}", "{}"\
	 \
	 );'.format(movies[dct]['title'],movies[dct]['year'],
	 	movies[dct]['runtime'],movies[dct]['genre(s)'],
	 	movies[dct]['rating'])
	cursor.execute(add_movie)
	cnx.commit()
df = pd.read_table('data.tsv',low_memory=False)
dfr = pd.read_table('data_ratings.tsv', low_memory=False)

dftuples =  df.itertuples()


for i in dftuples:
	try:
		#print(f"id: {i[1]} title: {i[3]} year:{i[6]} runtime: {i[8]} genres: {i[-1]}")
		movies[i[1]] = {'title':i[3],'year':int(i[6]),'runtime':int(i[8]),'genre(s)':i[-1]}
	except:
		continue


for i in dfr.itertuples():
	try:
		movies[i[1]]['rating'] = float(i[2])
	except:
		continue
	
	
for i in movies:
	try:
		print(i)
		savetodb(i)
	except:
		continue
#sorted_df = df.sort_index()
#print(sorted_df)





"""
tags = ['Title','Year','Rated','Released',
       'Runtime','Director','Writer', 'Actors','Country','Ratings']
"""


