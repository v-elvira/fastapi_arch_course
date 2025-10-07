from src.schemas.hotels import HotelAdd


# @pytest.mark.asyncio   # or add "asyncio_mode = auto" in pytest.ini for all functions
async def test_add_hotel(db):
    data = HotelAdd(title='Hotel 1', location='Main Street, 2')
    new_hotel = await db.hotels.add(data)
    print(f'{new_hotel=}')
    await db.commit()
