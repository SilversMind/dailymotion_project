from pydantic import BaseModel,field_validator, StringConstraints
from typing_extensions import Annotated, Optional
from src.auth.utils import validate_email, validate_phone_number

class UserRegistration(BaseModel):
    email: str
    password: str
    phone_number: Optional[str] = None

    _validate_email = field_validator('email')(validate_email)
    _validate_phone = field_validator('phone_number')(validate_phone_number)
    
class ActivationCode(BaseModel):
    activation_code: Annotated[
        str,
        StringConstraints(min_length=4, max_length=4, pattern=r'^\d{4}$'
        ),
    ]