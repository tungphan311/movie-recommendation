from app.models import Movie
from app.response import create_response
from app.search import query_index
from app import app, db
from routes.recommendation import get_movie_by_id
from sqlalchemy import desc


def search_movie(key, page):
    page_size = app.config['PAGE_SIZE']
    ids, total = Movie.search(key, page, page_size)
    # ids, total = query_index('movie', key, page, app.config['PAGE_SIZE'])

    response = []
    
    for id in ids:
        movie = Movie.query.get(id)
        data = get_movie_by_id(id, movie.tmdb_id)
        response.append(data)

    if total < page_size:
        missing = page_size - total
        search = "%{}%".format(key)
        query = "SELECT * FROM movie WHERE title LIKE '%{}%' ORDER BY rating desc LIMIT {}".format(key, missing)
        movies = db.engine.execute(query)

        for movie in movies:
            data = get_movie_by_id(movie.id, movie.tmdb_id)
            response.append(data)

    return create_response(200, 'Success', data=response, total=page_size)
