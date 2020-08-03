from app import app
from flask import request
from routes.search import search_movie
from flask_jwt_extended import jwt_required
from app.api.helpers import get_authorization
from routes.actor import actor_get_movies

@app.route("/api/movies")
@jwt_required
def search():
    user_id, _ = get_authorization()

    data = request.args
    page = data.get("page", 1, type=int)
    key = data.get("query", "", type=str)
    searchType = data.get("type", "All", type=str)
    short = data.get("short", 1, type=int)

    return search_movie(key, page, searchType, short, user_id)


@app.route("/api/actor/<int:id>")
@jwt_required
def actor_id(id=0):
    user_id, _ = get_authorization()

    data = request.args
    page = data.get("page", 1, type=int)

    return actor_get_movies(id, page, user_id)
