from flask import Flask, jsonify
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
CORS(app, resources={r"/api/*": { "origins": "http://localhost:3000" }})

# setup fkask-jwt-extended for using jwt
jwt = JWTManager(app)

@jwt.expired_token_loader
def my_custom_expired_token(expired_token):
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'Token has expired'
    }), 401

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
    if app.config['ELASTICSEARCH_URL'] else None


from app import models, response, recommend
from app.api import auth, movies, search, user
