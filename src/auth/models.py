from pydantic import BaseModel,field_validator
import re

class UserRegistration(BaseModel):
    email: str
    password: str

    @field_validator('email')
    def validate_email(cls, value: str):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise ValueError('Invalid email address format')
        return value