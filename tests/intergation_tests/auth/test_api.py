import pytest

from tests.conftest import client


@pytest.mark.parametrize(
    'email, password, status',
    [
        pytest.param('mail@mail.ru', 'pass', 201, id='Happy path'),
        pytest.param('mail@mail.ru', 'pass', 409, id='User exists'),
        pytest.param('mail', 'pass', 422, id='Wrong email'),
    ],
)
async def test_register(email, password, status, client):
    result = await client.post('/auth/register', json={'email': email, 'password': password})
    assert result.status_code == status


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
    assert 'access_token' in login_result.json()
    assert client.cookies.get('access_token')

    me = await client.get(
        '/auth/me',
    )
    assert me.status_code == 200
    me_data = me.json()
    assert me_data['email'] == user_data['email']
    assert 'id' in me_data
    assert 'password' not in me_data
    assert 'hashed_password' not in me_data

    logout_result = await client.post(
        '/auth/logout',
    )
    assert logout_result.status_code == 200
    assert 'access_token' not in client.cookies

    new_me_result = await client.get('/auth/me')
    assert new_me_result.status_code == 401
