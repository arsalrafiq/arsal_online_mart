# from sqlmodel import SQLModel, Field, Relationship
# from typing import Optional, List
# from datetime import datetime

# class Order(SQLModel, table=True):
#     order_id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: int
#     order_address: str
#     total_price: float
#     advance_price: Optional[float]
#     order_type: str
#     order_status: str = "pending"
#     order_date: datetime = datetime.utcnow()
#     items: List["OrderItem"] = Relationship(back_populates="order")

# class OrderItem(SQLModel, table=True):
#     order_item_id: Optional[int] = Field(default=None, primary_key=True)
#     order_id: int
#     product_id: int
#     product_item_id: int
#     product_size_id: int
#     quantity: int
#     order: Optional[Order] = Relationship(back_populates="items")

# class Payment(SQLModel, table=True):
#     payment_id: Optional[int] = Field(default=None, primary_key=True)
#     order_id: int
#     total_price: float
#     payment_method: Optional[str]
#     payment_intent_id: Optional[str]
#     payment_status: str
#     remaining_balance: float = 0
#     is_completed: bool = False
#     advance_payment_id: Optional[int] = Field(default=None, foreign_key="advancepayment.advance_payment_id")

# class AdvancePayment(SQLModel, table=True):
#     advance_payment_id: Optional[int] = Field(default=None, primary_key=True)
#     payment_id: int = Field(foreign_key="payment.payment_id")
#     advance_payment_intent_id: str
#     advance_payment_method: str
#     advance_price: float
#     advance_payment_status: str

from sqlmodel import SQLModel, Field
from typing import Optional

class Order(SQLModel, table=True):
    order_id: int = Field(default=None, primary_key=True)
    order_type: str

class Payment(SQLModel, table=True):
    payment_id: int = Field(default=None, primary_key=True)
    order_id: int
    amount: float

class PaymentForm(SQLModel):
    order_id: int
    amount: float

class RemainingPaymentModel(SQLModel):
    payment_id: int
    remaining_amount: float
