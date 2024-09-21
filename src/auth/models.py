from pydantic import BaseModel, field_validator
from datetime import datetime
from src.auth.utils import validate_email

class User(BaseModel):
    id: int
    email: str
    hashed_password: str
    activation_status: bool
    created_at: datetime

    _validate_email = field_validator('email')(validate_email)