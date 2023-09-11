from enum import Enum

from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
    scope: str = None
