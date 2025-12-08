from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session 
from models.service_model import Service
from schema.service_schema import ServiceInput
from dependencies import connect_db

router = APIRouter(prefix="/services")



@router.get("/")
def get_all_services(db:Session = Depends(connect_db)):
    return db.query(Service).all()


@router.get("/{service_id}")
def get_single_service(service_id: int,db:Session = Depends(connect_db)):
    valid_service = db.query(Service).filter(Service.service_id == service_id).first()
    if valid_service:
        return valid_service
    else:
        return {"message" : "Service not found"}
    

@router.post("/")
def create_service(data:ServiceInput , db: Session = Depends(connect_db)):
    new_data = Service(**data.model_dump())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


@router.put("/{service_id}")
def update_service(service_id: int,data: ServiceInput,db:Session = Depends(connect_db)):
    db.query(Service).filter(Service.service_id == service_id).update(data.model_dump())
    db.commit()
    return {"message" : "Service updated"}


@router.delete("/{service_id}")
def delete_service(service_id: int,db: Session = Depends(connect_db)):
    db.query(Service).filter(Service.service_id == service_id).delete()
    db.commit()
    return {"message" : "Service deleted"}



    
