import jwt
import os
from datetime import datetime as dt


class SessionStorage:
    def __init__(self, secret: str):
        self.sessions = {}
        self.jwt_secret = secret

    def create(self, data: dict, expired_at: str):
        access_token = os.urandom(15)
        encode = jwt.encode(
            {
                "access_token": access_token.hex(),
                "session_id": len(self.sessions) + 1,
                "expired_at": expired_at,
            },
            self.jwt_secret,
            algorithm="HS256",
        )
        string_key = encode.decode("utf-8")
        self.sessions[string_key] = data
        return string_key

    def is_expired(self, token: str):
        decode = jwt.decode(token, self.jwt_secret, algorithm="HS256")
        datetime_expired = dt.fromtimestamp(decode["expired_at"])
        date_now = dt.now()
        return datetime_expired > date_now

    def is_exist(self, token: str):
        return self.sessions.get(token, None)

    @property
    def json(self):
        return self.sessions

    def delete(self, token: str):
        del self.sessions[token]
