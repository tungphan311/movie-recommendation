from app.models import Movie, Rating, Review, User
from app.response import create_response


def movie_get_by_id(id, user_id):
    # query from id
    movie = Movie.query.filter_by(tmdb_id=id).first()
    ratings = Rating.query.filter_by(movie_id=movie.id).all()
    reviews = Review.query.filter_by(movie_id=movie.id).all()
    rated = Rating.query.filter_by(movie_id=movie.id, user_id=user_id).first()

    # calculate avarage rating of movie with request id
    total_rating = 0
    for i in range(len(ratings)):
        total_rating += ratings[i].rating
    avg_rating = round(total_rating / len(ratings), 1)

    # return score of user_id rate movie_id
    user_rate = 0 if rated is None else rated.rating

    res = {
        "rating": avg_rating,
        "total_rating": len(ratings),
        "reviews": reviews,
        "user_rate": user_rate
    }

    mes = "Lấy thông tin phim với id = " + str(id) + " thành công."

    return create_response(200, mes, data=res)
