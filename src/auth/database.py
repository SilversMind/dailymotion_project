import mysql.connector
from auth.models import UserRegistration
from auth.security import get_password_hash
import mysql
import redis

# Save user in the database
def save_user(user: UserRegistration, db : mysql.connector.connection.MySQLConnection):
    cursor = db.cursor()
    try:
        hashed_password = get_password_hash(user.password)
        cursor.execute("INSERT INTO users (email, hashed_password) VALUES (%s, %s)", 
                [user.email, hashed_password,])
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

def cache_activate_code(email:str, activation_code:str, cache:redis.Redis):
    cache.setex(name=email,time=60,value=activation_code)