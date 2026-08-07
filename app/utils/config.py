import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "Notice Board API")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "False") == "True"
    DATABASE_PATH = os.getenv("DATABASE_PATH", "data/notice_board.db")


settings = Settings()