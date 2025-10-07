import asyncio
import time
import os
from PIL import Image

from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


@celery_instance.task
def test_task():
    time.sleep(5)
    print('My test task done!')


# @celery_instance.task
def resize_image(image_path: str):
    sizes = [1000, 500, 200]
    output_folder = 'src/static/images'  # Ok if celery and uvicorn are started from src parent folder

    img = Image.open(image_path)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        img_resized = img.resize([size, int(img.height * size / img.width)], Image.Resampling.LANCZOS)
        new_file_name = f'{name}_{size}px{ext}'
        output_path = os.path.join(output_folder, new_file_name)
        img_resized.save(output_path)

    print(f'Image saved in sizes: {sizes} to folder {output_folder}')


async def get_bookings_with_today_checkin_helper():
    print("Today's booking helper..")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_booking_with_today_checkin()
        print(f'{bookings=}')


@celery_instance.task(name='booking_today_checkin')
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
