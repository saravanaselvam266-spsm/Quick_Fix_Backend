from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import connect_db
from models.location_model import Location
from schema.location_schema import LocationInput

router = APIRouter(prefix= "/locations")


@router.get("/")
def get_locations(db: Session = Depends(connect_db)):
    return db.query(Location).all()


@router.get("/{location_id}")
def get_location(location_id: int, db: Session = Depends(connect_db)):
    valid_location = db.query(Location).filter(Location.location_id == location_id).first()
    if valid_location:
        return valid_location
    else:
        return {"message" : "Location not found"}



@router.post("/")
def create_location(data: LocationInput, db: Session = Depends(connect_db)):
    new_location = Location(**data.model_dump())
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location


@router.put("/{location_id}")
def update_location(location_id: int, data: LocationInput, db: Session = Depends(connect_db)):
    db.query(Location).filter(Location.location_id == location_id).update(data.model_dump())
    db.commit()
    return {"message": "Location updated"}



@router.delete("/{location_id}")
def delete_location(location_id: int, db: Session = Depends(connect_db)):
    db.query(Location).filter(Location.location_id == location_id).delete()
    db.commit()
    return {"message": "Location deleted"}

