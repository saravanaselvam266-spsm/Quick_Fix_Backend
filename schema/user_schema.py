from pydantic import BaseModel

class UserInput(BaseModel):
    name : str
    email : str
    phone : int
    password_hash : str
    role : str
    address : str
    specialty : str
    experience_year : float
    rating : float
    availability : bool
    
