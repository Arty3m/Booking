from datetime import date

from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.service.mixins import ServiceMixin

from sqlalchemy import select, delete, insert, and_, or_, func

from app.bookings.models import Bookings
from app.db import async_session, engine


class HotelsService(ServiceMixin):
    model = Hotels

    @classmethod
    async def get_hotels_and_rooms_left(cls, location: str, date_from: date, date_to: date):
        async with async_session() as session:
            """
            WITH hotels_with_booked_rooms AS (
                WITH booked_rooms AS (
                    SELECT * FROM bookings
                    WHERE
                    (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                    (date_from <= '2023-05-15' AND date_to > '2023-05-15')
                )
    
                SELECT rooms.hotel_id, rooms.id,
                     COUNT(booked_rooms) as rooms_booked
                FROM booked_rooms
                LEFT JOIN rooms ON rooms.id=booked_rooms.room_id
                GROUP BY rooms.id, rooms.quantity, rooms.hotel_id
            )
            """
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

            hotels_with_booked_rooms = select(
                Rooms.id, Rooms.hotel_id,
                (func.count(booked_rooms.table_valued()).label("rooms_booked"))
            ).select_from(
                booked_rooms
            ).join(
                Rooms, Rooms.id == booked_rooms.c.room_id, isouter=True
            ).group_by(
                Rooms.id, Rooms.quantity, Rooms.hotel_id
            ).cte("hotels_with_booked_rooms")
            """
             SELECT hotels.name, hotels.location, hotels.rooms_quantity - SUM(COALESCE(hotels_with_booked_rooms.rooms_booked,0)) as r_left
            FROM hotels
            LEFT JOIN hotels_with_booked_rooms ON hotels_with_booked_rooms.hotel_id=hotels.id
            WHERE hotels.location LIKE '%Алтай%'
            GROUP BY hotels.name, hotels.location,  hotels.rooms_quantity
            """
            get_available_hotels = select(
                Hotels.id, Hotels.name, Hotels.location, Hotels.services, Hotels.rooms_quantity, Hotels.image_id,
                (Hotels.rooms_quantity - func.sum(func.coalesce(hotels_with_booked_rooms.c.rooms_booked, 0))).label(
                    "rooms_left")
            ).select_from(Hotels).join(
                hotels_with_booked_rooms, hotels_with_booked_rooms.c.hotel_id == Hotels.id, isouter=True
            ).where(Hotels.location.like(f"%{location}%")).group_by(Hotels.id, Hotels.name, Hotels.location,
                                                                    Hotels.rooms_quantity)
            available_hotels = await session.execute(get_available_hotels)
            # print(get_available_hotels.compile(engine, compile_kwargs={"literal_binds": True}))
            return available_hotels.mappings().all()
