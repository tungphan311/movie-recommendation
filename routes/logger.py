from app.models import Log, LogDetail
from app import db

class Logger(object):
    def __init__(self, user_id, action_type_id, movie_id = None, rating = None, headline = None, body = None):
        self.user_id = user_id
        self.action_type_id = action_type_id
        self.movie_id = movie_id
        self.rating = rating
        self.headline = headline
        self.body = body
    
    def create_log(self):
        log = Log(user_id=self.user_id, action_type_id=self.action_type_id)
        db.session.add(log)

        if (self.action_type_id > 3):
            db.session.flush()
            db.session.refresh(log)

            if self.movie_id is None:
                return

            detail1 = LogDetail(log_id=log.id, action_parameter_id=1, value=self.movie_id)
            db.session.add(detail1)

            if self.action_type_id == 5:
                if self.rating is None:
                    return

                detail2 = LogDetail(log_id=log.id, action_parameter_id=2, value=self.rating)
                db.session.add(detail2)

            if self.action_type_id == 7:
                if self.headline is None or self.body is None:
                    return

                detail2 = LogDetail(
                    log_id=log.id, action_parameter_id=3, value=self.headline)
                db.session.add(detail2)
                detail3 = LogDetail(
                    log_id=log.id, action_parameter_id=4, value=self.body)
                db.session.add(detail3)
            
        db.session.commit()
