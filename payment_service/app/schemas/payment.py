# app/schemas/payment.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    payment_method: str

class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    currency: str
    status: str
    payment_method: str
    stripe_payment_intent_id: Optional[str]
    created_at: datetime
    updated_at: datetime