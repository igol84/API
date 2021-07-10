from datetime import datetime, timedelta
from jose import jwt, JWTError
from .schemas import user as schemas
from .settings import settings


def create_access_token(data: dict):
    to_encode = data.copy()
    now = datetime.utcnow()
    to_encode.update({"nbf": now})
    expire = now + timedelta(seconds=settings.jwt_expiration_sec)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    return token_data
