from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from datetime import date
import uvicorn
from dataclasses import dataclass
from pydantic import BaseModel

from app.users.router import router as router_users
from app.bookings.router import router as router_bookings
# from app.hotels.router import router as router_hotels
# TODO refactor naming
from app.hotels.rooms.router import router as router_rooms
from app.images.router import router as router_images

from app.pages.router import router as router_pages

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_bookings)
app.include_router(router_users)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


# app.include_router(router_rooms)

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

# if __name__ == '__main__':
#     uvicorn.run()
