from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.product import ProductResponse
from app.schemas.order import OrderCreate, OrderResponse
from app.repositories.product_repo import product_repo
from app.repositories.order_repo import order_repo
from app.services.order_service import order_service

router = APIRouter()

@router.get("/products/", response_model=List[ProductResponse])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return product_repo.get_multi(db, skip=skip, limit=limit)

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = product_repo.get(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/checkout/", response_model=OrderResponse)
def place_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db=db, order=order)

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = order_repo.get(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
