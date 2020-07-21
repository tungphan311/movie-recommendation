from app import app
from flask import request
from flask_cors import cross_origin
from routes.auth import auth_register, auth_login
from routes.recommendation import recommend
from routes.movie import movie_get_by_id, movie_rating, remove_rating, user_review, get_user_review
from routes.user import add_movie_to_favorite
from routes.search import search_movie
from app.response import create_response


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


# authentication route
@app.route("/api/register", methods=['POST'])
@cross_origin()
def register():
    return auth_register()


@app.route("/api/login", methods=['POST'])
@cross_origin()
def login():
    return auth_login()


@app.route("/api/recommend/<int:id>")
@cross_origin()
def get_recommend(id=0):
    return recommend(id)


@app.route("/api/movies/<id>", methods=['POST'])
@cross_origin()
def get_movie_by_id(id=0):
    data = request.get_json()
    user_id = data.get("user_id", 0)

    if user_id == 0:
        return create_response(400, "Request info invalid")

    return movie_get_by_id(id, user_id)


@app.route("/api/movies/<id>/rate", methods=['POST'])
@cross_origin()
def rate_movie(id=0):
    data = request.get_json()
    user_id = data.get("user_id", 0)
    rated = data.get("rated", 0)
    return movie_rating(id, user_id, rated)


@app.route("/api/movies/<id>/rate/<user_id>", methods=['DELETE'])
@cross_origin()
def delete_movie_rating(id=0, user_id=0):
    return remove_rating(id, user_id)


@app.route("/api/favorites", methods=['POST'])
@cross_origin()
def add_to_favorites():
    data = request.get_json()
    user_id = data.get("user_id", 0)
    movie_id = data.get("movie_id", 0)

    return add_movie_to_favorite(user_id, movie_id)


@app.route("/api/movies/<id>/reviews", methods=['POST'])
@cross_origin()
def add_review(id=0):
    data = request.get_json()
    user_id = data.get("user_id", 0)
    headline = data.get("headline", "")
    body = data.get("body", "")

    # validate request data:
    if len(headline) > 0 and len(body) > 50 and len(body) < 500:
        return user_review(user_id, id, headline, body)
    else:
        return create_response(400, "Request data invalid")


@app.route("/api/movies/<id>/review/<user_id>")
@cross_origin()
def get_movie_review(id=0, user_id=0):
    return get_user_review(id, user_id)


@app.route("/api/search")
@cross_origin()
def search():
    data = request.args
    page = data.get("page", 1, type=int)
    key = data.get("key", "", type=str)

    return search_movie(key, page)
