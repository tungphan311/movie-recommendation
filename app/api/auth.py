from app import app
from routes.auth import auth_register, auth_login
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.helpers import get_authorization

# authentication route
@app.route("/api/auth/register", methods=['POST'])
def register():
    return auth_register()


@app.route("/api/auth/login", methods=['POST'])
def login():
    return auth_login()


@app.route("/api/auth/refresh-token", methods=['POST'])
def refresh_token():
    return None


@app.route("/api/auth/check-token")
@jwt_required
def protected():
    id, email = get_authorization()
    return create_response(200, 'Token is valid', {'id': id, 'email': email})
