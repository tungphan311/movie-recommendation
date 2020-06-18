from app import app
from flask import request
from flask_cors import cross_origin
from routes.auth import auth_register, auth_login
from routes.recommendation import recommend
from routes.movie import movie_get_by_id


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


# authentication route
@app.route("/api/register", methods=['POST'])
@cross_origin()
def register():
    return auth_register()


@app.route("/api/login", methods=['POST'])
@cross_origin()
def login():
    return auth_login()


@app.route("/api/recommend")
@cross_origin()
def get_recommend():
    data = request.get_json()
    id = data.get("user_id", 0)
    return recommend(id)


@app.route("/api/movies/<id>", methods=['POST'])
@cross_origin()
def get_movie_by_id(id=0):
    data = request.get_json()
    user_id = data.get("user_id", 0)
    return movie_get_by_id(id, user_id)
