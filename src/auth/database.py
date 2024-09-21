import mysql.connector
from auth.schemas import UserRegistration
from auth.models import User
from auth.security import get_password_hash
import mysql
import redis

def save_user(user: UserRegistration, db : mysql.connector.connection.MySQLConnection):
    cursor = db.cursor()
    try:
        hashed_password = get_password_hash(user.password)
        cursor.execute("INSERT INTO users (email, hashed_password) VALUES (%s, %s)", 
                [user.email, hashed_password,])
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
    cache.setex(name=email,time=60,value=activation_code)