from sqlalchemy import Column , Integer , String , Boolean , Float , DateTime 
from datetime import datetime
from db.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key = True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    password_hash = Column(String)
    role = Column(String)
    address = Column(String)
    specialty = Column(String)
    experience_years = Column(Float)
    rating = Column(Float)
    availability = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)

    
    