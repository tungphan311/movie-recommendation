import pandas as pd
import sqlite3 as sql
import requests
from routes.CF import CF
from app.response import create_response
from app.models import Movie, MovieGenres, Genre, User, Recommend
from app import app


def recommend(id):
    user = User.query.get(id)

    if user is None:
        return create_response(400, "Tài khoản không tồn tại")

    recommends = Recommend.query.filter_by(user_id=id).all()

    if recommends is None:
        return create_response(200, "Lấy danh sách thành công", [])

    response = []

    for rec in recommends:
        data = get_movie_by_id(rec.movie_id)

        response.append(data)

    return create_response(200, "Lấy danh sách thành công", data=response)


def get_movie_by_id(id):
    movie = Movie.query.get(id)

    length = formatMovieLength(movie.runtime)
    genres = []

    movie_genres = MovieGenres.query.filter_by(movie_id=id).all()
    for gen in movie_genres:
        genre = Genre.query.get(gen.genre_id)
        genres.append({
            "id": genre.id,
            "name": genre.name
        })

    data = {
        "id": id,
        "avatar": movie.poster_path,
        "background": movie.backdrop_path,
        "name": movie.original_title,
        "score": movie.vote_average,
        "certification": movie.certification,
        "length": length,
        "genres": genres
    }

    return data


def formatMovieLength(length):
    hour = length / 60
    minute = length % 60

    return str(hour) + "h " + str(minute) + "m"
