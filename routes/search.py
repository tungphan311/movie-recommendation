from app.models import Movie, Genre, MovieGenres, Cast
from app.response import create_response
from app.search import query_index
from app import app, db
from routes.recommendation import get_movie_by_id
from routes.movie import get_movie
from sqlalchemy import desc, case
from unidecode import unidecode


def search_movie(key, page, searchType, short, user_id):
    newKey = unidecode(key)

    response = { 'query': key }

    if searchType == 'All' or searchType == 'Titles':
        movies = query_movie(newKey, page, short, user_id)
        response['title'] = movies

    if searchType == 'Celebs' or searchType == 'All':
        casts = query_cast(newKey, page, short)
        response['celebs'] = casts

    return create_response(200, 'Success', data=response)


def query_movie(key, page, short, user_id):
    page_size = app.config['PAGE_SIZE']

    # create query
    search1 = "{}%".format(key)
    search2 = "%{}%".format(key)


    if short == 1:
        result = []
        movies = Movie.query.filter(Movie.title.like(search1))\
                .order_by(Movie.rating.desc())\
                .limit(3)\
                .all()

        for movie in movies:
            res = get_movie_short(movie.id)
            result.append(res)

        return result
    else:
        # order result by priory: title starts with key -> title contains key
        query = Movie.query.\
            filter(Movie.title.like(search1), Movie.title.like(search2))\
            .order_by(
                case(
                    [(Movie.title.like(search1), 0),
                        (Movie.title.like(search2), 1)],
                    else_=3))\
            .paginate(page, page_size, error_out=False)

        total = Movie.query.\
            filter(Movie.title.like(search1), Movie.title.like(search2))\
            .order_by(
                case(
                    [(Movie.title.like(search1), 0),
                        (Movie.title.like(search2), 1)],
                    else_=3))\
            .count()

        response = []
        
        for q in query.items:
            res = get_movie(q.id, user_id)
            response.append(res)

        has_more = True if total > page_size else False

        return { 'has_more': has_more, 'list': response }


def query_cast(key, page, short):
    # create query
    search1 = "{}%".format(key)
    search2 = "%{}%".format(key)

    result = []
    if short == 1:
        casts = Cast.query.filter(Cast.name.like(search1))\
            .limit(3)\
            .all()

        cast_list = [{ 'id': cast.id, 'name': cast.name, 'avatar': cast.image } for cast in casts]
        return cast_list



def get_movie_short(id):
    movie = Movie.query.get(id)
    release_date = movie.release_date
    year = release_date[:4]
    genres = Genre.query\
        .join(MovieGenres, MovieGenres.genre_id == Genre.id)\
        .filter(MovieGenres.movie_id == id)\
        .limit(3).all()

    genre_list = [gen.name for gen in genres]

    return {
        'id': id,
        'avatar': movie.poster_path,
        'name': movie.title,
        'year': year,
        'genres': genre_list
    }

def search_keyword(key, page):
    print('as')
    page_size = app.config['PAGE_SIZE']
    ids, total = query_index('keyword', key, page, app.config['PAGE_SIZE'])

    print(ids)

