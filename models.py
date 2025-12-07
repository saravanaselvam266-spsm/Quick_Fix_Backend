from sqlalchemy import Column , String , Float ,Integer
from database import Base

class Users(Base):
    # defining the table name 
    __tablename__ = "users"

    users_id = Column(Integer, Primary_key = True)
    user_name = Column(String)
    user_email = Column(String)
    user_phone = Column(Integer)
    