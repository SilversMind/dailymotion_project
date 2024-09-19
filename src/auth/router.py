from fastapi import APIRouter, Depends
from auth.dependencies import get_cache
auth_router = APIRouter()

@auth_router.get("/test")
def test(cache=Depends(get_cache)):
    cache.set("value", 0)
    return f"It works ! it equals {int(cache.get('value')) + 1}"