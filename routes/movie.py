from app.models import Movie, Rating, Review, User, Favorite, Genre, MovieGenres
from app.response import create_response
from app import db, app
from routes.validate import valid_user, valid_movie
from routes.recommendation import formatMovieLength
from routes.credit import get_credits, get_videos, get_first_review
from routes.ContentBase import get_recommendations
from routes.DemongraphicFiltering import get_most_popular
import datetime


def movie_get_by_id(id, user_id):
    if not valid_user(user_id):
        return create_response(400, "Invalid user")

    if not valid_movie(id):
        return create_response(404, "Movie's not existed")

    res = get_movie(id, user_id)

    mes = "Get movie's info with id = " + str(id) + " successfully."

    return create_response(200, mes, data=res)


def get_movie(id, user_id):
    # query from id
    movie = Movie.query.get(id)
    reviews = Review.query.filter_by(movie_id=id).all()
    rated = Rating.query.filter_by(movie_id=id, user_id=user_id).first()
    favorite = Favorite.query.filter_by(
        movie_id=movie.id, user_id=user_id).first()
    movie_genres = MovieGenres.query.filter_by(movie_id=id).all()
    ratings = Rating.query.filter_by(movie_id=id).all()

    # return score of user_id rate movie_id
    user_rate = 0 if rated is None else rated.rating
    isFavorite = True if favorite is not None else False

    genres = []

    for gen in movie_genres:
        genre = Genre.query.get(gen.genre_id)
        genres.append({
            "id": genre.id,
            "name": genre.name
        })

    casts, director, writings = get_credits(movie.id)
    videos = get_videos(movie.id)
    review = get_first_review(movie.id)

    res = {
        "rating": round(movie.rating, 1),
        "total_rating": len(ratings),
        "user_rate": user_rate,
        "is_favorite": isFavorite,
        "id": id,
        "avatar": movie.poster_path,
        "background": movie.backdrop_path,
        "name": movie.original_title,
        "score": movie.vote_average,
        "certification": movie.certification,
        "length": formatMovieLength(movie.runtime),
        "overview": movie.overview,
        "genres": genres,
        "release_date": movie.release_date,
        "casts": casts,
        "director": director,
        "writers": writings,
        "videos": videos,
        "review": review,
    }

    return res

def movie_rating(id, user_id, rated):
    # query from request info
    movie = Movie.query.get(id)

    if movie is None:
        return create_response(400, "Movie is not exist")

    rating = Rating.query.filter_by(movie_id=movie.id, user_id=user_id).first()

    if rating is None:
        r = Rating(rating=rated, user_id=user_id, movie_id=movie.id)
        db.session.add(r)
    else:
        rating.rating = rated
        rating.timestamp = datetime.datetime.utcnow()
        db.session.add(rating)

    db.session.flush()

    new_rating = calc_rating(id)
    movie.rating = new_rating
    db.session.add(movie)

    db.session.commit()

    return create_response(200, "Rate film successfully")


def calc_rating(id):
    ratings = Rating.query.filter_by(movie_id=id).all()

    # calculate avarage rating of movie with request id
    total_rating = 0
    for i in range(len(ratings)):
        total_rating += ratings[i].rating
    avg_rating = total_rating / len(ratings)

    return avg_rating


def remove_rating(id, user_id):
    # query from request info
    movie = Movie.query.get(id)

    if movie is None:
        return create_response(400, "Movie is not exist")
        
    rating = Rating.query.filter_by(movie_id=movie.id, user_id=user_id).first()

    if rating is not None:
        db.session.delete(rating)
        db.session.commit()

    return create_response(200, "Delete movie's rating successfully")


def user_review(user_id, id, headline, body, rated):
    # query from request info
    movie = Movie.query.get(id)

    if movie is None:
        return create_response(400, "Movie is not exist")

    review = Review.query.filter_by(movie_id=movie.id, user_id=user_id).first()

    if review is not None:
        review.headline = headline
        review.body = body
        db.session.add(review)
    else:
        r = Review(headline=headline, body=body,
                   user_id=user_id, movie_id=movie.id)
        db.session.add(r)

    rating = Rating.query.filter_by(movie_id=movie.id, user_id=user_id).first()

    if rating is None:
        r = Rating(rating=rated, user_id=user_id, movie_id=movie.id)
        db.session.add(r)
    else:
        rating.rating = rated
        rating.timestamp = datetime.datetime.utcnow()
        db.session.add(rating)

    db.session.commit()
    return create_response(200, "Update review for movie successfully")


def get_user_review(id, user_id):
    # query from request info
    movie = Movie.query.get(id)
    user = User.query.get(user_id)

    if movie is None or user is None:
        return create_response(400, "Invalid request")

    review = Review.query.filter_by(movie_id=id, user_id=user_id).first()

    res = {}

    if review is not None:
        res = {
            "headline": review.headline,
            "body": review.body
        }
    else:
        res = {
            "headline": "",
            "body": ""
        }

    return create_response(200, "Success", data=res)


def movie_get_similar(id):
    movie = Movie.query.get(id)

    if movie is None:
        return create_response(400, 'Movie is not exist')
    
    movies = get_recommendations(movie.title)

    similars = []

    for index, row in movies.iterrows():
        movie_id = row['id']

        mov = Movie.query.get(movie_id)
        genres = Genre.query\
                .join(MovieGenres, MovieGenres.genre_id == Genre.id)\
                .filter(MovieGenres.movie_id == movie_id)\
                .limit(3).all()

        mov_genres = [ gen.name for gen in genres ]
            
        similars.append({ 
            'id': movie_id,
            'title': mov.title,
            'img': mov.poster_path,
            'rating': round(mov.rating, 1),
            'certification': mov.certification,
            'overview': mov.overview,
            'genres': mov_genres
        })

    return create_response(200, 'Get similar movie success', similars)


def get_popular_movies(user_id):
    page_size = app.config['PAGE_SIZE']

    # get trending now
    trendings = get_most_popular(user_id)
    trending_now = {
        'rowId': 3,
        'title': 'Trending Now',
        'list': trendings
    }

    return create_response(200, 'Success.', trending_now)


def get_top_rated_movies(user_id):
    page_size = app.config['PAGE_SIZE']

    # get top rated movies
    list_top_rated = Movie.query.order_by(
        Movie.rating.desc()).paginate(1, page_size, error_out=False)
    top_rateds = []
    for movie in list_top_rated.items:
        res = get_movie(movie.id, user_id)
        top_rateds.append(res)
    top_rated = {
        'rowId': 2,
        'title': 'Top Rated',
        'list': top_rateds
    }
    return create_response(200, 'Success.', top_rated)
