from datetime import date

from fastapi import APIRouter, Depends

from app.hotels.service import HotelsService
from app.hotels.schemas import HotelsSearchArgs

router = APIRouter(prefix="/hotels",
                   tags=["Отели и комнаты"])


@router.get("/{location}", summary="Получение списка отелей")
# async def get_hotels(location: str, date_from: date, date_to: date):
async def get_hotels(location: str, query_params: HotelsSearchArgs = Depends()):
    print(location, query_params.date_from, query_params.date_to)
    available_hotels = await HotelsService.get_hotels_and_rooms_left(
        location=location, date_from=query_params.date_from, date_to=query_params.date_to
    )
    return available_hotels


@router.get("/id/{hotel_id}", summary="Получение конкретного отеля")
async def get_hotel(hotel_id: int):
    hotel = await HotelsService.find_by_id(model_id=hotel_id)
    if not hotel:
        print('takogo net')
    return hotel
