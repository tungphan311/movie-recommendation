import pandas as pd
import sqlite3 as sql
import requests
from routes.CF import CF
from app.response import create_response
from app.models import Movie, MovieGenres, Genre, User, Recommend, Video, Favorite, Rating
from app import app
from routes.credit import get_credits


def recommend(id):
    user = User.query.get(id)

    if user is None:
        return create_response(400, "Tài khoản không tồn tại")

    recommends = Recommend.query.filter_by(user_id=id).all()

    if recommends is None:
        return create_response(200, "Lấy danh sách thành công", [])

    response = []

    for rec in recommends:
        data = get_movie_by_id(rec.movie_id, id)

        response.append(data)

    return create_response(200, "Lấy danh sách thành công", data=response)


def get_movie_by_id(id, user_id):
    movie = Movie.query.get(id)
    ratings = Rating.query.filter_by(movie_id=id).all()
    rated = Rating.query.filter_by(movie_id=id, user_id=user_id).first()

    length = formatMovieLength(movie.runtime)
    genres = []

    movie_genres = MovieGenres.query.filter_by(movie_id=id).all()
    for gen in movie_genres:
        genre = Genre.query.get(gen.genre_id)
        genres.append({
            "id": genre.id,
            "name": genre.name
        })

    video = Video.query.filter_by(movie_id=id).first()
    video_url = app.config['VIDEO_URL'] + video.key if video is not None else ""

    # check if user with id added this movie to favorite list
    favorite = Favorite.query.filter_by(
        movie_id=id, user_id=user_id).first()
    isFavorite = True if favorite is not None else False
    user_rate = 0 if rated is None else rated.rating

    casts, director, writings = get_credits(movie.id)

    data = {
        "id": id,
        "background": movie.backdrop_path,
        "name": movie.original_title,
        "score": movie.vote_average,
        "certification": movie.certification,
        "length": length,
        "genres": genres,
        "rating": round(movie.rating, 1),
        "video": video_url,
        "is_favorite": isFavorite,
        "total_rating": len(ratings),
        "user_rate": user_rate,
        "overview": movie.overview,
        "release_date": movie.release_date,
        "casts": casts,
        "director": director,
        "writers": writings,
    }

    return data


def formatMovieLength(length):
    hour = int(length / 60)
    minute = length % 60

    return str(hour) + "h " + str(minute) + "m"
