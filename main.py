import uvicorn
from fastapi import FastAPI

from src.core.config import setup_logging
from src.modules.users.endpoints import users

setup_logging()

app = FastAPI()

app.include_router(users.user_router, prefix="/api/v1/user", tags=["Users"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
