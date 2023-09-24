from datetime import date

from fastapi import APIRouter, Request, Depends, status

from app.bookings.schemas import SchemeBooking
from app.bookings.service import BookingService
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.model import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("", summary="Получить бронирования")
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingService.find_all(user_id=user.id)


@router.post("", summary="Добавить бронирование")
async def add_booking(room_id: int, date_from: date, date_to: date,
                      user: Users = Depends(get_current_user)):
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    # return await BookingService.find_all(user_id=user.id)


@router.delete("/{booking_id}", summary="Удалить бронирование", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingService.delete(id=booking_id)
