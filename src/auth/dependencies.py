from typing import Generator
import redis
import mysql.connector
from fastapi import Header, HTTPException, status

import base64
from auth.schemas import UserRegistration
from constants import MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER, REDIS_HOST, REDIS_PORT, MYSQL_DATABASE, LOGGER_NAME
import logging
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


def get_basic_auth_credentials(authorization: str = Header(...)):
    """
    Extract and decode Basic Auth credentials from the 'Authorization' header.
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