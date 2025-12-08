from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from models.payment_model import Payment
from schema.payment_schema import PaymentInput
from dependencies import connect_db

router = APIRouter(prefix="/payments")

@router.get("/")
def get_all_payments(db:Session = Depends(connect_db)):
    return db.query(Payment).all()


@router.get("/{payment_id}")
def get_single_payment(payment_id: int, db:Session = Depends(connect_db)):
    valid_payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if valid_payment :
        return valid_payment
    else:
        return {"message" : "Payment not found"}
    

@router.post("/")
def create_payment(data: PaymentInput, db: Session = Depends(connect_db)):
    new_payment = Payment(**data.model_dump())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


@router.put("/{payment_id}")
def update_payment(payment_id: int, data: PaymentInput, db: Session = Depends(connect_db)):
    db.query(Payment).filter(Payment.payment_id == payment_id).update(data.model_dump())
    db.commit()
    return {"message" : "Payment updated"}

@router.delete("/{payment_id}")
def delete_payment(payment_id: int,db: Session = Depends(connect_db)):
    db.query(Payment).filter(Payment.payment_id == payment_id).delete()
    db.commit()
    return {"message" : "Payment deleted"}


