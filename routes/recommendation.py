import pandas as pd
import sqlite3 as sql
import requests
from routes.CF import CF
from app.response import create_response
from app.models import Movie
from app import app


def recommend(id):
    if id == 0:
        return create_response(400, "Tài khoản không hợp lệ")

    conn = sql.connect("app.db")
    ratings = pd.read_sql_query("select user_id, movie_id, rating from rating", conn)

    rate_train = ratings.to_numpy(dtype="Int64")

    rate_train[:, :2] -= 1

    rs = CF(rate_train, k = 30)
    rs.fit()

    recommended_items = rs.recommend(id - 1)
    result = recommended_items[:5]

    response = []

    for i in range(10):
        if len(result) > i:
            movie_id = result[i] + 1
            movie = Movie.query.get(movie_id)

            data = get_movie_by_id(i+1, movie.tmdb_id)
            
            response.append(data)

    return create_response(200, "Lấy danh sách thành công", data=response)

def get_movie_by_id(id, movieId):
    url = "https://api.themoviedb.org/3/movie/" + \
        str(movieId) + "?api_key=" + app.config['API_KEY']

    res = requests.get(url).json()

    avatar = app.config['IMG_URL'] + \
        res['poster_path'] if res['poster_path'] is not None else app.config['IMG_DEFAULT']
    background = app.config['IMG_URL'] + \
        res['backdrop_path'] if res['backdrop_path'] is not None else app.config['BACKDROP_DEFAULT']
    name = res['original_title']
    score = res['vote_average']
    limit = '18+' if res['adult'] == True else '13+'
    length = formatMovieLength(res['runtime'])
    genres = res['genres']

    data = { 
        "id": id, 
        "movId": movieId, 
        "avatar": avatar, 
        "background": background, 
        "name": name,
        "score": score,
        "limit": limit,
        "length": length,
        "genres": genres
    }

    return data

def formatMovieLength(length):
    hour = length / 60
    minute = length % 60

    return str(hour) + "h " + str(minute) + "m"
