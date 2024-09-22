from typing import Generator
import redis
import mysql.connector
from fastapi import Header, HTTPException, status
import base64
from src.auth.schemas import UserRegistration
from src.constants import MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER, REDIS_HOST, REDIS_PORT, MYSQL_DATABASE, LOGGER_NAME
import logging
from typing import Union
from pydantic import ValidationError

logger = logging.getLogger(LOGGER_NAME)
def get_cache() -> Generator[redis.Redis, None, None]:
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    try:
        yield client
    finally:
        client.close()
        
def get_db() -> Generator[mysql.connector.MySQLConnection, None, None]:
    client = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    try:
        yield client
    finally:
        client.close()


def get_basic_auth_credentials(authorization: str = Header(...)) -> Union[UserRegistration,HTTPException]:
    """
    Extracts and decodes Basic Auth credentials from the 'Authorization' header.

    This function checks if the provided authorization string uses Basic Auth. 
    If valid, it decodes the credentials and returns a UserRegistration instance. 
    If the format is invalid or the credentials are malformed, it raises 
    an appropriate HTTPException.

    Args:
        authorization (str): The 'Authorization' header containing the Basic Auth credentials.

    Raises:
        HTTPException: 
            - If the authorization header is missing or does not start with "Basic".
            - If the credentials format is invalid or if decoding fails.

    Returns:
        UserRegistration: A UserRegistration object containing the email and password.
    """
    if not authorization.startswith("Basic "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Basic Auth credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    auth_data = authorization.split(" ")[1]
    decoded_auth = base64.b64decode(auth_data).decode("utf-8")

    try:
        email, password = decoded_auth.split(":")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Basic Auth format",
        )
    try:
        return UserRegistration(email=email, password=password)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials format",
        )