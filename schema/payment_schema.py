from pydantic import BaseModel


class PaymentInput(BaseModel):
    booking_id: int
    amount: float
    payment_method: str
    status: str
