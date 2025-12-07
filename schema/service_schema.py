from pydantic import BaseModel

class ServiceInput(BaseModel):
    service_name : str
    description : str
    base_price : float
    vehicle_type : str
    