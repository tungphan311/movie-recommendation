from app import app
from routes.recommendation import recommend


@app.route("/api/user/<int:id>/recommend")
def get_recommend(id=0):
    return recommend(id)
