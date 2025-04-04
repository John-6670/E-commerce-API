import jwt
from datetime import datetime, timedelta, UTC
from django.conf import settings


def generate_email_verification_token(user):
    payload = {
        'user_id': user.id,
        'iat': datetime.now(UTC),
        'exp': datetime.now(UTC) + timedelta(hours=24)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def verify_email_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError or jwt.InvalidTokenError:
        return None
