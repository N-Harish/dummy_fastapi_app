from sqlalchemy.orm import Session
from app.models.order import Order, OrderStatus

class OrderRepository:
    def get(self, db: Session, order_id: int):
        return db.query(Order).filter(Order.id == order_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Order).offset(skip).limit(limit).all()

    def update_status(self, db: Session, db_obj: Order, status: OrderStatus):
        db_obj.status = status
        db.commit()
        db.refresh(db_obj)
        return db_obj

order_repo = OrderRepository()
