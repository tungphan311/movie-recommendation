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
    # ratings = db.relationship('Rating', backref='author', lazy=True)
    # reviews = db.relationship('Review', backref='review', lazy=True)
    # views = db.relationship('View', backref='view', lazy=True)
    # favorites = db.relationship('Favorite', backref='author', lazy=True)
    # recommends = db.relationship('Recommend', backref='target', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Recommend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=True)
    movie_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Recommend {}>'.format(self.movie_id)

class Movie(SearchableMixin, db.Model):
    __tablename__ = 'movie'
    __searchable__ = ['title']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    original_title = db.Column(db.String(128))
    tmdb_id = db.Column(db.Integer)
    rating = db.Column(db.Float)
    vote_average = db.Column(db.Float)
    vote_count = db.Column(db.Integer)
    backdrop_path = db.Column(db.String(500))
    poster_path = db.Column(db.String(500))
    release_date = db.Column(db.String(500))
    runtime = db.Column(db.Integer)
    overview = db.Column(db.String)
    certification = db.Column(db.String(120))
    credit_id = db.Column(db.Integer)
    # ratings = db.relationship('Rating', backref='movie', lazy=True)
    # reviews = db.relationship('Review', backref='movie_review', lazy=True)
    # views = db.relationship('View', backref='movie_view', lazy=True)
    # favorites = db.relationship('Favorite', backref='movie', lazy=True)
    # recommends = db.relationship('Recommend', backref='movie', lazy=True)
    # genres = db.relationship('Genre', backref='movie', lazy=True)
    # keywords = db.relationship('Keyword', backref='movie', lazy=True)
    # credit = db.relationship('Credit', uselist=False, back_populates='movie')
    # videos = db.relationship('Video', backref='movie', lazy=True)

    def __repr__(self):
        return '<Movie {}>'.format(self.ratings)

class MovieGenres(db.Model):
    __tablename__ = 'movie_genres'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    genre_id = db.Column(db.Integer)
    # movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    # genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)

class MovieKeywords(db.Model):
    __tablename__ = 'movie_keywords'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    keyword_id = db.Column(db.Integer)
    # movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    # keyword_id = db.Column(db.Integer, db.ForeignKey(
    #     'keyword.id'), nullable=False)

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return '<Genre {}>'.format(self.name)

class Keyword(db.Model):
    __tablename__ = 'keyword'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return '<Keyword {}>'.format(self.name)

class Credit(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class CreditCrews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credit_id = db.Column(db.Integer)
    crew_id = db.Column(db.Integer)

class CreditCasts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credit_id = db.Column(db.Integer)
    cast_id = db.Column(db.Integer)
    order = db.Column(db.Integer)

class Crew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(120))
    name = db.Column(db.String(120))
    # credit_id = db.Column(db.Integer, db.ForeignKey('credit.id'), nullable=False)

    def __repr__(self):
        return '<Crew {}>'.format(self.name)

class Cast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.String(120))
    name = db.Column(db.String(120))
    image = db.Column(db.String(120))
    # credit_id = db.Column(db.Integer, db.ForeignKey(
    #     'credit.id'), nullable=False)

    def __repr__(self):
        return '<Cast {}>'.format(self.name)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(120))
    name = db.Column(db.String(120))
    movie_id = db.Column(db.Integer, nullable=False)
    # movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    def __repr__(self):
        return '<Video {}>'.format(self.name)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Rating {}>'.format(self.rating)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(128))
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Review {}>'.format(self.body)

class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    def __repr__(self):
        return '<View {}>'.format(self.user_id)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    def __repr__(self):
        return '<Favorite {}>'.format(self.user_id)
