from flask_jwt_extended import get_jwt_identity
import json

def get_authorization():
    user = json.loads(get_jwt_identity())
    id = user.get('id')
    email = user.get('email')

    return id, email
