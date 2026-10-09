from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.router import api_router

# Needs to import models to create tables
from app.models.product import Product
from app.models.order import Order, OrderItem

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router)
