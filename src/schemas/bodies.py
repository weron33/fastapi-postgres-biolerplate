from pydantic import BaseModel


class AuthBody(BaseModel):
    username: str
    password: str


class RefreshBody(BaseModel):
    refresh_token: str
