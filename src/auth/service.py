import mysql.connector
from auth.models import UserRegistration
from auth.database import user_exists, save_user, cache_activate_code
from auth.utils import generate_activation_code
from fastapi import HTTPException
import mysql
import redis

class UserService:
    def register_user(self, user:UserRegistration, db: mysql.connector.MySQLConnection, cache:redis.Redis):
        if user_exists(user.email, db):
            raise HTTPException(status_code=409, detail="This email is already taken")
        
        save_user(user, db)
        activation_code = generate_activation_code()
        cache_activate_code(user.email, activation_code, cache)
        # I choose the simplest option which is to print the value of the activation code in console
        print(activation_code)
        return {"message": "User registered sucessfully. Please check your email for the activation code"}

    def activate_account(self, email, code):
        pass