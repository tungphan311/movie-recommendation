from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    ratings = db.relationship('Rating', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    genres = db.Column(db.String(200))
    tmdb_id = db.Column(db.Integer)
    ratings = db.relationship('Rating', backref='movie', lazy='dynamic')

    def __repr__(self):
        return '<Movie {}>'.format(self.body)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    def __repr__(self):
        return '<Rating {}>'.format(self.body)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(128))
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    def __repr__(self):
        return '<Review {}>'.format(self.body)