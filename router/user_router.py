from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user_model import User
from schema.user_schema import UserInput, CustomerSignup, VendorSignup, LoginInput, AdminSignup

from dependencies import connect_db, get_current_user
from models.booking_model import Booking
from sqlalchemy import func
from core.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/users" , tags=["Users"])


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
    # 1. Hashing
    user_dict = data.model_dump()
    
    # Check if user already exists
    existing_user = db.query(User).filter((User.email == user_dict['email']) | (User.phone == user_dict['phone'])).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email or phone already exists")

    # Handle different field names if necessary, but assuming password_hash is passed
    # If the input sends "password", we hash it. 
    if 'password' in user_dict:
        user_dict['password_hash'] = get_password_hash(user_dict.pop('password'))
    elif 'password_hash' in user_dict:
        # Fallback if somehow it came through (unlikely with strict schema)
        user_dict['password_hash'] = get_password_hash(user_dict['password_hash'])

    new_data = User(**user_dict)
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
    # 1. Hashing
    user_dict = data.model_dump()

    # Check if user already exists
    existing_user = db.query(User).filter((User.email == user_dict['email']) | (User.phone == user_dict['phone'])).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email or phone already exists")

    if 'password' in user_dict:
         user_dict['password_hash'] = get_password_hash(user_dict.pop('password'))
    else:
         user_dict['password_hash'] = get_password_hash(user_dict.get('password_hash'))

    # Explicitly set role
    new_user = User(**user_dict, role="customer")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/vendors")
def create_vendor(data: VendorSignup, db: Session = Depends(connect_db)):
    vendor_data = data.model_dump()
    vendor_data["role"] = "vendor"
    vendor_data["rating"] = 0.0
    
    # Check if user already exists
    existing_user = db.query(User).filter((User.email == vendor_data['email']) | (User.phone == vendor_data['phone'])).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email or phone already exists")
    
    # 1. Hashing
    if 'password' in vendor_data:
         vendor_data['password_hash'] = get_password_hash(vendor_data.pop('password'))
    
    # Ensure mapping matches model
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


@router.post("/admins")
def create_admin(data: AdminSignup, db: Session = Depends(connect_db)):
    # 1. Hashing
    user_dict = data.model_dump()
    
    # Check if user already exists
    existing_user = db.query(User).filter((User.email == user_dict['email']) | (User.phone == user_dict['phone'])).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email or phone already exists")

    if 'password' in user_dict:
         user_dict['password_hash'] = get_password_hash(user_dict.pop('password'))
    
    # 2. Set Role
    new_admin = User(**user_dict, role="admin")
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    
    return {
        "message": "Admin created successfully",
        "user_id": new_admin.user_id,
        "role": new_admin.role
    }


@router.post("/login")
def login_user(data: LoginInput, db: Session = Depends(connect_db)):

    # Robust login: Strip whitespace and handle case-insensitive email
    username = data.username.strip()
    
    # Check case-insensitive email OR phone
    # func.lower() requires 'from sqlalchemy import func' which is already imported
    user = (
        db.query(User)
        .filter(
            (func.lower(User.email) == func.lower(username)) | 
            (User.phone == username)
        )
        .first()
    )

    if not user:
        return {"error": "User not found"}

    # 1. Verify Password
    if not verify_password(data.password, user.password_hash):
        return {"error": "Invalid password"}

    # 2. Create Token
    access_token = create_access_token(data={"sub": str(user.user_id), "role": user.role})

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.user_id, 
        "name": user.name, 
        "role": user.role
    }


@router.get("/dashboard/{user_id}")
def user_dashboard(user_id: int, db: Session = Depends(connect_db), current_user: User = Depends(get_current_user)):

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return {"error": "User not found"}

    # Upcoming + in-progress bookings count
    upcoming_count = (
        db.query(Booking)
        .filter(
            Booking.customer_id == user_id,
            Booking.status.in_(["upcoming", "in_progress", "pending", "accepted"]),
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
def user_dashboard_summary(user_id: int, db: Session = Depends(connect_db), current_user: User = Depends(get_current_user)):

    upcoming = db.query(Booking).filter(
        Booking.customer_id == user_id,
        Booking.status.in_(["upcoming", "in_progress", "pending", "accepted"])
    ).count()

    completed = db.query(Booking).filter(
        Booking.customer_id == user_id,
        Booking.status == "completed"
    ).count()

    total_spent = db.query(func.coalesce(func.sum(Booking.price), 0)).filter(
        Booking.customer_id == user_id,
        Booking.status == "completed"
    ).scalar()

    return {
        "upcoming": upcoming,
        "completed": completed,
        "total_spent": total_spent
    }

@router.get("/vendor/stats/{vendor_id}")
def get_vendor_stats(vendor_id: int, db: Session = Depends(connect_db), current_user: User = Depends(get_current_user)):
    from datetime import datetime, timedelta
    
    today = datetime.utcnow().date()
    start_of_week = today - timedelta(days=today.weekday())
    
    # Simple query helper
    def get_earnings(query_filter):
        return db.query(func.coalesce(func.sum(Booking.price), 0)).filter(
            Booking.vendor_id == vendor_id,
            *query_filter
        ).scalar()
        
    def get_count(query_filter):
        return db.query(Booking).filter(
            Booking.vendor_id == vendor_id,
            *query_filter
        ).count()

    today_earnings = get_earnings([
        func.date(Booking.date_time) == today,
        Booking.status.in_(["completed"]) 
    ])

    week_earnings = get_earnings([
        func.date(Booking.date_time) >= start_of_week,
        Booking.status.in_(["completed"]) 
    ])
    
    active_jobs = get_count([
        Booking.status == "accepted"
    ])
    
    completed_today = get_count([
        func.date(Booking.date_time) == today,
        Booking.status == "completed"
    ])

    return {
        "today_earnings": today_earnings,
        "week_earnings": week_earnings,
        "active_jobs": active_jobs,
        "completed_today": completed_today
    }






