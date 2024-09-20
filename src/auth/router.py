from fastapi import APIRouter, HTTPException, Depends
from auth.service import UserService
from auth.models import UserRegistration
from auth.dependencies import get_db, get_cache

auth_router = APIRouter()

@auth_router.post("/register")
def register_user(user:UserRegistration,
                user_service: UserService = Depends(UserService),
                db = Depends(get_db)):
        
        return user_service.register_user(user, db)
 