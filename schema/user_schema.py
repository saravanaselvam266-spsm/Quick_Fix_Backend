from pydantic import BaseModel
from typing import Optional

class UserInput(BaseModel):
    name : str
    email : str
    phone : str
    password_hash : str
    role : str
    address : str
    specialty : str
    experience_year : float
    rating : float
    availability : bool

class CustomerSignup(BaseModel):
    name: str
    email: str
    phone: str
    password_hash: str
    address: str

class VendorSignup(BaseModel):
    name: str
    email: str
    phone: str
    password_hash: str
    address: str
    specialty: Optional[str] = None
    experience_years: Optional[float] = None  
    availability: Optional[bool] = True

class LoginInput(BaseModel):
    username: str  
    password: str

