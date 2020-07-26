import json
import datetime
from flask import make_response

class Response:
    def __init__(self, code, msg, data):
        self.code = code
        self.msg = msg
        self.data = data

    def default_json(self, value):
        if isinstance(value, datetime.timedelta):
            return dict(days=value.days)
        else:
            return value.__dict__

    def to_json(self):
        return json.dumps(self, default=self.default_json, indent=2, ensure_ascii=False).encode('utf8')


def create_response(code, msg, data=[]):
    response = Response(code, msg, data).to_json()
    return make_response(response, code)
