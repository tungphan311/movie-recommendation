from app.models import Movie, Rating, Review, User, Favorite
from app.response import create_response
from app import db
import datetime


def movie_get_by_id(id, user_id):
    # query from id
    movie = Movie.query.filter_by(tmdb_id=id).first()
    ratings = Rating.query.filter_by(movie_id=movie.id).all()
    reviews = Review.query.filter_by(movie_id=movie.id).all()
    rated = Rating.query.filter_by(movie_id=movie.id, user_id=user_id).first()
    favorite = Favorite.query.filter_by(
        movie_id=movie.id, user_id=user_id).first()

    # calculate avarage rating of movie with request id
    total_rating = 0
    for i in range(len(ratings)):
        total_rating += ratings[i].rating
    avg_rating = round(total_rating / len(ratings), 1)

    # return score of user_id rate movie_id
    user_rate = 0 if rated is None else rated.rating

    isFavorite = True if favorite is not None else False

    res = {
        "rating": avg_rating,
        "total_rating": len(ratings),
        "reviews": reviews,
        "user_rate": user_rate,
        "is_favorite": isFavorite
    }

    mes = "Get movie's info with id = " + str(id) + " successfully."

    return create_response(200, mes, data=res)


def movie_rating(id, user_id, rated):
    # query from request info
    movie = Movie.query.filter_by(tmdb_id=id).first()
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
    movie = Movie.query.filter_by(tmdb_id=id).first()
    rating = Rating.query.filter_by(movie_id=movie.id, user_id=user_id).first()

    if rating is not None:
        db.session.delete(rating)
        db.session.commit()

    return create_response(200, "Delete movie's rating successfully")


def user_review(user_id, id, headline, body):
    # query from request info
    movie = Movie.query.filter_by(tmdb_id=id).first()
    review = Review.query.filter_by(movie_id=movie.id, user_id=user_id).first()

    if review is not None:
        review.headline = headline
        review.body = body
        db.session.add(review)
    else:
        r = Review(headline=headline, body=body,
                   user_id=user_id, movie_id=movie.id)
        db.session.add(r)

    db.session.commit()
    return create_response(200, "Update review for movie successfully")
