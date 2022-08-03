import json
import bcrypt
from aiohttp_homework.settings import web
from aiohttp_homework.models import User, Token
from aiohttp_homework.handlers import json_response


async def login(request: web.Request):
    json_data = await request.json()
    users = await User.query.where(User.user_name == json_data['user_name']).gino.all()
    if not users:
        raise web.HTTPForbidden(
                content_type='application/json',
                text=json.dumps({'error': 'user does not exist'})
            )
    user = users[0]
    check_password = bcrypt.checkpw(json_data['password'].encode(), user.password.encode())
    if not check_password:
        raise web.HTTPForbidden(
                content_type='application/json',
                text=json.dumps({'error': 'wrong password'})
            )
    new_token = await Token.create(user_id=user.id)
    return json_response(
        {
            'message': 'login successful',
            'token': new_token.id
        }
    )
