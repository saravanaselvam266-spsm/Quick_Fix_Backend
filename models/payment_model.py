from sqlalchemy import Column , Integer , String , Float , Datetime ,ForeignKey
from datetime import datetime
from db.database import Base

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer,primary_key = True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"))
    amount = Column(Float)
    payment_method = Column(String)
    status = Column(String)
    payment_date = Column(Datetime, default= datetime.utcnow)




