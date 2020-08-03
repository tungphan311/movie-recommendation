from app import app
from flask import request
from routes.search import search_movie

@app.route("/api/movies")
def search():
    data = request.args
    page = data.get("page", 1, type=int)
    key = data.get("query", "", type=str)
    searchType = data.get("type", "All", type=str)
    short = data.get("short", 1, type=int)

    return search_movie(key, page, searchType, short)
