from app import app, db
from app.models import User, Movie, Rating, Cast, Crew, Keyword, MovieKeywords, CreditCrews, CreditCasts, Genre, MovieGenres, Video
from app.search import add_to_index
from flask_script import Manager
import random
import string
import pandas as pd
import sqlite3 as sql
import datetime
import requests
from ast import literal_eval

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
    # if len(movies) == 0:
    mv = pd.read_csv("dataset/movies.csv")
    links = pd.read_csv("dataset/links.csv")

    for index, row in mv.iterrows():
        if row['movieId'] > 2389:
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

            result = requests.get(url)
            res = result.json() if result.status_code == 200 else None

            credits_res = requests.get(credits_url)
            credits = credits_res.json() if credits_res.status_code == 200 else None

            keywords_res = requests.get(keywords_url)
            keywords = keywords_res.json(
            )['keywords'] if keywords_res.status_code == 200 else []

            releases_res = requests.get(release_url)
            releases = releases_res.json() if releases_res.status_code == 200 else None

            videos_res = requests.get(video_url)
            videos = videos_res.json(
            )['results'] if videos_res.status_code == 200 else []

            poster_path = app.config['IMG_URL'] + \
                str(res['poster_path']
                    ) if res is not None else app.config['IMG_DEFAULT']
            backdrop_path = app.config['IMG_URL'] + \
                str(res['backdrop_path']
                    ) if res is not None else app.config['BACKDROP_DEFAULT']
            original_title = res['original_title'] if res is not None else row['title']
            vote_average = res['vote_average'] if res is not None else 0
            vote_count = res['vote_count'] if res is not None else 0
            runtime = res['runtime'] if res is not None else 0
            genres = res['genres'] if res is not None else []
            release_date = res['release_date'] if res is not None else '2000'
            overview = res['overview'] if res is not None else ''

            certification = "G"

            if releases is not None:
                release_results = releases['results']

                if len(release_results) > 0:
                    release_dates = release_results[0]['release_dates']

                    if len(release_dates) > 0:
                        certification = release_dates[0]['certification']

            casts = credits['cast'] if credits is not None else []
            crews = credits['crew'] if credits is not None else []

            total = 0
            rating_list = Rating.query.filter_by(movie_id=id).all()
            for r in rating_list:
                total += r.rating
            avg = total / len(rating_list) if len(rating_list) > 0 else 0

            m = Movie(id=id, title=row['title'], original_title=original_title, tmdb_id=tmdb_id, rating=avg,
                    backdrop_path=backdrop_path, poster_path=poster_path, release_date=release_date, runtime=runtime, overview=overview,
                    vote_average=vote_average, vote_count=vote_count, certification=certification)
            db.session.add(m)
            db.session.flush()
            db.session.refresh(m)

            for crew in crews:
                c = Crew.query.filter_by(name=crew['name']).first()

                if c is None:
                    new_crew = Crew(name=crew['name'])
                    db.session.add(new_crew)
                    db.session.flush()
                    db.session.refresh(new_crew)

                    credit_crew = CreditCrews(
                        movie_id=m.id, crew_id=new_crew.id, department=crew['department'])
                    db.session.add(credit_crew)
                else:
                    credit_crew = CreditCrews(
                        movie_id=m.id, crew_id=c.id, department=crew['department'])
                    db.session.add(credit_crew)

            for cast in casts:
                c = Cast.query.filter_by(name=cast['name']).first()

                if c is None:
                    image = app.config['IMG_URL'] + str(cast['profile_path'])
                    new_cast = Cast(name=cast['name'], image=image)
                    db.session.add(new_cast)
                    db.session.flush()
                    db.session.refresh(new_cast)

                    credit_cast = CreditCasts(character=cast['character'],
                                            movie_id=m.id, cast_id=new_cast.id, order=cast['order'])
                    db.session.add(credit_cast)
                else:
                    credit_cast = CreditCasts(character=cast['character'],
                                            movie_id=m.id, cast_id=c.id, order=cast['order'])
                    db.session.add(credit_cast)

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


@manager.command
def data():
    conn = sql.connect("app.db")
    movies = pd.read_sql_query(
        "select id, title from movie", conn)

    cast_list = []
    director_list = []
    keyword_list = []
    genre_list = []

    for index, row in movies.iterrows():
        id = row['id']

        casts = Cast.query\
            .join(CreditCasts, Cast.id == CreditCasts.cast_id)\
            .filter(CreditCasts.movie_id == id)\
            .filter(CreditCasts.order < 3)\
            .all()
        cast_names = [ cast.name for cast in casts ]
        cast_list.append(','.join(cast_names))

        keywords = Keyword.query\
            .join(MovieKeywords, MovieKeywords.keyword_id == Keyword.id)\
            .filter(MovieKeywords.movie_id == id)\
            .limit(3)\
            .all()
        keyword_names = [ keyword.name for keyword in keywords ]
        keyword_list.append(','.join(keyword_names))

        director = Crew.query\
            .join(CreditCrews, CreditCrews.crew_id == Crew.id)\
            .filter(CreditCrews.movie_id == id)\
            .filter(CreditCrews.department == "Directing")\
            .first()
        if director is None:
            director_list.append('')
        else:
            director_list.append(director.name)

        genres = Genre.query\
            .join(MovieGenres, MovieGenres.genre_id == Genre.id)\
            .filter(MovieGenres.movie_id == id)\
            .limit(3).all()
        genre_names = [ genre.name for genre in genres ]
        genre_list.append(','.join(genre_names))

    movies['cast'] = cast_list
    movies['director'] = director_list
    movies['keywords'] = keyword_list
    movies['genres'] = genre_list

    movies.to_csv('dataset/cb.csv', sep='\t', encoding='utf-8')

    print(movies.head())


if __name__ == "__main__":
    manager.run()
