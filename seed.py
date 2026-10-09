from app.core.database import SessionLocal, engine, Base
from app.models.product import Product
from app.models.order import Order, OrderItem

def seed_db():
    # Ensure tables are created before we try to seed
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if we already have products
    existing = db.query(Product).first()
    if existing:
        print("Database already seeded with products.")
        db.close()
        return

    dummy_products = [
        Product(name="Wireless Mouse", description="Ergonomic wireless mouse with fast response.", price=25.99, stock=50),
        Product(name="Mechanical Keyboard", description="RGB mechanical keyboard with tactile switches.", price=89.99, stock=20),
        Product(name="USB-C Hub", description="7-in-1 USB-C Hub with HDMI and SD card reader.", price=34.50, stock=100),
        Product(name="Noise Cancelling Headphones", description="Over-ear Bluetooth headphones with active noise cancellation.", price=199.99, stock=15),
        Product(name="Laptop Stand", description="Adjustable aluminum laptop stand.", price=45.00, stock=30),
    ]
    
    db.add_all(dummy_products)
    db.commit()
    print(f"Successfully added {len(dummy_products)} dummy products.")
    db.close()

if __name__ == "__main__":
    seed_db()
