import uuid
from datetime import date
from enum import Enum
from typing import Optional

from pydantic import Field, PositiveInt, constr, validator
from pydantic_settings import BaseSettings


class PropertyType(str, Enum):
    House = "House"
    Condo = "Condo"
    Duplex = "Duplex"


class HomeListing(BaseSettings):

    id: str
    address_id: str
    full_address: constr(strip_whitespace=True, min_length=1)
    street_name: constr(strip_whitespace=True, min_length=1)
    city: constr(strip_whitespace=True, min_length=1)
    province: constr(strip_whitespace=True, min_length=2, max_length=2, pattern=r"^(ON)$")
    postal_code: constr(strip_whitespace=True, min_length=7, max_length=7, pattern=r"^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$")
    lat: float = Field(..., ge=42, le=83)
    lon: float = Field(..., ge=-141, le=52.6)
    home_price: float = Field(..., ge=300000)
    bed: Optional[PositiveInt]
    bath: Optional[PositiveInt]
    property_type: Optional[PropertyType]
    description: Optional[str]
    listing_date: date

    @validator("id", "address_id")
    def validate_uuid(cls, value):
        try:
            uuid_obj = uuid.UUID(value)
        except ValueError:
            raise ValueError("Invalid UUID format")

        return value
