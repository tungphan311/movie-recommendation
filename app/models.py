from app import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    ratings = db.relationship('Rating', backref='author', lazy='dynamic')
    reviews = db.relationship('Review', backref='review', lazy='dynamic')
    views = db.relationship('View', backref='view', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    genres = db.Column(db.String(200))
    tmdb_id = db.Column(db.Integer)
    ratings = db.relationship('Rating', backref='movie', lazy='dynamic')
    reviews = db.relationship('Review', backref='movie_review', lazy='dynamic')
    views = db.relationship('View', backref='movie_view', lazy='dynamic')

    def __repr__(self):
        return '<Movie {}>'.format(self.body)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
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


class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    def __repr__(self):
        return '<View {}>'.format(self.body)
