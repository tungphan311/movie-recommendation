import datetime
import pandas as pd
import sqlite3 as sql
from app.models import Recommend, User, Rating
from routes.CF import CF
from app import db
from sqlalchemy import desc

import atexit
from apscheduler.schedulers.background import BackgroundScheduler


def run_recommend_alg():
    print('running ...')

    user = db.session.query(User).order_by(User.id.desc()).first()
    nums_user = user.id

    conn = sql.connect("app.db")
    ratings = pd.read_sql_query(
        "select user_id, movie_id, rating from rating", conn)

    rate_train = ratings.to_numpy(dtype="Int64")

    rate_train[:, :2] -= 1

    rs = CF(rate_train, k=30)
    rs.fit()

    for id in range(nums_user):
        rating = Rating.query.filter_by(user_id=id+1).order_by(
            Rating.timestamp.desc()).first()
        date = rating.timestamp
        day = date.day
        month = date.month
        year = date.year

        today = datetime.datetime.now()

        if day + 1 == today.day and month == today.month and year == today.year:
            print('found')
            recommends = Recommend.query.filter_by(user_id=id+1).all()
            for i in range(len(recommends)):
                db.session.delete(recommends[i])

            recommended_items = rs.recommend(id)
            result = recommended_items[:10]

            for i in range(len(result)):
                movie_id = result[i][0] + 1

                rec = Recommend(user_id=id+1, movie_id=movie_id)
                db.session.add(rec)
        else:
            continue

    db.session.commit()


def recommend():
    hour = datetime.datetime.now().hour
    print('start')

    run_recommend_alg()
    print('finish')


schedule = BackgroundScheduler()
schedule.add_job(func=recommend, trigger="cron", hour="1", minute="0")
schedule.start()

atexit.register(lambda: schedule.shutdown())
