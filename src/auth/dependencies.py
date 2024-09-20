from typing import Generator
import redis
import mysql.connector
from constants import MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER, REDIS_HOST, REDIS_PORT, MYSQL_DATABASE

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