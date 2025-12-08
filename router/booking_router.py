from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import connect_db
from models.booking_model import Booking
from schema.booking_schema import BookingInput

router = APIRouter(prefix="/bookings")


@router.get("/")
def get_bookings(db: Session = Depends(connect_db)):
    return db.query(Booking).all()

@router.get("/{booking_id}")
def get_booking(booking_id: int, db: Session = Depends(connect_db)):
    valid_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if valid_booking:
        return valid_booking
    else:
        return {"message" : "Booking not found"}

@router.post("/")
def create_booking(data: BookingInput, db: Session = Depends(connect_db)):
    new_booking = Booking(**data.model_dump())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


@router.put("/{booking_id}")
def update_booking(booking_id: int, data: BookingInput, db: Session = Depends(connect_db)):
    db.query(Booking).filter(Booking.booking_id == booking_id).update(data.model_dump())
    db.commit()
    return {"message": "Booking updated"}


@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(connect_db)):
    db.query(Booking).filter(Booking.booking_id == booking_id).delete()
    db.commit()
    return {"message": "Booking deleted"}
