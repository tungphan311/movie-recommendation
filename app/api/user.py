from app import app
from routes.recommendation import recommend
from flask_jwt_extended import jwt_required
from app.api.helpers import get_authorization


@app.route("/api/user/recommend")
@jwt_required
def get_recommend():
    user_id, _ = get_authorization()

    return recommend(user_id)


