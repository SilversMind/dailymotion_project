from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from src.auth.utils import validate_email, validate_phone_number

class User(BaseModel):
    id: int
    email: str
    phone_number: Optional[str]
    hashed_password: str
    activation_status: bool
    created_at: datetime

    _validate_email = field_validator('email')(validate_email)
    _validate_phone = field_validator('phone_number')(validate_phone_number)

