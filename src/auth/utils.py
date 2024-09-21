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