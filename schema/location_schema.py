from pydantic import BaseModel 

class LocationInput(BaseModel):
    user_id : int
    latitude : float
    longitude : float

