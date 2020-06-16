from app import app
from flask_cors import cross_origin
from routes.auth import auth_register


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"



@app.route("/api/register", methods=['POST'])
@cross_origin()
def register():
    return auth_register()
        
@app.route("/api/login", methods=['POST'])
@cross_origin()
def login():
    return "login"