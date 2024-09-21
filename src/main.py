from fastapi import FastAPI
from auth.router import auth_router
from contextlib import asynccontextmanager
from db.initialize import init_db
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from constants import LOGGER_NAME
import logging

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": "Invalid parameters provided. Please refer to the documentation to "
                 "check the expected parameters"},
    )


app.include_router(auth_router)
