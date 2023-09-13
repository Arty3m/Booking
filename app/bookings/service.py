from sqlalchemy import select

from app.bookings.models import Bookings
from app.db import async_session
from app.service.mixins import ServiceMixin


# ИСПЛЬЗУЕТСЯ ПАТТЕРН DAO

class BookingService(ServiceMixin):
    model = Bookings
