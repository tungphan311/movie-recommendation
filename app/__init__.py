from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from elasticsearch import Elasticsearch


app = Flask(__name__)

# set config for database
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# setup CORS policy
CORS(app)

# setup fkask-jwt-extended for using jwt
jwt = JWTManager(app)

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
    if app.config['ELASTICSEARCH_URL'] else None


from app import routes, models, response, recommend
