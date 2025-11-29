import shutil

from fastapi import UploadFile  # from fastapi: not good for Service idea
from starlette.background import BackgroundTask

from src.services.base import BaseService
from src.tasks.tasks import resize_image


class ImageService(BaseService):
    def upload_image(self, file: UploadFile, bg_tasks: BackgroundTask):
        image_path = f'src/static/images/{file.filename}'  # Uvicorn is started from src parent folder
        with open(image_path, 'wb+') as new_file:
            shutil.copyfileobj(file.file, new_file)

        # resize_image.delay(image_path)
        bg_tasks.add_task(resize_image(), image_path)
