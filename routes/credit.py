from app.models import CreditCasts, CreditCrews, Cast, Crew, Video, Review, Rating, User, Keyword, MovieKeywords
from app import app

def get_credits(id):
    creditCasts = CreditCasts.query.filter_by(movie_id=id).limit(5).all()
    creditCrews = CreditCrews.query.filter_by(movie_id=id).all()

    crew = Crew.query\
        .join(CreditCrews, CreditCrews.crew_id == Crew.id)\
        .filter(CreditCrews.movie_id == id)\
        .filter(CreditCrews.department == "Directing")\
        .first()

    writings = Crew.query\
        .join(CreditCrews, CreditCrews.crew_id == Crew.id)\
        .filter(CreditCrews.movie_id == id)\
        .filter(CreditCrews.department == "Writing")\
        .all()

    writing_list = [{'id': w.id,'name': w.name} for w in writings]
    writing_list = writing_list[:2]

    director = {
        'id': crew.id,
        'name': crew.name
    }

    casts = []

    for c in creditCasts:
        cast = Cast.query.get(c.cast_id)
        casts.append({
            'id': cast.id, 
            'name': cast.name,
            'character': c.character,
            'img': cast.image
        })

    return casts, director, writing_list


def get_keywords(id):
    keywords = Keyword.query\
        .join(MovieKeywords, MovieKeywords.keyword_id == Keyword.id)\
        .filter(MovieKeywords.movie_id == id)\
        .limit(4).all()

    keyword_list = [{ 'id': k.id, 'name': k.name } for k in keywords]
    return keyword_list


def get_videos(id):
    videos = Video.query.filter_by(movie_id=id).all()

    if videos is None:
        return []
    
    movie_videos = [{ 'id': v.id, 'name': v.name, 'key': app.config['VIDEO_URL'] + v.key } for v in videos]

    return movie_videos


def get_first_review(id):
    review = Review.query.filter_by(movie_id=id).order_by(Review.timestamp.desc()).first()
    count = Review.query.filter_by(movie_id=id).count()

    if review is None:
        return None

    rating = Rating.query\
        .filter(Rating.movie_id == id)\
        .filter(Rating.user_id == review.user_id)\
        .first()

    user = User.query.get(review.user_id)
    
    return { 
        'headline': review.headline,
        'body': review.body,
        'timestamp': review.timestamp,
        'rating': rating.rating,
        'user': user.email,
        'total': count
    }
