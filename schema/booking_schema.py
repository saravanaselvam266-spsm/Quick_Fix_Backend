from pydantic import BaseModel

class BookingInput(BaseModel):
    customer_id : int
    vendor_id : int
    service_id : int
    address : str
    date_time : str
    status : str
    price : float
    


