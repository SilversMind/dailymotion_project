import mysql.connector
from src.auth.schemas import UserRegistration
from src.auth.models import User
from src.auth.security import get_password_hash
from src.auth.constants import ACTIVATION_CODE_EXPIRATION_TIME
import mysql
import redis

def save_user(user: UserRegistration, db : mysql.connector.MySQLConnection):
    cursor = db.cursor()
    try:
        hashed_password = get_password_hash(user.password)
        cursor.execute("INSERT INTO users (email, phone_number, hashed_password) VALUES (%s,%s, %s)", 
                [user.email, user.phone_number, hashed_password])
        db.commit()
    finally:
        cursor.close()

def get_user_by_email(email: str, db: mysql.connector.MySQLConnection) -> User:
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        
        if result is None:
            return None

        user = User(**result)
        return user
    finally:
        cursor.close()

def activate_user(email: str, db: mysql.connector.MySQLConnection) -> User:
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE users SET activation_status = %s WHERE email = %s",
            (1, email)
        )
        db.commit()
    finally:
        cursor.close()
    
def user_exists(email: str, db : mysql.connector.connection.MySQLConnection):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        return result['count'] > 0 
    finally:
        cursor.close()

def cache_activation_code(email:str, activation_code:str, cache:redis.Redis):
    cache.setex(name=email,time=ACTIVATION_CODE_EXPIRATION_TIME,value=activation_code)