from app.models import Movie, Favorite, User
from app.response import create_response
from app import db
from routes.logger import Logger


def add_movie_to_favorite(user_id, movie_id):
    movie = Movie.query.get(movie_id)
    user = User.query.get(user_id)

    if movie is None or user is None: 
        return create_response(400, "Invalid request")

    favorite = Favorite.query.filter_by(
        user_id=user_id, movie_id=movie.id).first()

    if favorite is None:
        f = Favorite(user_id=user_id, movie_id=movie.id)
        db.session.add(f)

        logger = Logger(user_id=user_id, action_type_id=8, movie_id=movie_id)
        logger.create_log()
    else:
        db.session.delete(favorite)

        logger = Logger(user_id=user_id, action_type_id=9, movie_id=movie_id)
        logger.create_log()

    db.session.commit()

    return create_response(200, "Success")
