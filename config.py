import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")

    # Authentication database role
    DB_AUTH_USER = os.getenv("DB_AUTH_USER")
    DB_AUTH_PASSWORD = os.getenv("DB_AUTH_PASSWORD")

    # Administrator database role
    DB_ADMIN_USER = os.getenv("DB_ADMIN_USER")
    DB_ADMIN_PASSWORD = os.getenv("DB_ADMIN_PASSWORD")

    # Lecturer database role
    DB_LECTURER_USER = os.getenv("DB_LECTURER_USER")
    DB_LECTURER_PASSWORD = os.getenv("DB_LECTURER_PASSWORD")

    # Student database role
    DB_STUDENT_USER = os.getenv("DB_STUDENT_USER")
    DB_STUDENT_PASSWORD = os.getenv("DB_STUDENT_PASSWORD")