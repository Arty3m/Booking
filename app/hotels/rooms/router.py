from fastapi import Depends

from app.hotels.rooms.schemas import RoomsSearchArgs

from app.hotels.rooms.service import RoomsService
from app.hotels.router import router


@router.get("/{hotel_id}/rooms", summary="Получить список комнат")
async def get_rooms(hotel_id: int, query_params: RoomsSearchArgs = Depends()):
    print(query_params.date_from,query_params.date_to)
    available_rooms = await RoomsService.get_rooms_info(hotel_id=hotel_id, date_from=query_params.date_from,
                                                        date_to=query_params.date_to)
    return available_rooms
