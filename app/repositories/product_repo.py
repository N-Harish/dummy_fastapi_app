from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductRepository:
    def get(self, db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Product).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: ProductCreate):
        db_obj = Product(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Product, obj_in: ProductUpdate):
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, product_id: int):
        db_obj = self.get(db, product_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

product_repo = ProductRepository()
