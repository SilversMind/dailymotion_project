from pydantic import BaseModel,field_validator, StringConstraints
from typing_extensions import Annotated
from auth.utils import validate_email

class UserRegistration(BaseModel):
    email: str
    password: str

    _validate_email = field_validator('email')(validate_email)
    
class ActivationCode(BaseModel):
    activation_code: Annotated[
        str,
        StringConstraints(min_length=4, max_length=4, pattern=r'^\d{4}$'
        ),
    ]