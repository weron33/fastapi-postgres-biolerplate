from sqlalchemy.orm import Session

from src.models.products import User
from src.utils.access_util import hash_password, verify_password, create_access_tokens, authenticate


def get_user_by_username(username: str, db: Session):
    return db.query(User).filter_by(username=username).first()


def create_user(username: str, password: str, db: Session) -> None:
    hashed_password = hash_password(password)
    user = User(username=username, hashedPassword=hashed_password)
    db.add(user)
    db.commit()


def auth_user(username: str, password: str, db: Session) -> False or dict:
    user = get_user_by_username(username, db)
    if not user:
        return False
    if verify_password(password, user.hashedPassword):
        tokens_dict = create_access_tokens(user.username)
        return tokens_dict
    else:
        return False


async def refresh_tokens(refresh_token: str, db: Session) -> dict:
    user = await authenticate(token=refresh_token, db=db)
    return create_access_tokens(user.username)
