from dataclasses import dataclass
from datetime import date
from typing import Annotated

from fastapi import Query


# @dataclass
# class HotelsSearchArgs:
#     location: str
#     date_from: date
#     date_to: date
#     has_spa: bool = None
#     stars: Annotated[int, Query(ge=1, le=5)] = None

@dataclass
class HotelsSearchArgs:
    date_from: date
    date_to: date
