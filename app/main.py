from fastapi import FastAPI, Query, Depends
from typing import Annotated
from datetime import date
import uvicorn
from dataclasses import dataclass
from pydantic import BaseModel

from app.bookings.router import router as router_bookings

app = FastAPI()

app.include_router(router_bookings)

# class HotelsSearchArgs:
#     def __init__(self, location: str,
#                  date_from: date,
#                  date_to: date,
#                  has_spa: bool = None,
#                  stars: Annotated[int, Query(ge=1, le=5)] = None):
#         self.location = location
#         self.date_from = date_from
#         self.date_to = date_to
#         self.has_spa = has_spa
#         self.stars = stars

# OR USE DATACLASS


@dataclass
class HotelsSearchArgs:
    location: str
    date_from: date
    date_to: date
    has_spa: bool = None
    stars: Annotated[int, Query(ge=1, le=5)] = None


class SchemeHotels(BaseModel):
    address: str
    name: str
    stars: int
    # stars: int = Field(0-5)


@app.get('/hotels')
def get_hotels(search_args: HotelsSearchArgs = Depends()):

    return search_args


class SchemeBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post('/bookings')
def add_booking(booking: SchemeBooking):
    return None

# if __name__ == '__main__':
#     uvicorn.run()
