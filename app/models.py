from app import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)

        return ids, total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    ratings = db.relationship('Rating', backref='author', lazy='dynamic')
    reviews = db.relationship('Review', backref='review', lazy='dynamic')
    views = db.relationship('View', backref='view', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='author', lazy='dynamic')
    recommends = db.relationship('Recommend', backref='target', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Recommend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    def __repr__(self):
        return '<Recommend {}>'.format(self.movie_id)


class Movie(SearchableMixin, db.Model):
    __tablename__ = 'movie'
    __searchable__ = ['title']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    genres = db.Column(db.String(200))
    tmdb_id = db.Column(db.Integer)
    rating = db.Column(db.Float)
    ratings = db.relationship('Rating', backref='movie', lazy='dynamic')
    reviews = db.relationship('Review', backref='movie_review', lazy='dynamic')
    views = db.relationship('View', backref='movie_view', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='movie', lazy='dynamic')
    recommends = db.relationship('Recommend', backref='movie', lazy='dynamic')

    def __repr__(self):
        return '<Movie {}>'.format(self.ratings)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    def __repr__(self):
        return '<Rating {}>'.format(self.rating)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(128))
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    def __repr__(self):
        return '<Review {}>'.format(self.body)


class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    def __repr__(self):
        return '<View {}>'.format(self.user_id)


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    def __repr__(self):
        return '<Favorite {}>'.format(self.user_id)
