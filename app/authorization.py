import json
from app.settings import web
from app.models import User, Advertisement, Token


async def check_token(headers: dict):
    token = await Token.query.where(
        User.user_name == headers.get('user_name')
    ).where(
        Token.id == headers.get('token')
    ).gino.first()
    if token is None:
        raise web.HTTPForbidden(
            content_type='application/json',
            text=json.dumps({'error': 'invalid token or user name'})
        )
    return token


async def check_authorization(headers: dict, advertisement: Advertisement):
    token = await check_token(headers)
    if token.user_id != advertisement.owner_id:
        raise web.HTTPForbidden(
            content_type='application/json',
            text=json.dumps({'error': 'auth error'})
        )
