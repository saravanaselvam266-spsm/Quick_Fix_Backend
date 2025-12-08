from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from models.user_model import User
from schema.user_schema import UserInput
from dependencies import connect_db

router = APIRouter(prefix="/users")


@router.get("/")
def get_all_users(db:Session = Depends(connect_db)):
    return db.query(User).all()


@router.get("/{user_id}")
def get_single_user(user_id : int,db:Session = Depends(connect_db)):
    valid_user = db.query(User).filter(User.user_id == user_id).first()
    if valid_user :
        return valid_user
    else:
        return {"Message" : "The user is not found"}
    

@router.post("/")
def create_user(data:UserInput,db:Session = Depends(connect_db)):
    new_data = User(**data.model_dump())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


@router.put("/{user_id}")
def update_user(user_id : int ,data : UserInput ,db:Session = Depends(connect_db)):
    db.query(User).filter(User.user_id == user_id).update(data.model_dump())
    db.commit()
    return {"message" : "User updated"}



@router.delete("/{user_id}")
def delete_user(user_id : int, db:Session =Depends(connect_db)):
    db.query(User).filter(User.user_id == user_id).delete()
    db.commit()
    return {"message" : "User deleted"}
    







