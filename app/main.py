from app.settings import web, app, orm_context
from app.views import UserView, AdvertisementView
from app.login import login

app.add_routes(
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

app.cleanup_ctx.append(orm_context)

if __name__ == '__main__':
    web.run_app(app, port=5000)
