from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


# version sqlalchemy 1.x
# class Rooms(Base):
#     __tablename__ = "rooms"
#
#     id = Column(Integer, primary_key=True, nullable=False)
#     hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
#     name = Column(String, nullable=False)
#     description = Column(String, nullable=True)
#     price = Column(Integer, nullable=False)
#     services = Column(JSON, nullable=True)
#     quantity = Column(Integer, nullable=False)
#     image_id = Column(Integer)

# version sqlachemy 2.x
class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    #  если нужно явно задать параметр строки или необычный для python тип,
    #  пр. длина - указываем явно внутри mapped_column и будет применён он или JSON формат
    services: Mapped[list[str]] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int]
