from app import app
from flask import request
from routes.search import search_movie

@app.route("/api/search")
def search():
    data = request.args
    page = data.get("page", 1, type=int)
    key = data.get("key", "", type=str)

    return search_movie(key, page)
