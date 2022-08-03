import json
from aiohttp_homework.settings import web


async def get_object_or_404(model, *criterion):
    object_model = model
    object = await object_model.get(*criterion)
    if object is None:
        raise web.HTTPNotFound(
            content_type='application/json',
            text=json.dumps({'error': 'object not found'})
        )
    return object


def json_response(response):
    return web.json_response(
        content_type='application/json',
        text=json.dumps(response)
    )
