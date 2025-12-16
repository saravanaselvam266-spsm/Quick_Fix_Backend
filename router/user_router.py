from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user_model import User
from schema.user_schema import UserInput, CustomerSignup, VendorSignup, LoginInput
from dependencies import connect_db
from models.booking_model import Booking
from sqlalchemy import func

router = APIRouter(prefix="/users")


@router.get("/")
def get_all_users(db: Session = Depends(connect_db)):
    return db.query(User).all()


@router.get("/{user_id}")
def get_single_user(user_id: int, db: Session = Depends(connect_db)):
    valid_user = db.query(User).filter(User.user_id == user_id).first()
    if valid_user:
        return valid_user
    else:
        return {"Message": "The user is not found"}


@router.post("/")
def create_user(data: UserInput, db: Session = Depends(connect_db)):
    new_data = User(**data.model_dump())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


@router.put("/{user_id}")
def update_user(user_id: int, data: UserInput, db: Session = Depends(connect_db)):
    db.query(User).filter(User.user_id == user_id).update(data.model_dump())
    db.commit()
    return {"message": "User updated"}


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(connect_db)):
    db.query(User).filter(User.user_id == user_id).delete()
    db.commit()
    return {"message": "User deleted"}


@router.post("/customers")
def create_customer(data: CustomerSignup, db: Session = Depends(connect_db)):
    new_user = User(**data.model_dump(), role="customer")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/vendors")
def create_vendor(data: VendorSignup, db: Session = Depends(connect_db)):
    vendor_data = data.model_dump()
    vendor_data["role"] = "vendor"
    vendor_data["rating"] = 0.0

    new_vendor = User(**vendor_data)

    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)

    return {
        "message": "Vendor created successfully",
        "vendor_id": new_vendor.user_id,
        "name": new_vendor.name,
        "role": new_vendor.role,
    }


@router.post("/login")
def login_user(data: LoginInput, db: Session = Depends(connect_db)):

    user = (
        db.query(User)
        .filter((User.email == data.username) | (User.phone == data.username))
        .first()
    )

    if not user:
        return {"error": "User not found"}

    if user.password_hash != data.password:
        return {"error": "Invalid password"}

    return {"user_id": user.user_id, "name": user.name, "role": user.role}


@router.get("/dashboard/{user_id}")
def user_dashboard(user_id: int, db: Session = Depends(connect_db)):

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return {"error": "User not found"}

    # Upcoming + in-progress bookings count
    upcoming_count = (
        db.query(Booking)
        .filter(
            Booking.customer_id == user_id,
            Booking.status.in_(["upcoming", "in_progress"]),
        )
        .count()
    )

    # Completed bookings count
    completed_count = (
        db.query(Booking)
        .filter(Booking.customer_id == user_id, Booking.status == "completed")
        .count()
    )

    # Total spent
    total_spent = (
        db.query(func.coalesce(func.sum(Booking.price), 0))
        .filter(Booking.customer_id == user_id, Booking.status == "completed")
        .scalar()
    )

    # All bookings
    bookings = (
        db.query(Booking)
        .filter(Booking.customer_id == user_id)
        .order_by(Booking.date_time.desc())
        .all()
    )

    return {
        "user": {"name": user.name, "role": user.role},
        "summary": {
            "upcoming": upcoming_count,
            "completed": completed_count,
            "total_spent": total_spent,
        },
        "bookings": bookings,
    }


@router.get("/dashboard/summary/{user_id}")
def user_dashboard_summary(user_id: int, db: Session = Depends(connect_db)):

    upcoming = db.query(Booking).filter(
        Booking.user_id == user_id,
        Booking.status.in_(["upcoming", "in-progress"])
    ).count()

    completed = db.query(Booking).filter(
        Booking.user_id == user_id,
        Booking.status == "completed"
    ).count()

    total_spent = db.query(Booking).filter(
        Booking.user_id == user_id,
        Booking.status == "completed"
    ).with_entities(func.sum(Booking.price)).scalar() or 0

    return {
        "upcoming": upcoming,
        "completed": completed,
        "total_spent": total_spent
    }
