import uvicorn
from fastapi import FastAPI

from app.api.endpoints import users
from app.core.config import setup_logging

setup_logging()

app = FastAPI()

app.include_router(users.user_router, prefix="/api/v1/user", tags=["Users"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
