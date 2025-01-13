from fastapi import FastAPI

from app.api.endpoints import users

app = FastAPI()

app.include_router(users.user_router, prefix="/api/v1/user", tags=["Users"])
