from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from src.configs.config import settings, logger
from src.schemas.responses import CreatedResponse, SuccessResponse, ForbiddenResponse, UnauthorizedResponse
from src.services import auth_service


def initialize_admin():
    db = next(settings.get_db())
    admin = auth_service.get_user_by_username(settings.ADMIN_USERNAME, db)
    if admin:
        logger.info(f'Admin already exists! [admin_username={settings.ADMIN_USERNAME}]')
    else:
        auth_service.create_user(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD, db)
        logger.info(f'Admin created! [admin_username={settings.ADMIN_USERNAME}]')


def create_user(username: str, password: str, db: Session) -> CreatedResponse:
    auth_service.create_user(username, password, db)
    return CreatedResponse(message='User successfully created!')


def auth_user(username: str, password: str, db: Session) -> SuccessResponse or ForbiddenResponse:
    auth_result = auth_service.auth_user(username, password, db)
    if auth_result:
        return SuccessResponse(message="Login success", **auth_result)
    else:
        return ForbiddenResponse(message="Bad credentials.")


async def refresh_user(refresh_token: str, db: Session) -> SuccessResponse or ForbiddenResponse:
    try:
        auth_result = await auth_service.refresh_tokens(refresh_token, db)
        return SuccessResponse(message="Login success", **auth_result)
    except HTTPException:
        return UnauthorizedResponse(message="Bad credentials.")
