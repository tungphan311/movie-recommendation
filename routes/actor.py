from app.models import Movie, Cast, CreditCasts, User, Genre, MovieGenres
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


def get_all_genres():
    genres = Genre.query.all()
    response = [{'id': genre.id, 'name': genre.name} for genre in genres]

    return create_response(200, 'Success.', response)


def genre_get_movies(id, page, user_id):
    page_size = app.config['PAGE_SIZE']
    user = User.query.get(user_id)

    if user is None:
        return create_response(400, 'Invalid request!')

    if id == 0:
        movie_ids = Movie.query.order_by(Movie.rating.desc(
        ), Movie.vote_average.desc()).paginate(page, page_size, error_out=False)

        total = Movie.query.count()
        has_more = True if total > page * page_size else False

        movies = []

        for movie in movie_ids.items:
            res = get_movie(movie.id, user_id)
            movies.append(res)

        response = {
            'has_more': has_more,
            'list': movies
        }
        return create_response(200, 'Success.', response)
    elif id > 0:
        movie_ids = MovieGenres.query\
            .join(Movie, Movie.id == MovieGenres.movie_id)\
            .filter(MovieGenres.genre_id == id)\
            .order_by(Movie.rating.desc(), Movie.vote_average.desc())\
            .paginate(page, page_size, error_out=False)

        total = MovieGenres.query\
            .join(Movie, Movie.id == MovieGenres.movie_id)\
            .filter(MovieGenres.genre_id == id)\
            .order_by(Movie.rating.desc(), Movie.vote_average.desc()).count()
        has_more = True if total > page * page_size else False

        movies = []

        for movie in movie_ids.items:
            res = get_movie(movie.movie_id, user_id)
            movies.append(res)

        response = {
            'has_more': has_more,
            'list': movies
        }
        return create_response(200, 'Success.', response)
