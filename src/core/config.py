import logging

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


def setup_logging():
    logging.basicConfig(
        filename="logging.log",
        format="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]",
        datefmt="%d/%m/%Y %I:%M:%S",
        encoding="utf-8",
        filemode="a",
        level=logging.WARNING,
    )


setup_logging()


class Settings(BaseSettings):
    DEBUG: bool

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str

    DATABASE_HOST_TEST: str
    DATABASE_PORT_TEST: int
    DATABASE_USER_TEST: str
    DATABASE_PASSWORD_TEST: str
    DATABASE_NAME_TEST: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()
