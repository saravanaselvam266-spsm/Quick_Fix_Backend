from pydantic import BaseModel
from typing import Optional


class UserInput(BaseModel):
    name: str
    email: str
    phone: str
    role: str
    address: str
    specialty: str
    experience_years: float
    rating: float
    availability: bool


class CustomerSignup(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    address: str


class AdminSignup(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    address: Optional[str] = None


class VendorSignup(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    address: str
    specialty: Optional[str] = None
    experience_years: Optional[float] = None
    availability: Optional[bool] = True


class LoginInput(BaseModel):
    username: str
    password: str


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
