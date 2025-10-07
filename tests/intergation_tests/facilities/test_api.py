async def test_create_facility(client):
    test_title = 'Wi-Fi'
    result = await client.post(
        '/facilities',
        json={'title': test_title},
    )
    # print(f'Response create facility: {result.json()}')
    assert result.status_code == 201
    result_json = result.json()
    assert isinstance(result_json, dict)
    assert 'data' in result_json
    assert result_json['data']['title'] == test_title


async def test_get_facilities(client):
    result = await client.get('/facilities')
    # print(f'Rescponse get facilities: {result.json()}')   #  [{'title': 'Wi-Fi', 'id': 1}]
    assert result.status_code == 200
    assert isinstance(result.json(), list)
