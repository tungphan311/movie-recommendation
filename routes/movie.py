from app.models import Movie, Rating, Review, User, Favorite, Genre, MovieGenres
from app.response import create_response
from app import db
from routes.validate import valid_user, valid_movie
from routes.recommendation import formatMovieLength
from routes.credit import get_credits, get_videos, get_first_review
import datetime


def movie_get_by_id(id, user_id):
    if not valid_user(user_id):
        return create_response(400, "Invalid user")

    if not valid_movie(id):
        return create_response(404, "Movie's not existed")

    # query from id
    movie = Movie.query.get(id)
    ratings = Rating.query.filter_by(movie_id=id).all()
    reviews = Review.query.filter_by(movie_id=id).all()
    rated = Rating.query.filter_by(movie_id=id, user_id=user_id).first()
    favorite = Favorite.query.filter_by(
        movie_id=movie.id, user_id=user_id).first()
    movie_genres = MovieGenres.query.filter_by(movie_id=id).all()


    # calculate avarage rating of movie with request id
    total_rating = 0
    for i in range(len(ratings)):
        total_rating += ratings[i].rating
    avg_rating = round(total_rating / len(ratings), 1)

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

    casts, director, writings = get_credits(movie.credit_id)
    videos = get_videos(movie.id)
    review = get_first_review(movie.id)

    res = {
        "rating": avg_rating,
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

    mes = "Get movie's info with id = " + str(id) + " successfully."

    return create_response(200, mes, data=res)


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

    db.session.commit()

    return create_response(200, "Rate film successfully")


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
    review = Review.query.filter_by(movie_id=movie.id, user_id=user_id).first()

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
