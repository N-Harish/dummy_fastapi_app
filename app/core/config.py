import os

class Settings:
    PROJECT_NAME: str = "E-Commerce API"
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")

settings = Settings()
