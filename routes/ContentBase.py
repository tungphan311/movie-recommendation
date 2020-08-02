import pandas as pd
import sqlite3 as sql
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

movies = pd.read_csv('dataset/cb.csv', sep='\t')

movies.drop('index', axis=1, inplace=True)

# Convert all strings to lowercase and strip names of spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        # Check if data exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''


# Declear which column applied clean_data
features = ['cast', 'keywords', 'director', 'genres']

for feat in features:
    movies[feat] = movies[feat].apply(clean_data)

# Create our "metadata soup", a string that contain all the metadata to feed to vectorizer
def create_soup(x):
    return x['keywords'] + ' ' + x['cast'] + ' ' + x['director'] + ' ' + x['genres']

movies['soup'] = movies.apply(create_soup, axis=1)

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(movies['soup'])
count_matrix = count_matrix.astype(np.float32)

# compute the cosine similarity matrix based on count_matrix
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# reset index of our main DataFrame and construct reverse mapping as before
movies = movies.reset_index()
indices = pd.Series(movies.index, index=movies['title'])


# Function that takes in movie title as input and output most similar movies
def get_recommendations(title, cosine_sim=cosine_sim):
    # get index of movie that matches title
    idx = indices[title]

    # get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # get score of the 10 most similar movies
    sim_scores = sim_scores[1:6]

    # get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    return movies[['id','title']].iloc[movie_indices]


