from pydantic.dataclasses import dataclass
from http import HTTPStatus
from fastapi.responses import JSONResponse


@dataclass
class Response:
    message: str
    items: list


class SuccessResponse(JSONResponse):
    message = HTTPStatus.OK.phrase
    status_code = HTTPStatus.OK
    items: list

    def __init__(self, content=None, **kwargs):
        if content is None:
            content = []
        responseSchema = {
            'message': HTTPStatus.OK.phrase,
        }
        self.model = Response(message=self.message, items=content)
        self.example_body = self.model.__dict__
        responseSchema = dict(responseSchema, **kwargs)
        content = dict({'items': content}, **responseSchema) if content else responseSchema
        super(SuccessResponse, self).__init__(content=content, status_code=self.status_code)


class CreatedResponse(JSONResponse):
    message = HTTPStatus.OK.phrase
    status_code = HTTPStatus.OK
    items: list

    def __init__(self, content=None, **kwargs):
        if content is None:
            content = []
        responseSchema = {
            'message': HTTPStatus.CREATED.phrase,
        }
        self.model = Response(message=self.message, items=content)
        self.example_body = self.model.__dict__
        responseSchema = dict(responseSchema, **kwargs)
        content = dict({"items": content}, **responseSchema)
        super(CreatedResponse, self).__init__(content=content, status_code=self.status_code)


class PingResponse(JSONResponse):
    message: str = 'pong'
    status_code = HTTPStatus.OK

    def __init__(self, content=None):
        self.model = Response(message=self.message, items=[])
        self.example_body = self.model.__dict__
        if content is None:
            content = self.model.__dict__
        super(PingResponse, self).__init__(content=content, status_code=self.status_code)


class NotAllowedResponse(JSONResponse):
    message = HTTPStatus.OK.phrase
    status_code = HTTPStatus.METHOD_NOT_ALLOWED
    items: list

    def __init__(self, content, **kwargs):
        if content is None:
            content = []
        responseSchema = {
            'message': kwargs['message'] if 'message' in kwargs else HTTPStatus.METHOD_NOT_ALLOWED.phrase,
        }
        self.model = Response(message=self.message, items=content)
        self.example_body = self.model.__dict__
        responseSchema = dict(responseSchema, **kwargs)
        content = dict({"items": content}, **responseSchema)
        super(NotAllowedResponse, self).__init__(content=content, status_code=self.status_code)


class UnauthorizedResponse(JSONResponse):
    message = HTTPStatus.UNAUTHORIZED.phrase
    status_code = HTTPStatus.UNAUTHORIZED
    items: list = []

    def __init__(self, content=None, **kwargs):
        if content is None:
            content = []
        responseSchema = {
            'message': kwargs['message'] if 'message' in kwargs else HTTPStatus.UNAUTHORIZED.phrase,
        }
        self.model = Response(message=self.message, items=content)
        self.example_body = self.model.__dict__
        responseSchema = dict(responseSchema, **kwargs)
        content = dict({"items": content}, **responseSchema)
        super(UnauthorizedResponse, self).__init__(content=content, status_code=self.status_code)


class ForbiddenResponse(JSONResponse):
    message = HTTPStatus.FORBIDDEN.phrase
    status_code = HTTPStatus.FORBIDDEN
    items: list = []

    def __init__(self, content=None, **kwargs):
        if content is None:
            content = []
        responseSchema = {
            'message': kwargs['message'] if 'message' in kwargs else HTTPStatus.FORBIDDEN.phrase,
        }
        self.model = Response(message=self.message, items=content)
        self.example_body = self.model.__dict__
        responseSchema = dict(responseSchema, **kwargs)
        content = dict({"items": content}, **responseSchema)
        super(ForbiddenResponse, self).__init__(content=content, status_code=self.status_code)


class NotFoundResponse(JSONResponse):
    message = HTTPStatus.NOT_FOUND.phrase
    status_code = HTTPStatus.NOT_FOUND
    items: list = []

    def __init__(self, content=None, **kwargs):
        if content is None:
            content = []
        responseSchema = {
            'message': kwargs['message'] if 'message' in kwargs else HTTPStatus.NOT_FOUND.phrase,
        }
        self.model = Response(message=self.message, items=content)
        self.example_body = self.model.__dict__
        responseSchema = dict(responseSchema, **kwargs)
        content = dict({"items": content}, **responseSchema)
        super(NotFoundResponse, self).__init__(content=content, status_code=self.status_code)
