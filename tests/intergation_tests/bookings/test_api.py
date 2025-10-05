import pytest
from tests.conftest import authenticated_client

@pytest.mark.parametrize('room_id, date_from, date_to, status_code', [
     (1, '2025-10-01', '2025-10-08', 201),
     (1, '2025-10-03', '2025-10-10', 201),
     (1, '2025-10-01', '2025-10-09', 201),
     (1, '2025-10-01', '2025-10-10', 201),
     pytest.param(1, '2025-10-01', '2025-10-10', 201, id='last free room'),
     pytest.param(1, '2025-10-01', '2025-10-10', 409, id='no free rooms'),
     (1, '2025-10-09', '2025-10-12', 201),
 ])
async def test_add_booking(room_id, date_from, date_to, status_code, db, authenticated_client):
    result = await authenticated_client.post(
        '/bookings',
        json={
            'room_id': room_id,
            'date_from': date_from,
            'date_to': date_to,
        }
    )
    assert result.status_code == status_code
    result_json = result.json()
    assert isinstance(result_json, dict)
    if status_code == 201:
        assert result_json.get('status') == 'OK'
        assert 'data' in result_json
        assert result_json['data'].get('room_id') == room_id


async def test_get_my_bookings(authenticated_client):
    result = await authenticated_client.get(
        '/bookings/me',
    )
    # print(f'My bookings: {result.json()}')
    assert result.status_code == 200
    assert isinstance(result.json(), list)

@pytest.fixture
async def delete_all_bookings(fill_database, db):
    await db.bookings.delete()
    await db.commit()


@pytest.mark.parametrize('booking_count', [1, 2, 3])
async def test_add_and_get_bookings(booking_count, delete_all_bookings, authenticated_client):
    booking_params = {'room_id': 1, 'date_from': '2025-10-01', 'date_to': '2025-10-10'}
    for _ in range(booking_count):
        result = await authenticated_client.post(
            '/bookings',
            json=booking_params,
        )
        assert result.status_code == 201

    result = await authenticated_client.get(
        '/bookings/me',
    )
    assert result.status_code == 200
    result_json = result.json()
    assert isinstance(result_json, list)
    assert len(result_json) == booking_count
