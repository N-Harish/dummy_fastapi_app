from pydantic import BaseModel
from typing import List
from app.models.order import OrderStatus

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_per_item: float
    model_config = {"from_attributes": True}

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    customer_email: str
    total_price: float
    status: OrderStatus
    items: List[OrderItemResponse]
    model_config = {"from_attributes": True}
