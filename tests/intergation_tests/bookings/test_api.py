from tests.conftest import authenticated_client

async def test_get_my_bookings(authenticated_client):
    result = await authenticated_client.get(
        '/bookings/me',
    )
    # print(f'My bookings: {result.json()}')
    assert result.status_code == 200
    assert isinstance(result.json(), list)
