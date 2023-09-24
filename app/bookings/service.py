from datetime import date

from sqlalchemy import select, delete, insert, and_, or_, func

from app.bookings.models import Bookings
from app.db import async_session, engine
from app.hotels.rooms.models import Rooms
from app.service.mixins import ServiceMixin


# ИСПЛЬЗУЕТСЯ ПАТТЕРН DAO

class BookingService(ServiceMixin):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
            (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )
        """
        async with async_session() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == 1,
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
                )
            ).cte("booked_rooms")

            """
            SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            WHERE rooms.id = 1
            GROUP BY rooms.quantity, booked_rooms.room_id
            """
            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )
            # print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

            rooms_left_result = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left_result.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price_result = await session.execute(get_price)
                price: int = price_result.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Bookings)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalars()
            else:
                return None

    # mb rename to get_booking_with_info_about_rooms
    @classmethod
    async def find_all(cls, user_id: int):
        async with async_session() as session:
            get_bookings = select(
                Bookings.__table__.columns, Rooms.image_id, Rooms.name, Rooms.description, Rooms.services
            ).select_from(Bookings, Rooms).join(
                Rooms, Rooms.id == Bookings.room_id, isouter=True).where(Bookings.user_id == user_id)
            bookings = await session.execute(get_bookings)
        return bookings.mappings().all()
