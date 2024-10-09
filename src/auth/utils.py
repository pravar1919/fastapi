from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.config import Config
import jwt
import uuid
import logging

password_context = CryptContext(
    schemes=['bcrypt']
)


def generate_password_hash(password: str) -> str:
    password_hash = password_context.hash(password)

    return password_hash


def verify_password(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)


def create_access_token(data: dict, expiry: timedelta = timedelta(days=1), refresh: bool = False):
    '''
    Here expiry of the token is one day (timedelta(1))
    '''
    payload = {}
    payload['user'] = data
    payload['exp'] = datetime.now() + expiry
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM
    )
    return token


def decode_access_token(token: str):
    try:
        return jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
