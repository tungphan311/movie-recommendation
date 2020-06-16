import json

class Response:
    def __init__(self, code, msg, data=[], total=0):
        self.code = code
        self.msg = msg
        self.data = data
        self.total = total

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2, ensure_ascii=False).encode('utf8')