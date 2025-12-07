from sqlalchemy import Column , Integer , Float , Datetime , ForeignKey
from datetime import datetime
from db.database import Base

class Location(Base):
    __tablename__ = "locations"

    location_id = Column(Integer, primary_key = True)
    user_id = Column(Integer,ForeignKey("users.user_id"))
    latitude = Column(Float)
    longitude = Column(Float)
    updated_at = Column(Datetime ,default= datetime.utcnow)
