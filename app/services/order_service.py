from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import OrderCreate
from app.repositories.product_repo import product_repo

class OrderService:
    def create_order(self, db: Session, order: OrderCreate):
        total_price = 0.0
        order_items = []
        
        for item in order.items:
            product = product_repo.get(db, item.product_id)
            if not product:
                raise HTTPException(status_code=400, detail=f"Product with id {item.product_id} not found")
            if product.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Not enough stock for product '{product.name}'")
            
            price = product.price * item.quantity
            total_price += price
            product.stock -= item.quantity
            
            order_item = OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                price_per_item=product.price
            )
            order_items.append(order_item)
            
        db_order = Order(
            customer_name=order.customer_name,
            customer_email=order.customer_email,
            total_price=total_price,
            status=OrderStatus.PENDING
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        for oi in order_items:
            oi.order_id = db_order.id
            db.add(oi)
        
        db.commit()
        db.refresh(db_order)
        return db_order

order_service = OrderService()
