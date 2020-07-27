from app import app
from routes.auth import auth_register, auth_login, refresh
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_refresh_token_required
from app.api.helpers import get_authorization
from app.response import create_response

# authentication route
@app.route("/api/auth/register", methods=['POST'])
def register():
    return auth_register()


@app.route("/api/auth/login", methods=['POST'])
def login():
    return auth_login()


@app.route("/api/auth/refresh-token", methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
    id, email = get_authorization()
    return refresh(id, email)


@app.route("/api/auth/check-token")
@jwt_required
def protected():
    id, email = get_authorization()
    return create_response(200, 'Token is valid', {'id': id, 'email': email})
