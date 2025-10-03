from tests.conftest import authenticated_client

async def test_add_booking(db, authenticated_client):
    room_id = (await db.rooms.get_all())[0].id
    result = await authenticated_client.post(
        '/bookings',
        json={
            'room_id': room_id,
            'date_from': '2025-10-01',
            'date_to': '2025-10-02',
        }
    )
    assert result.status_code == 201
    result_json = result.json()
    assert isinstance(result_json, dict)
    assert result_json.get('status') == 'OK'
    assert 'data' in result_json
    assert result_json['data'].get('room_id') == room_id


async def test_add_booking_extra_temp(db, authenticated_client):
    room_id = (await db.rooms.get_all())[0].id
    for i in range(4):
        result = await authenticated_client.post(
            '/bookings',
            json={
                'room_id': room_id,
                'date_from': '2025-10-01',
                'date_to': '2025-10-02',
            }
        )
        assert result.status_code == 201
        result_json = result.json()
        assert isinstance(result_json, dict)
        assert result_json.get('status') == 'OK'
        assert 'data' in result_json
        assert result_json['data'].get('room_id') == room_id

    result = await authenticated_client.post(
        '/bookings',
        json={
            'room_id': room_id,
            'date_from': '2025-10-01',
            'date_to': '2025-10-02',
        }
    )
    assert result.status_code == 409
    assert isinstance(result.json(), dict)


async def test_get_my_bookings(authenticated_client):
    result = await authenticated_client.get(
        '/bookings/me',
    )
    # print(f'My bookings: {result.json()}')
    assert result.status_code == 200
    assert isinstance(result.json(), list)
