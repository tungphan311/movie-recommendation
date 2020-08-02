import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    API_KEY = os.environ.get('API_KEY')

    PAGE_SIZE = 24

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    CORS_HEADERS = 'Content-Type'

    IMG_URL = "http://images.tmdb.org/t/p/original"
    IMG_DEFAULT = "https://www.reelviews.net/resources/img/default_poster.jpg"
    BACKDROP_DEFAULT = "https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png"
    VIDEO_URL = "https://www.youtube.com/embed/"
