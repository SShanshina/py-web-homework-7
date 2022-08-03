from aiohttp_homework.settings import web, orm_context
from aiohttp_homework.views import UserView, AdvertisementView
from aiohttp_homework.login import login


def get_app():
    app = web.Application()
    app.cleanup_ctx.append(orm_context)
    app.router.add_routes(
        [
            web.get('/user/{user_id:\d+}/', UserView),
            web.post('/user/', UserView),
            web.get('/advertisement/{advertisement_id:\d+}/', AdvertisementView),
            web.post('/advertisement/', AdvertisementView),
            web.delete('/advertisement/{advertisement_id:\d+}/', AdvertisementView),
            web.put('/advertisement/{advertisement_id:\d+}/', AdvertisementView),
            web.post('/login/', login)
        ]
    )
    return app


my_app = get_app()
