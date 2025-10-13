async def test_get_hotels(client):
    # "AssertionError: You must call init first!" if @cache is not commented in api
    result = await client.get(
        '/hotels',
        params={'date_from': '2025-10-01', 'date_to': '2025-10-02'},
    )
    print(f'ALL hotels: {result.json()}')
    assert result.status_code == 200


async def test_get_hotel(client):
    result = await client.get(
        '/hotels/1',
    )
    print(f'GOT hotel: {result.json()}')
    assert result.status_code == 200
    result_json = result.json()
    assert isinstance(result_json, dict)
    assert 'title' in result_json
    assert 'location' in result_json
    assert 'id' in result_json
