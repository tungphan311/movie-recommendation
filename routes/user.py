from app.models import Movie, Favorite, User
from app.response import create_response
from app import db, app
from routes.logger import Logger
from routes.movie import get_movie


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


def get_favorite_movies(user_id):
    user = User.query.get(user_id)
    page_size = app.config['PAGE_SIZE']
    page = 1

    if user is None:
        return create_response(400, "Invalid request")

    favorites = Favorite.query.filter_by(
        user_id=user_id).paginate(page, page_size, error_out=False)
    count = Favorite.query.filter_by(user_id=user_id).count()

    response = []

    for favorite in favorites.items:
        res = get_movie(favorite.movie_id, user_id)
        response.append(res)

    has_more = True if count > page_size * page else False

    return create_response(200, 'Success.', { 'has_more': has_more, 'list': response })
