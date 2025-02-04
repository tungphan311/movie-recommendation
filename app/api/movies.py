from app import app
from flask_jwt_extended import jwt_required
from app.api.helpers import get_authorization
from flask import request
from routes.movie import movie_get_by_id, movie_rating, remove_rating, user_review, get_user_review,\
    movie_get_similar, get_popular_movies, get_top_rated_movies, movie_get_review, movie_get_review
from routes.user import add_movie_to_favorite


@app.route("/api/movies/<int:id>")
@jwt_required
def get_movie_by_id(id=0):
    user_id, _ = get_authorization()

    return movie_get_by_id(id, user_id)

@app.route("/api/movies/<int:id>/reviews")
@jwt_required
def get_movie_review(id=0):
    user_id, _ = get_authorization()
    page = request.args.get('page', default=1, type=int)

    return movie_get_review(id, user_id, page)


@app.route("/api/movies/<int:id>/similar")
def get_similar_movie(id=0):
    return movie_get_similar(id)


@app.route("/api/movies/<int:id>/rate", methods=['POST'])
@jwt_required
def rate_movie(id=0):
    user_id, _ = get_authorization()

    data = request.get_json()
    rated = data.get("rated", 0)
    return movie_rating(id, user_id, rated)


@app.route("/api/movies/<int:id>/rate", methods=['DELETE'])
@jwt_required
def delete_movie_rating(id=0):
    user_id, _ = get_authorization()
    
    return remove_rating(id, user_id)


@app.route("/api/movies/<int:id>/reviews", methods=['POST'])
@jwt_required
def add_review(id=0):
    user_id, _ = get_authorization()

    data = request.get_json()
    rated = data.get("rated", 0)
    headline = data.get("headline", "")
    body = data.get("body", "")

    # validate request data:
    if len(headline) > 0 and len(body) > 50 and len(body) < 500:
        return user_review(user_id, id, headline, body, rated)
    else:
        return create_response(400, "Request data invalid")


@app.route("/api/movies/<int:id>/review")
@jwt_required
def get_review(id=0):
    user_id, _ = get_authorization()
    
    return get_user_review(id, user_id)


@app.route("/api/movies/<int:id>/favorites", methods=['POST'])
@jwt_required
def add_to_favorites(id=0):
    user_id, _ = get_authorization()

    return add_movie_to_favorite(user_id, id)


@app.route("/api/movies/popular")
@jwt_required
def get_popular():
    user_id, _ = get_authorization()

    return get_popular_movies(user_id)


@app.route("/api/movies/top-rated")
@jwt_required
def get_top_rated():
    user_id, _ = get_authorization()

    return get_top_rated_movies(user_id)
