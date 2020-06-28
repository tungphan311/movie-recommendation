from app import app, db
from app.models import User, Movie, Rating
from flask_script import Manager
import random
import string
import pandas as pd
import datetime

manager = Manager(app)


def randomEmail():
    email = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    return email + "@gmail.com"


@manager.command
def seed():
    users = User.query.all()
    if len(users) == 0:
        for i in range(1, 611):
            email = randomEmail()
            u = User(id=i, email=email)
            u.hash_password("123456")
            db.session.add(u)

    movies = Movie.query.all()
    if len(movies) == 0:
        mv = pd.read_csv("dataset/movies.csv")
        links = pd.read_csv("dataset/links.csv")

        for index, row in mv.iterrows():
            tmdb_id = links.loc[index, 'tmdbId']
            m = Movie(id=row['movieId'], title=row['title'],
                      genres=row['genres'], tmdb_id=tmdb_id)
            db.session.add(m)

    ratings = Rating.query.all()
    if len(ratings) == 0:
        rt = pd.read_csv("dataset/ratings.csv")

        for index, row in rt.iterrows():
            time = datetime.datetime.fromtimestamp(1347517370)
            rating = int(round(row['rating']))

            r = Rating(rating=rating, timestamp=time,
                       user_id=row['userId'], movie_id=row['movieId'])
            db.session.add(r)

    db.session.commit()


if __name__ == "__main__":
    manager.run()
