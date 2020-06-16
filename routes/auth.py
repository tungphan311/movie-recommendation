from flask import request, make_response, jsonify
from flask_jwt_extended import create_access_token
from app import app, db
from app.models import User
from app.response import Response
import re
import json

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

            identity = Token(u.id, u.email).to_json()
            token = create_access_token(identity=identity)

            response = Response("201", "Tạo tài khoản thành công", data=token).to_json()
            return  make_response(response, 201)
        else:
            response = Response("400", "Email đã được đăng ký").to_json()
            return make_response(response, 400)
    else:
        response = Response("400", "Thông tin đăng ký không hợp lệ").to_json()
        return make_response(response, 400)


def user_existed(email):
    user = User.query.filter_by(email=email).first()

    if user is None:
        return False
    else:
        return True
