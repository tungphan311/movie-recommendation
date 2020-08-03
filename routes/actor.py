from app.models import Movie, Cast, CreditCasts, User
from app.response import create_response
from routes.movie import get_movie
from app import app


def actor_get_movies(id, page, user_id):
    page_size = app.config['PAGE_SIZE']
    user = User.query.get(user_id)

    if user is None:
        return create_response(400, 'Invalid request!')

    cast = Cast.query.get(id)

    movie_ids = CreditCasts.query\
        .filter_by(cast_id=id)\
        .paginate(page, page_size, error_out=False)

    total = CreditCasts.query.filter_by(cast_id=id).count()
    has_more = True if total > page * page_size else False

    movies = []

    for movie in movie_ids.items:
        res = get_movie(movie.movie_id, user_id)
        movies.append(res)

    response = {
        'name': cast.name,
        'has_more': has_more,
        'list': movies
    }

    return create_response(200, 'Success.', response)
