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

@router.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return product_repo.create(db, obj_in=product)

@router.get("/products/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return product_repo.get_multi(db, skip=skip, limit=limit)

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = product_repo.get(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_repo.update(db, db_obj=db_product, obj_in=product)

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = product_repo.delete(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}

@router.get("/orders/", response_model=List[OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return order_repo.get_multi(db, skip=skip, limit=limit)

@router.put("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status: OrderStatus, db: Session = Depends(get_db)):
    db_order = order_repo.get(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_repo.update_status(db, db_obj=db_order, status=status)
