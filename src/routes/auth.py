from fastapi import Depends, APIRouter, Body
from sqlalchemy.orm import Session

from src.configs.config import settings, logger
from src.controllers import auth_controller
from src.schemas.bodies import AuthBody, RefreshBody
from src.schemas.responses import SuccessResponse, NotFoundResponse, CreatedResponse, ForbiddenResponse, \
    UnauthorizedResponse
from src.utils import access_util

successResponse = SuccessResponse(content=[])
createdResponse = CreatedResponse(content=[])
notFoundResponse = NotFoundResponse(content=[])
forbiddenResponse = ForbiddenResponse(content=[])
unauthorizedResponse = UnauthorizedResponse(content=[])

router = APIRouter(tags=['auth'],
                   responses={
                       '200': {
                           'class': successResponse,
                           'model': successResponse.model,
                           'description': successResponse.message
                       },
                       '201': {
                           'class': createdResponse,
                           'model': createdResponse.model,
                           'description': createdResponse.message
                       },
                       '401': {
                           'class': unauthorizedResponse,
                           'model': unauthorizedResponse.model,
                           'description': unauthorizedResponse.message
                       },
                       '403': {
                           'class': forbiddenResponse,
                           'model': forbiddenResponse.model,
                           'description': forbiddenResponse.message
                       },
                       '404': {
                           'class': notFoundResponse,
                           'model': notFoundResponse.model,
                           'description': notFoundResponse.message
                       }
                   })
auth_controller.initialize_admin()
logger.info(f'Admin initialized!')


@router.post('/recommendation-api/user', description='Method to allow create user', dependencies=[Depends(access_util.authenticate)])
async def post_user(body: AuthBody = Body(description='User metadata'),
                    db: Session = Depends(settings.get_db)
                    ) -> SuccessResponse or ForbiddenResponse:
    response = auth_controller.create_user(username=body.username, password=body.password, db=db)
    return response


@router.post("/recommendation-api/login", description='Method to authenticate user')
async def login(body: AuthBody = Body(description='User metadata'),
                db: Session = Depends(settings.get_db)
                ) -> SuccessResponse or ForbiddenResponse:
    response = auth_controller.auth_user(body.username, body.password, db)
    return response


@router.post("/recommendation-api/token/refresh", description='Method to refresh authorization token', dependencies=[Depends(access_util.authenticate)])
async def refresh(body: RefreshBody = Body(description='Token metadata'),
                  db: Session = Depends(settings.get_db)
                  ) -> SuccessResponse or UnauthorizedResponse:
    response = await auth_controller.refresh_user(body.refresh_token, db)
    return response
