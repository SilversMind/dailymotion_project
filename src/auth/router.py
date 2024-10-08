from fastapi import APIRouter, Depends
from src.auth.service import UserService
from src.auth.schemas import UserRegistration, ActivationCode
from src.auth.dependencies import get_db, get_cache, get_basic_auth_credentials

auth_router = APIRouter()

@auth_router.post("/register", status_code=201,responses={
        201: {"description": "User registered successfully"},
        409: {"description": "Conflict: Email already taken"},
        400: {"description": "Bad Request: Invalid input"}})
def register_user(user:UserRegistration,
                user_service: UserService = Depends(UserService),
                db = Depends(get_db),
                cache = Depends(get_cache)):
        
        return user_service.register_user(user, db, cache)

@auth_router.post("/activate", responses={
        200: {"description": "Account sucessfully_activated"},
        409: {"description": "Conflict: Email already taken"},
        401: {"description": "Unauthorized: Authentication failed"},
        400: {"description": "Bad Request: Invalid input"}})
def activate_code(activation_code: ActivationCode,
                user: UserRegistration = Depends(get_basic_auth_credentials),
                user_service: UserService = Depends(UserService),
                db = Depends(get_db),
                cache = Depends(get_cache)):
        return user_service.activate_account(user, activation_code.activation_code, db, cache)
 