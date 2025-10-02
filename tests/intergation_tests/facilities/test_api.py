from tests.conftest import client

async def test_create_facility(client):
    result = await client.post(
        '/facilities',
        json={'title': 'Wi-Fi'},
    )
    print(f'Response create facility: {result.json()}')
    assert result.status_code == 201
    assert result.json()['data']['title'] == 'Wi-Fi'


async def test_get_facilities(client):
    result = await client.get('/facilities')
    print(f'Rescponse get facilities: {result.json()}')   #  [{'title': 'Wi-Fi', 'id': 1}]
    assert result.status_code == 200
