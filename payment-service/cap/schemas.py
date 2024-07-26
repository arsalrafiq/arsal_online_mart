from typing import Optional
from pydantic import BaseModel

class PaymentForm(BaseModel):
    order_id: int
    total_price: float
    payment_method_id: Optional[str]
    advance_payment: Optional["AdvancePaymentForm"]

class AdvancePaymentForm(BaseModel):
    advance_price: float
    advance_payment_method_id: str

class RemainingPaymentModel(BaseModel):
    payment_method_id: str
    remaining_balance: float
