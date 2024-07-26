# # app/schemas.py
# from uuid import UUID
# from pydantic import BaseModel
# from typing import List, Optional
# from datetime import datetime


# class OrderItemCreate(BaseModel):
#     product_id: Optional[str] = None
#     name: str
#     quantity: int
#     price: float

# class ShippingAddressCreate(BaseModel):
#     address: str
#     city: str
#     country: str
#     postal_code: str

# class OrderCreate(BaseModel):
#     user_id: str
#     order_amount: float
#     items: List[OrderItemCreate]
#     shipping_address: ShippingAddressCreate

# class OrderResponse(BaseModel):
#     id: UUID
#     user_id: str
#     status: str
#     total_amount: float
#     created_at: datetime
#     updated_at: datetime


from uuid import UUID
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: Optional[str] = None
    name: str
    quantity: int
    price: float

class OrderItemResponse(OrderItemCreate):
    order_item_id: int

class ShippingAddressCreate(BaseModel):
    address: str
    city: str
    country: str
    postal_code: str

class ShippingAddressResponse(ShippingAddressCreate):
    id: UUID

class OrderCreate(BaseModel):
    user_id: UUID
    total_amount: float
    items: List[OrderItemCreate]
    shipping_address: ShippingAddressCreate

class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    status: str
    total_amount: float
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse]
    shipping_address: ShippingAddressResponse

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    is_active: bool
    is_admin: bool

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
