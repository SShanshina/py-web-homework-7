import json
import bcrypt
from app.settings import web
from app.validation import validation, CreateUser, CreateAdvertisement
from app.models import User, Advertisement
from app.handlers import get_object_or_404, json_response
from app.authorization import check_token, check_authorization
from asyncpg.exceptions import UniqueViolationError


class UserView(web.View):

    async def get(self):
        request = self.request
        user = await get_object_or_404(User, int(request.match_info['user_id']))
        return json_response(user.to_dict())

    async def post(self):
        request = self.request
        json_data_validated = validation(await request.json(), CreateUser)
        json_data_validated['password'] = bcrypt.hashpw(
            json_data_validated['password'].encode(), bcrypt.gensalt()
        ).decode()
        try:
            new_user = await User.create(**json_data_validated)
        except UniqueViolationError:
            raise web.HTTPBadRequest(
                content_type='application/json',
                text=json.dumps({'error': 'user already exists'})
            )
        return json_response(new_user.to_dict())


class AdvertisementView(web.View):

    async def get(self):
        request = self.request
        advertisement = await get_object_or_404(Advertisement, int(request.match_info['advertisement_id']))
        return json_response(advertisement.to_dict())

    async def post(self):
        request = self.request
        headers = dict(request.headers)
        json_data_validated = validation(await request.json(), CreateAdvertisement)
        token = await check_token(headers)
        if token:
            advertisement_owner = await User.query.where(
                User.user_name == headers.get('user_name')
            ).gino.first()
            json_data_validated['owner_id'] = advertisement_owner.id
            try:
                new_advertisement = await Advertisement.create(**json_data_validated)
            except UniqueViolationError:
                raise web.HTTPBadRequest(
                    content_type='application/json',
                    text=json.dumps({'error': 'advertisement already exists'})
                )
            return json_response(new_advertisement.to_dict())

    async def delete(self):
        request = self.request
        advertisement_id = int(request.match_info['advertisement_id'])
        advertisement = await get_object_or_404(Advertisement, advertisement_id)
        await check_authorization(dict(request.headers), advertisement)
        await Advertisement.delete.where(Advertisement.id == advertisement_id).gino.status()
        return json_response({'message': 'your advertisement has been successfully deleted'})

    async def put(self):
        request = self.request
        json_data_validated = validation(await request.json(), CreateAdvertisement)
        advertisement = await get_object_or_404(Advertisement, int(request.match_info['advertisement_id']))
        await check_authorization(dict(request.headers), advertisement)
        await advertisement.update(
            title=json_data_validated['title'],
            description=json_data_validated['description']
        ).apply()
        return json_response(advertisement.to_dict())
