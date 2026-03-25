from sqlalchemy import Column, Integer, String, Float
from db.database import Base


class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True)
    service_name = Column(String)
    description = Column(String)
    base_price = Column(Float)
    vehicle_type = Column(String)
