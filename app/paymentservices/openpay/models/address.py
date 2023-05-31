from dataclasses import dataclass
from typing import Optional


@dataclass
class Address():

    line1: str
    line2: Optional[str]
    line3: Optional[str]
    postal_code: str
    state: str
    city: str
    country_code: str
