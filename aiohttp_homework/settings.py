from aiohttp import web
from gino import Gino

db = Gino()


async def orm_context(app: web.Application):
    print('Приложение стартовало')
    await db.set_bind('postgresql://aiohttp_db_user:123@db:5432/aiohttp_homework')
    await db.gino.create_all()
    yield
    await db.pop_bind().close()
    print('Приложение завершило работу')
