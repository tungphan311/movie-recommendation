from app.models import User, Movie

def valid_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        return False

    return True

def valid_movie(id):
    movie = Movie.query.get(id)

    if movie is None:
        return False

    return True