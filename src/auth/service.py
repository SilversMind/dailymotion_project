import mysql.connector
from src.auth.schemas import UserRegistration
from src.auth.database import user_exists, save_user, cache_activation_code, get_user_by_email, activate_user
from src.auth.utils import generate_activation_code
from src.auth.email_client import send_mail
from src.auth.security import password_matches
from src.auth.models import User
from src.auth.constants import ACTIVATION_CODE_LENGTH
from fastapi import HTTPException, status
import logging
import mysql
import redis
from src.constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class UserService:
    def register_user(self, user:UserRegistration, db: mysql.connector.MySQLConnection, cache:redis.Redis):
        if user_exists(user.email, db):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email is already taken")
        
        save_user(user, db)
        activation_code = generate_activation_code(ACTIVATION_CODE_LENGTH)
        cache_activation_code(user.email, activation_code, cache)
        send_mail(user.email, activation_code)
        return {"message": "User registered sucessfully. Please check your email for the activation code"}

    def activate_account(self, 
                        user: UserRegistration,
                        activation_code: str,
                        db: mysql.connector.MySQLConnection,
                        cache:redis.Redis):
        stored_user : User = get_user_by_email(user.email, db)
        if not stored_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This account is not registered")
        
        if not password_matches(user.password, stored_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed. Please check your credentials")
        
        if stored_user.activation_status is True:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This account is already activated")

        cached_activation_code = cache.get(user.email)
        if not cached_activation_code:
            raise HTTPException(status_code=status.HTTP_410_GONE, detail="The activation code has expired.")
        
        if activation_code != cached_activation_code.decode():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The provided activation code is incorrect")
        
        activate_user(user.email, db)
        return {"message": "Account sucessfully activated"}
        
            
