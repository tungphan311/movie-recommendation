from flask import request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from app import app, db
from app.models import User
from app.response import Response, create_response
import re
import json
import datetime


class Token:
    def __init__(self, id, email):
        self.id = id
        self.email = email

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)


def auth_register():
    data = request.get_json()
    email = data.get("email", "")
    password = data.get("password", "")
    valid_email = re.search(
        "^(([^<>()[\]\\.,;:\s@“]+(\.[^<>()[\]\\.,;:\s@“]+)*)|(“.+“))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$",
        email
    )
    valid_password = len(password) >= 6 and len(password) <= 15

    if valid_password and valid_email:
        if not user_existed(email):
            u = User(email=email)
            u.hash_password(password)
            db.session.add(u)
            db.session.flush()
            db.session.commit()

            data = create_token(u)

            return create_response(201, "Create account successfully", data=data)
        else:
            return create_response(400, "Email is already taken")
    else:
        return create_response(400, "Request info is not valid")


def create_token(user):
    identity = Token(user.id, user.email).to_json()
    expires = datetime.timedelta(hours=1)
    res = {
        'token': create_access_token(identity=identity, expires_delta=expires),
        'refresh_token': create_refresh_token(identity=identity, expires_delta=datetime.timedelta(days=1))
    }
    return res


def user_existed(email):
    user = User.query.filter_by(email=email).first()

    if user is None:
        return False
    else:
        return True


def auth_login():
    data = request.get_json()
    email = data.get("email", "")
    password = data.get("password", "")

    user = User.query.filter_by(email=email).first()

    if user is None:
        return create_response(401, "Email or password is not correct")
    else:
        if user.check_password(password):
            data = create_token(user)

            return create_response(200, "Login successfully", data=data)
        else:
            return create_response(401, "Email or password is not correct")


def refresh(id, email):
    identity = Token(id, email).to_json()
    expires = datetime.timedelta(hours=1)
    res = {
        'token': create_access_token(identity=identity, expires_delta=expires)
    }

    return create_response(200, "Refreshed token", data=res)
