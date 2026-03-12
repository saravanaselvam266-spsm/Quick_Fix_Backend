from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from dependencies import connect_db, get_current_user
from models.user_model import User
from models.booking_model import Booking
from schema.booking_schema import BookingInput, BookingResponse
from math import radians, cos, sin, asin, sqrt
from typing import List

router = APIRouter(prefix="/bookings", tags=["Bookings"])


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    if lon1 is None or lat1 is None or lon2 is None or lat2 is None:
        return float("inf")

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(
        radians, [float(lon1), float(lat1), float(lon2), float(lat2)]
    )

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r


@router.get("/", response_model=List[BookingResponse])
def get_bookings(
    db: Session = Depends(connect_db), current_user: User = Depends(get_current_user)
):
    return db.query(Booking).all()


@router.get("/nearby", response_model=List[BookingResponse])
def get_nearby_bookings(
    lat: float,
    lon: float,
    radius: float = 10.0,
    db: Session = Depends(connect_db),
    current_user: User = Depends(get_current_user),
):
    # Fetch all pending bookings (optimization: filter rough box in SQL first if scale needed)
    pending_bookings = db.query(Booking).filter(Booking.status == "pending").all()

    nearby = []
    for booking in pending_bookings:
        if booking.latitude is not None and booking.longitude is not None:
            dist = haversine(lon, lat, booking.longitude, booking.latitude)
            if dist <= radius:
                nearby.append(booking)

    return nearby


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(connect_db)):
    valid_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if valid_booking:
        return valid_booking
    else:
        raise HTTPException(status_code=404, detail="Booking not found")


@router.get("/user/{user_id}", response_model=List[BookingResponse])
def get_user_bookings(
    user_id: int,
    db: Session = Depends(connect_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Booking)
        .filter(Booking.customer_id == user_id)
        .order_by(Booking.date_time.desc())
        .all()
    )


@router.get("/vendor/{vendor_id}", response_model=List[BookingResponse])
def get_vendor_bookings(
    vendor_id: int,
    db: Session = Depends(connect_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Booking)
        .filter(Booking.vendor_id == vendor_id)
        .order_by(Booking.date_time.desc())
        .all()
    )


@router.post("/", response_model=BookingResponse)
def create_booking(
    data: BookingInput,
    db: Session = Depends(connect_db),
    current_user: User = Depends(get_current_user),
):
    # vendor_id is usually None initially for broadcast flow
    new_booking = Booking(**data.dict())
    if current_user.role != "customer":  # Optional Safety check
        pass

    new_booking.customer_id = (
        current_user.user_id
    )  # Force customer_id to match token owner for safety
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


@router.put("/{booking_id}/accept")
def accept_booking(
    booking_id: int,
    vendor_id: int,
    db: Session = Depends(connect_db),
    current_user: User = Depends(get_current_user),
):

    if int(vendor_id) != current_user.user_id:
        raise HTTPException(
            status_code=403, detail="You can only accept jobs for your own account"
        )
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status != "pending":
        raise HTTPException(
            status_code=400, detail="Booking already accepted or completed"
        )

    booking.vendor_id = vendor_id
    booking.status = "accepted"
    db.commit()
    return {
        "message": "Booking accepted",
        "booking_id": booking_id,
        "vendor_id": vendor_id,
    }


@router.put("/{booking_id}")
def update_booking(
    booking_id: int,
    data: BookingInput,
    db: Session = Depends(connect_db),
    current_user: User = Depends(get_current_user),
):
    db.query(Booking).filter(Booking.booking_id == booking_id).update(data.dict())
    db.commit()
    return {"message": "Booking updated"}


@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(connect_db)):
    db.query(Booking).filter(Booking.booking_id == booking_id).delete()
    db.commit()
    return {"message": "Booking deleted"}
