from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.configs.config import settings
from src.models.products import User
from src.schemas.parameters import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/recommendation-api/login",
    scheme_name="JWT"
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_tokens(username: str):
    to_encode = {'sub': username}
    expire = datetime.utcnow() + timedelta(minutes=settings.API_ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expire = datetime.utcnow() + 2 * timedelta(minutes=settings.API_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    payload = dict(to_encode, **{"scope": 'access_token'})
    refresh_payload = dict(to_encode, **{"scope": 'refresh_token', 'exp': refresh_expire})
    token = jwt.encode(payload, settings.API_SECRET_KEY, algorithm=settings.API_HASH_ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, settings.API_SECRET_KEY, algorithm=settings.API_HASH_ALGORITHM)
    return {'token': token, 'refresh_token': refresh_token}


async def authenticate(token: str = Depends(reusable_oauth), db: Session = Depends(settings.get_db)) -> User or None:
    try:
        payload = jwt.decode(
            token, settings.API_SECRET_KEY, algorithms=[settings.API_HASH_ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # średnie rozwiązanie
    user: User or None = db.query(User).filter_by(username=token_data.sub).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
