from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.schemas.order import OrderResponse
from app.models.order import OrderStatus
from app.repositories.product_repo import product_repo
from app.repositories.order_repo import order_repo

router = APIRouter()


@router.get("/heath/")
def health():
    return "App Running"
