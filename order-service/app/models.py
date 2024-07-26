# import uuid
# from sqlmodel import SQLModel, Field, Relationship
# from typing import List, Optional
# from datetime import datetime
# from uuid import UUID, uuid4

# class OrderItem(SQLModel, table=True):
#     order_item_id: Optional[int] = Field(default=None, primary_key=True)
#     order_id: UUID = Field(foreign_key="order.id")
#     product_id: Optional[str] = None
#     name: str
#     quantity: int
#     price: float
#     order: "Order" = Relationship(back_populates="items")

# class ShippingAddress(SQLModel, table=True):
#     id: UUID = Field(default_factory=uuid4, primary_key=True)
#     order_id: UUID = Field(foreign_key="order.id")
#     address: str
#     city: str
#     country: str
#     postal_code: str
#     order: "Order" = Relationship(back_populates="shipping_address")

# class Order(SQLModel, table=True):
#     id: UUID = Field(default_factory=uuid4, primary_key=True)
#     user_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
#     status: str = Field(default="PENDING")
#     total_amount: float
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     updated_at: datetime = Field(default_factory=datetime.utcnow)

#     items: List[OrderItem] = Relationship(back_populates="order")
#     shipping_address: ShippingAddress = Relationship(back_populates="order", sa_relationship_kwargs={"uselist": False})

# app/models.py
import uuid
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    orders: List["Order"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class OrderItem(SQLModel, table=True):
    order_item_id: Optional[int] = Field(default=None, primary_key=True)
    order_id: UUID = Field(foreign_key="order.id")
    product_id: Optional[str] = None
    name: str
    quantity: int
    price: float
    order: "Order" = Relationship(back_populates="items")

class ShippingAddress(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    order_id: UUID = Field(foreign_key="order.id")
    address: str
    city: str
    country: str
    postal_code: str
    order: "Order" = Relationship(back_populates="shipping_address")

class Order(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    status: str = Field(default="PENDING")
    total_amount: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    items: List[OrderItem] = Relationship(back_populates="order")
    shipping_address: Optional[ShippingAddress] = Relationship(back_populates="order")
    user: User = Relationship(back_populates="orders")

User.orders = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class OrderCreate(BaseModel):
    order_amount: float
    
    