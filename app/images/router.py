from fastapi import APIRouter, UploadFile, status
import shutil


router = APIRouter(prefix="/images",
                   tags=["Загрузка картинок"])


@router.post("/hotels", status_code=status.HTTP_201_CREATED)
async def add_hotel_image(name: int, file: UploadFile):
    with open(f"app/static/images/{name}.webp", "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

