from datetime import date

from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.service.mixins import ServiceMixin
from sqlalchemy import select, delete, insert, and_, or_, func

from app.bookings.models import Bookings
from app.db import async_session, engine


class RoomsService(ServiceMixin):
    model = Rooms

    @classmethod
    async def get_rooms_info(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session() as session:
            """
                 WITH booked_rooms AS (
                    SELECT * FROM bookings
                    WHERE
                    (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                    (date_from <= '2023-05-15' AND date_to > '2023-05-15')
                )"""
            booked_rooms = select(Bookings).where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from
                    )
                )
            ).cte("booked_rooms")
            """
            SELECT rooms.name, rooms.id, rooms.price, rooms.quantity - COUNT(booked_rooms.room_id) as rooms_left
            FROM booked_rooms
            LEFT JOIN rooms ON rooms.id=booked_rooms.room_id 
            LEFT JOIN hotels ON rooms.hotel_id=hotels.id
            WHERE hotels.id = 1
            GROUP BY rooms.name,  rooms.id, rooms.price
            """
            get_rooms = select(
                Rooms.id, Rooms.hotel_id, Rooms.name, Rooms.description, Rooms.services, Rooms.price,
                Rooms.quantity, Rooms.image_id,
                (Rooms.quantity - func.count(booked_rooms.table_valued())).label("rooms_left")
            ).select_from(
                booked_rooms
            ).join(
                Rooms, Rooms.id == booked_rooms.c.room_id, isouter=True
            ).join(
                Hotels, Rooms.hotel_id == Hotels.id, isouter=True
            ).where(
                Hotels.id == hotel_id
            ).group_by(Rooms.id)

            # print(get_rooms.compile(engine, compile_kwargs={"literal_binds": True}))

            available_rooms = await session.execute(get_rooms)
            return available_rooms.mappings().all()
