from tests.conftest import client

async def test_full_auth(client):
    user_data = {'email': 'test@mail.ru', 'password': 'test'}
    register_result = await client.post(
        '/auth/register',
        json=user_data,
    )
    assert register_result.status_code == 201

    login_result = await client.post(
        '/auth/login',
        json=user_data,
    )
    assert login_result.status_code == 200

    me = await client.get(
        '/auth/me',
    )
    assert me.status_code == 200
    me_data = me.json()
    assert me_data['email'] == user_data['email']

    logout_result = await client.post(
        '/auth/logout',
    )
    assert logout_result.status_code == 200

    new_me_result = await client.get(
        '/auth/me'
    )
    assert new_me_result.status_code == 401
