import random
import re

def generate_activation_code(length):
    code = random.randint(0, 10**length - 1)
    return str(code).zfill(length)

def validate_email(value: str) -> str:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+$'
    if not re.match(email_regex, value):
        raise ValueError('Invalid email address format')
    return value

def validate_phone_number(value: str) -> str:
    if value:
        sms_regex  = r"^\+?[1-9]\d{9,14}$"
        if not re.match(sms_regex, value):
            raise ValueError('Invalid phone number format')
    return value
    