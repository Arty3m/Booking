from fastapi import APIRouter

from app.bookings.schemas import SchemeBooking
from app.bookings.service import BookingService

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("", summary="Получить бронирования")
async def get_bookings() -> list[SchemeBooking]:
    return await BookingService.find_all()
    # return await BookingService.find_by_id(2)
    # return await BookingService.find_one_or_none(room_id=1)
