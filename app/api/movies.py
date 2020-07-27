from app import app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.helpers import get_authorization
from flask import request
from routes.movie import movie_get_by_id, movie_rating, remove_rating, user_review, get_user_review


@app.route("/api/movies/<int:id>")
@jwt_required
def get_movie_by_id(id=0):
    user_id, _ = get_authorization()

    return movie_get_by_id(id, user_id)


@app.route("/api/movies/<int:id>/rate", methods=['POST'])
def rate_movie(id=0):
    data = request.get_json()
    user_id = data.get("user_id", 0)
    rated = data.get("rated", 0)
    return movie_rating(id, user_id, rated)


@app.route("/api/movies/<int:id>/rate/<int:user_id>", methods=['DELETE'])
def delete_movie_rating(id=0, user_id=0):
    return remove_rating(id, user_id)


@app.route("/api/movies/<int:id>/reviews", methods=['POST'])
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


@app.route("/api/movies/<int:id>/review/<user_id>")
def get_movie_review(id=0, user_id=0):
    return get_user_review(id, user_id)


@app.route("/api/movies/<int:id>/favorites", methods=['POST'])
def add_to_favorites():
    data = request.get_json()
    user_id = data.get("user_id", 0)
    movie_id = data.get("movie_id", 0)

    return add_movie_to_favorite(user_id, movie_id)
