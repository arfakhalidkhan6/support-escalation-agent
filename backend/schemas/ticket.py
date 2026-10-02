from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class TicketRequest(BaseModel):
    message: str = Field(..., description="Customer support ticket message")
    customer_name: Optional[str] = None
    customer_email: Optional[EmailStr] = None
