from app.models import Movie
from app.response import create_response
from app.search import query_index
from app import app, db
from routes.recommendation import get_movie_by_id
from sqlalchemy import desc, case


def search_movie(key, page):
    page_size = app.config['PAGE_SIZE']
    ids, total = Movie.search(key, page, page_size)
    # ids, total = query_index('movie', key, page, app.config['PAGE_SIZE'])

    response = []
    
    # for id in ids:
    #     movie = Movie.query.get(id)
    #     data = get_movie_by_id(id, movie.tmdb_id)
    #     response.append(data)

    if total < page_size:
        missing = page_size - total if total > 0 else page_size * page - total

        # create query
        search1 = "{}%".format(key)
        search2 = "%{}%".format(key)

        # order result by priory: title starts with key -> title contains key
        query = Movie.query.\
            filter(Movie.title.like(search1), Movie.title.like(search2))\
            .order_by(
                case(
                    [(Movie.title.like(search1), 0),
                     (Movie.title.like(search2), 1)],
                     else_=3))\
            .paginate(page, page_size, error_out=False)
        # movies = db.engine.execute(query)

        # for movie in movies:
        #     data = get_movie_by_id(movie.id, movie.tmdb_id)
        #     response.append(data)

        for q in query.items:
            response.append(q.id)

    return create_response(200, 'Success', data=response)
