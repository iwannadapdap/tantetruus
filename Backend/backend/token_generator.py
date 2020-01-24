from itsdangerous import URLSafeTimedSerializer
from app_config import SECURITY_PASSWORD_SALT, SECRET_KEY


def generate_confirm_token(email: str):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=36000):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
            max_age=expiration)
    except:
        return False
    return email
