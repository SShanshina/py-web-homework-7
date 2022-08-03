import json
import pydantic
from app.settings import web


def validation(unvalidated_data: dict, validation_model):
    try:
        return validation_model(**unvalidated_data).dict()
    except pydantic.error_wrappers.ValidationError as error:
        raise web.HTTPBadRequest(
            content_type='application/json',
            text=json.dumps({'error': error.errors()})
        )


class CreateUser(pydantic.BaseModel):
    user_name: str
    email: str
    password: str

    @pydantic.validator('password')
    def check_password(cls, value: str):
        if len(value) < 8:
            raise ValueError('password is too short')
        return value


class CreateAdvertisement(pydantic.BaseModel):
    title: str
    description: str
