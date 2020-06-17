from app import app
from flask_cors import cross_origin
from routes.auth import auth_register, auth_login


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


@app.route("/api/get-recommend")
@cross_origin()
def get_recommend():
    return "rec"