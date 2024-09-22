import bcrypt

def password_matches(plain_password: str, hashed_password: str) -> bool:
    """
    Compares a plain password with a hashed password to check if they match.

    Args:
        plain_password: The plain text password entered by the user.
        hashed_password: The hashed password stored in the database.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generates a hashed version of the provided password.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password as a string.
    """
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf8')
