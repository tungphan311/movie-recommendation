from app import app, db
from app.models import User, Movie, Rating, Credit, Cast, Crew, Keyword, MovieKeywords, CreditCrews, CreditCasts, Genre, MovieGenres, Video
from app.search import add_to_index
from flask_script import Manager
import random
import string
import pandas as pd
import datetime
import requests

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

    ratings = Rating.query.all()
    if len(ratings) == 0:
        rt = pd.read_csv("dataset/ratings.csv")

        for index, row in rt.iterrows():
            time = datetime.datetime.fromtimestamp(1347517370)
            rating = int(round(row['rating']))

            r = Rating(rating=rating, timestamp=time,
                       user_id=row['userId'], movie_id=row['movieId'])
            db.session.add(r)

    movies = Movie.query.all()
    if len(movies) == 0:
        mv = pd.read_csv("dataset/movies.csv")
        links = pd.read_csv("dataset/links.csv")

        for index, row in mv.iterrows():
            tmdb_id = links.loc[index, 'tmdbId']
            id = row['movieId']

            url = "https://api.themoviedb.org/3/movie/" + \
                str(tmdb_id) + "?api_key=" + app.config['API_KEY']
            credits_url = "https://api.themoviedb.org/3/movie/" + \
                str(tmdb_id) + "/credits?api_key=" + app.config['API_KEY']
            keywords_url = "https://api.themoviedb.org/3/movie/" + \
                str(tmdb_id) + "/keywords?api_key=" + app.config['API_KEY']
            release_url = "https://api.themoviedb.org/3/movie/" + \
                str(tmdb_id) + "/release_dates?api_key=" + \
                app.config['API_KEY']
            video_url = "https://api.themoviedb.org/3/movie/" + \
                str(tmdb_id) + "/videos?api_key=" + \
                app.config['API_KEY']

            res = requests.get(url).json()
            credits = requests.get(credits_url).json()
            keywords_json = requests.get(keywords_url).json()
            keywords = keywords_json['keywords']
            releases = requests.get(release_url).json()
            videos_json = requests.get(video_url).json()
            videos = videos_json['results']

            poster_path = app.config['IMG_URL'] + \
                res['poster_path'] if res['poster_path'] is not None else app.config['IMG_DEFAULT']
            backdrop_path = app.config['IMG_URL'] + \
                res['backdrop_path'] if res['backdrop_path'] is not None else app.config['BACKDROP_DEFAULT']
            original_title = res['original_title']
            vote_average = res['vote_average']
            vote_count = res['vote_count']
            runtime = res['runtime']
            genres = res['genres']
            release_date = res['release_date']
            overview = res['overview']

            release_dates = releases['results'][0]['release_dates']
            certification = release_dates[0]['certification']

            casts = credits['cast']
            crews = credits['crew']

            credit = Credit()
            db.session.add(credit)
            db.session.flush()
            db.session.refresh(credit)

            for crew in crews:
                c = Crew.query.filter_by(name=crew['name']).first()

                if c is None:
                    new_crew = Crew(name=crew['name'], department=crew['department'])
                    db.session.add(new_crew)
                    db.session.flush()
                    db.session.refresh(new_crew)

                    credit_crew = CreditCrews(
                        credit_id=credit.id, crew_id=new_crew.id)
                    db.session.add(credit_crew)
                else:
                    credit_crew = CreditCrews(
                        credit_id=credit.id, crew_id=c.id)
                    db.session.add(credit_crew)
            
            for cast in casts:
                c = Cast.query.filter_by(name=cast['name']).first()

                if c is None:
                    image = app.config['IMG_URL'] + str(cast['profile_path'])
                    new_cast = Cast(character=cast['character'], name=cast['name'],
                            image=image)
                    db.session.add(new_cast)
                    db.session.flush()
                    db.session.refresh(new_cast)

                    credit_cast = CreditCasts(
                        credit_id=credit.id, cast_id=new_cast.id, order=cast['order'])
                    db.session.add(credit_cast)
                else:
                    credit_cast = CreditCasts(
                        credit_id=credit.id, cast_id=c.id, order=cast['order'])
                    db.session.add(credit_cast)

            total = 0
            rating_list = Rating.query.filter_by(movie_id=id).all()
            for r in rating_list:
                total += r.rating
            avg = total / len(rating_list) if len(rating_list) > 0 else 0

            m = Movie(id=id, title=row['title'], original_title=original_title, tmdb_id=tmdb_id, rating=avg, 
                    backdrop_path=backdrop_path, poster_path=poster_path, release_date=release_date, runtime=runtime, overview=overview, 
                        vote_average=vote_average, vote_count=vote_count, credit_id=credit.id, certification=certification)
            db.session.add(m)
            db.session.flush()
            db.session.refresh(m)

            for video in videos:
                v = Video(key=video['key'], name=video['name'], movie_id=m.id)
                db.session.add(v)

            for keyword in keywords:
                k = Keyword.query.filter_by(name=keyword['name']).first()

                if k is None:
                    new_keyword = Keyword(name=keyword['name'])
                    db.session.add(new_keyword)
                    db.session.flush()
                    db.session.refresh(new_keyword)

                    key = MovieKeywords(
                        movie_id=m.id, keyword_id=new_keyword.id)
                    db.session.add(key)
                else:
                    key = MovieKeywords(movie_id=m.id, keyword_id=k.id)
                    db.session.add(key)

            for genre in genres:
                g = Genre.query.filter_by(name=genre['name']).first()

                if g is None:
                    new_genre = Genre(name=genre['name'])
                    db.session.add(new_genre)
                    db.session.flush()
                    db.session.refresh(new_genre)

                    gen = MovieGenres(
                        movie_id=m.id, genre_id=new_genre.id)
                    db.session.add(gen)
                else:
                    gen = MovieGenres(movie_id=m.id, genre_id=g.id)
                    db.session.add(gen)
    
    db.session.commit()

if __name__ == "__main__":
    manager.run()
