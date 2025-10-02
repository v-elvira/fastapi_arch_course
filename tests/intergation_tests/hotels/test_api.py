from tests.conftest import client

async def test_get_hotels(client):
    # "AssertionError: You must call init first!" if @cache is not commented in api
    result = await client.get(
        '/hotels',
        params={'date_from': '2025-10-01', 'date_to': '2025-10-02'},
    )
    print(f'ALL hotels: {result.json()}')
    assert result.status_code == 200
