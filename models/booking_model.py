from sqlalchemy import Column , Integer , String , Float , DateTime , ForeignKey  
from datetime import datetime 
from db.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key = True)
    customer_id = Column(Integer , ForeignKey("users.user_id"))
    vendor_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    service_id = Column(Integer,ForeignKey("services.service_id"))
    address = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    date_time = Column(DateTime)
    status = Column(String ,default="pending")
    completed_at = Column(DateTime, nullable=True)
    price = Column(Float)
    create_at = Column(DateTime, default = datetime.utcnow )

    


