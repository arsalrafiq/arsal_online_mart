from sqlmodel import SQLModel, Field
from typing import Optional

class EmailTemplate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    notification_type: str
