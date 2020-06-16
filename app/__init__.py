from flask import Flask, Response, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# set config for database
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# setup CORS policy
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# setup fkask-jwt-extended for using jwt
app.config['JWT_SECRET_KEY'] = 'movie-recommendation-server-secret-key'
jwt = JWTManager(app)


from app import routes, models, jwt
