import pytest
from typing import Generator
import mysql.connector
import redis
from fastapi.testclient import TestClient
from src.constants import MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER, MYSQL_TEST_DATABASE, REDIS_HOST, REDIS_PORT, MYSQL_PORT
from src.main import app
from src.auth.dependencies import get_db, get_cache

@pytest.fixture(scope="function", autouse=True)
def clear_database(get_test_db):
    cursor = get_test_db.cursor()
    cursor.execute("DELETE FROM users")
    get_test_db.commit()
    cursor.close()

@pytest.fixture(scope="module")
def get_test_cache() -> Generator[redis.Redis, None, None]:
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=1)
    try:
        yield client
    finally:
        client.close()

@pytest.fixture(scope="module")
def get_test_db() -> Generator[mysql.connector.MySQLConnection, None, None]:
    client = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_TEST_DATABASE,
        port=MYSQL_PORT
    )
    try:
        yield client
    finally:
        client.close()

@pytest.fixture
def client(get_test_db, get_test_cache) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = lambda: get_test_db
    app.dependency_overrides[get_cache] = lambda: get_test_cache

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
