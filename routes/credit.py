from app.models import Credit, CreditCasts, CreditCrews, Cast, Crew

def get_credits(id):
    credit = Credit.query.get(id)
    creditCasts = CreditCasts.query.filter_by(credit_id=credit.id).limit(5).all()
    creditCrews = CreditCrews.query.filter_by(credit_id=credit.id).all()

    crew = Crew.query\
        .join(CreditCrews, CreditCrews.crew_id == Crew.id)\
        .filter(CreditCrews.credit_id == credit.id)\
        .filter(Crew.department == "Directing")\
        .first()

    writings = Crew.query\
        .join(CreditCrews, CreditCrews.crew_id == Crew.id)\
        .filter(CreditCrews.credit_id == credit.id)\
        .filter(Crew.department == "Writing")\
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
            'character': cast.character,
            'img': cast.image
        })

    return casts, director, writing_list
