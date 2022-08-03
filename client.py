import asyncio
import aiohttp

HOST = 'http://127.0.0.1:8080'


async def main():
    async with aiohttp.ClientSession() as session:

        async with session.post(f'{HOST}/user/',
                                json={
                                    'user_name': 'Will Herondale',
                                    'email': 'w.herondale@example.org',
                                    'password': 'skdskjfakjfnal1',
                                }) as response:
            response = await response.json()
            print('>>> create normal user')
            print(response, '\n')

        async with session.post(f'{HOST}/user/',
                                json={
                                    'user_name': 'James Carstairs',
                                    'email': 'j.carstairs@example.org',
                                    'password': 'gkdn',
                                }) as response:
            response = await response.json()
            print('>>> create user with too short password')
            print(response, '\n')

        async with session.post(f'{HOST}/user/',
                                json={
                                    'user_name': 'Tessa Gray',
                                    'email': 't.gray@example.org',
                                    'password': 'dkjsnfkjbkafnk223',
                                    'blablabla': 'blablabla',
                                }) as response:
            response = await response.json()
            print('>>> create user with redundant field')
            print(response, '\n')

        async with session.get(f'{HOST}/user/1/') as response:
            response = await response.json()
            print('>>> get user by id')
            print(response, '\n')

        async with session.get(f'{HOST}/user/10/') as response:
            response = await response.json()
            print('>>> get non-existent user by id')
            print(response, '\n')

        async with session.post(f'{HOST}/login/',
                                json={
                                    'user_name': 'Tessa Gray',
                                    'email': 't.gray@example.org',
                                    'password': 'dkjsnfkjbkafnk223'
                                }) as response:
            response = await response.json()
            print('>>> login user 1')
            print(response, '\n')

        async with session.post(f'{HOST}/login/',
                                json={
                                    'user_name': 'Will Herondale',
                                    'email': 'w.herondale@example.org',
                                    'password': 'skdskjfa1',
                                }) as response:
            response = await response.json()
            print('>>> login user 2 with wrong password')
            print(response, '\n')

        # async with session.post(f'{HOST}/login/',
        #                         json={
        #                             'user_name': 'Will Herondale',
        #                             'email': 'w.herondale@example.org',
        #                             'password': 'skdskjfakjfnal1',
        #                         }) as response:
        #     response = await response.json()
        #     print('>>> login user 2')
        #     print(response, '\n')

        async with session.post(f'{HOST}/advertisement/',
                                json={
                                    'title': 'Куплю диван',
                                    'description': 'Рассмотрю угловые, складные и др. виды диванов',
                                }) as response:
            response = await response.json()
            print('>>> post advertisement without authorization')
            print(response, '\n')

        async with session.post(f'{HOST}/advertisement/',
                                json={
                                    'title': 'Продам стол',
                                    'description': 'Дубовый стол в отличном состоянии',
                                    'blablabla': 'blablabla'
                                },
                                headers={
                                    'user_name': 'Tessa Gray',
                                    'token': 'a3ecf325-ff9d-4017-9911-029df22520e7',
                                }) as response:
            response = await response.json()
            print('>>> post advertisement with authorization')
            print(response, '\n')

        async with session.get(f'{HOST}/advertisement/1/') as response:
            response = await response.json()
            print('>>> get advertisement by id')
            print(response, '\n')

        async with session.get(f'{HOST}/advertisement/10/') as response:
            response = await response.json()
            print('>>> get non-existent advertisement by id')
            print(response, '\n')

        async with session.put(f'{HOST}/advertisement/1/',
                               json={
                                   'title': 'Продам дубовый стол',
                                   'description': 'В отличном состоянии'
                               },
                               headers={
                                   'user_name': 'Will Herondale',
                                   'token': '74e71152-075b-4a26-9909-157722c4b487',
                               }) as response:
            response = await response.json()
            print('>>> change advertisement by id with the wrong user and token')
            print(response, '\n')

        async with session.put(f'{HOST}/advertisement/1/',
                               json={
                                   'title': 'Продам дубовый стол',
                                   'description': 'В отличном состоянии'
                               },
                               headers={
                                   'user_name': 'Tessa Gray',
                                   'token': 'a3ecf325-ff9d-4017-9911-029df22520e7',
                               }) as response:
            response = await response.json()
            print('>>> change advertisement by id with owner token')
            print(response, '\n')

        async with session.delete(f'{HOST}/advertisement/1/',
                                  headers={
                                      'user_name': 'Will Herondale',
                                      'token': '74e71152-075b-4a26-9909-157722c4b487',
                                  }) as response:
            response = await response.json()
            print('>>> delete advertisement by id with the wrong user and token')
            print(response, '\n')

        async with session.delete(f'{HOST}/advertisement/1/',
                                  headers={
                                      'user_name': 'Tessa Gray',
                                      'token': 'a3ecf325-ff9d-4017-9911-029df22520e7',
                                  }) as response:
            response = await response.json()
            print('>>> delete advertisement by id with authorization')
            print(response, '\n')


asyncio.run(main())
