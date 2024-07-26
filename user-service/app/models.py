from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    hashed_password: str
    is_admin: bool = Field(default=False)  # New field to distinguish admin users

class UserCreate(SQLModel):
    name: str
    email: str
    password: str
    is_admin: bool = Field(default=False)  # Allow setting admin status on creation

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None  # Allow updating admin status
