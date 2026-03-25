from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BookingInput(BaseModel):
    customer_id: int
    vendor_id: Optional[int] = None
    service_id: int
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    date_time: datetime = None
    status: str = "pending"
    price: float


class BookingResponse(BookingInput):
    booking_id: int

    class Config:
        from_attributes = True
