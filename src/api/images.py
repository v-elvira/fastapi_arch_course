# import shutil
from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.images import ImageService
# from src.tasks.tasks import resize_image

router = APIRouter(prefix='/images', tags=['Hotel images'])

# @router.post('')
# def upload_image_celery_version(file: UploadFile):
#     image_path = f'src/static/images/{file.filename}'  # Uvicorn is started from src parent folder
#     with open(image_path, 'wb+') as new_file:
#         shutil.copyfileobj(file.file, new_file)
#
#     resize_image.delay(image_path)  # resize_image must be decorated with @celery_instance.task


@router.post('')
def upload_image(file: UploadFile, bg_tasks: BackgroundTasks):
    ImageService().upload_image(file, bg_tasks)
