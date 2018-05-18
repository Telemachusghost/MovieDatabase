"""
This script reads in an imdb database file and parses it putting it into a database for further educational
use
Derick Falk
"""

import pandas as pd
from MySQLdb import *

movies = {}

# Connects to your database replace with you username, password, and hostname
cnx = connect(user=<user>, password=<password>,host=<hostname>,database=<database>)
cursor = cnx.cursor()

# Method that saves a movie to the database column names and structure may vary
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

# Used pandas to read the tsvs	
df = pd.read_table('data.tsv',low_memory=False)
dfr = pd.read_table('data_ratings.tsv', low_memory=False)

# Convert the columns into tuples
dftuples =  df.itertuples()

# Breaks up the datafile and makes a dictionary based on id
for i in dftuples:
	try:
		movies[i[1]] = {'title':i[3],'year':int(i[6]),'runtime':int(i[8]),'genre(s)':i[-1]}
	except:
		continue

# Adds the ratings from a seperate tsv
for i in dfr.itertuples():
	try:
		movies[i[1]]['rating'] = float(i[2])
	except:
		continue
	
# Goes through and saves the movies to a database
for i in movies:
	try:
		print(i)
		savetodb(i)
	except:
		continue


