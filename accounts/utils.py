import jwt
from datetime import datetime, timedelta, UTC
from django.conf import settings


def generate_token(user, minutes, token_type):
    payload = {
        'user_id': user.id,
        'type': token_type,
        'iat': datetime.now(UTC),
        'exp': datetime.now(UTC) + timedelta(minutes=minutes)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def verify_token(token, token_type):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        if payload['type'] != token_type:
            raise jwt.InvalidTokenError("Invalid token type")
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token")
