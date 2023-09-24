from dataclasses import dataclass
from datetime import date


@dataclass
class RoomsSearchArgs:
    date_from: date
    date_to: date
