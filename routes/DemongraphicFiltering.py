import pandas as pd
import sqlite3 as sql
from app.models import Movie, Review, Rating, Favorite, MovieGenres, Rating, Genre
from routes.credit import get_credits, get_videos, get_first_review
from routes.recommendation import formatMovieLength

conn = sql.connect("app.db")
movies = pd.read_sql_query(
    "select id, title, vote_count, vote_average from movie", conn)

C = movies['vote_average'].mean()
m = movies['vote_count'].quantile(0.9)

q_movies = movies.copy().loc[movies['vote_count'] >= m]


def weighted_rating(x, m=m, C=C):
    v = x['vote_count']
    R = x['vote_average']
    # Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * C)


# Define a new feature 'score' and calculate its value with `weighted_rating()
q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

#Sort movies based on score calculated above
q_movies = q_movies.sort_values('score', ascending=False)

def get_most_popular(user_id):
    most_popular = q_movies.head(24)
    response = []

    for index, row in most_popular.iterrows():
        id = row['id']

        res = get_movie(id, user_id)
        response.append(res)

    return response


def get_movie(id, user_id):
    # query from id
    movie = Movie.query.get(id)
    reviews = Review.query.filter_by(movie_id=id).all()
    rated = Rating.query.filter_by(movie_id=id, user_id=user_id).first()
    favorite = Favorite.query.filter_by(
        movie_id=movie.id, user_id=user_id).first()
    movie_genres = MovieGenres.query.filter_by(movie_id=id).all()
    ratings = Rating.query.filter_by(movie_id=id).all()

    # return score of user_id rate movie_id
    user_rate = 0 if rated is None else rated.rating
    isFavorite = True if favorite is not None else False

    genres = []

    for gen in movie_genres:
        genre = Genre.query.get(gen.genre_id)
        genres.append({
            "id": genre.id,
            "name": genre.name
        })

    casts, director, writings = get_credits(movie.id)
    videos = get_videos(movie.id)
    review = get_first_review(movie.id)

    res = {
        "rating": round(movie.rating, 1),
        "total_rating": len(ratings),
        "user_rate": user_rate,
        "is_favorite": isFavorite,
        "id": id,
        "avatar": movie.poster_path,
        "background": movie.backdrop_path,
        "name": movie.original_title,
        "score": movie.vote_average,
        "certification": movie.certification,
        "length": formatMovieLength(movie.runtime),
        "overview": movie.overview,
        "genres": genres,
        "release_date": movie.release_date,
        "casts": casts,
        "director": director,
        "writers": writings,
        "videos": videos,
        "review": review,
    }

    return res
