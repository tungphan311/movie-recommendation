import json
import datetime
from flask import make_response

class Response:
    def __init__(self, code, msg, data, total):
        self.code = code
        self.msg = msg
        self.data = data
        self.total = total

    def default_json(self, value):
        if isinstance(value, datetime.timedelta):
            return dict(days=value.days)
        else:
            return value.__dict__

    def to_json(self):
        return json.dumps(self, default=self.default_json, indent=2, ensure_ascii=False).encode('utf8')


def create_response(code, msg, data=[], total=0):
    response = Response(code, msg, data, total).to_json()
    return make_response(response, code)
