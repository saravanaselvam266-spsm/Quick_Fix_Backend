from db.database import SessionLocal, engine, Base
from models.user_model import User
from models.service_model import Service

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed():
    # 1. Create Demo User (Customer)
    if not db.query(User).filter(User.email == "user@example.com").first():
        customer = User(
            name="Demo User",
            email="user@example.com",
            phone="1234567890",
            # Storing plain text because user_router.py compares with != plain_text
            password_hash="password", 
            role="customer",
            address="123 Main St"
        )
        db.add(customer)
        print("Created Demo Customer (ID: 1 probably)")

    # 2. Create Demo User (Mechanic)
    if not db.query(User).filter(User.email == "mechanic@example.com").first():
        mechanic = User(
            name="Mike Mechanic",
            email="mechanic@example.com",
            phone="0987654321",
            password_hash="password",
            role="vendor",
            address="Mechanic Shop",
            specialty="Car Repair",
            availability=True
        )
        db.add(mechanic)
        print("Created Demo Mechanic")

    # 3. Create Services
    services = [
        {"name": "Bike Service", "price": 25.0, "desc": "Full bike checkup"},
        {"name": "Car Service", "price": 75.0, "desc": "Oil change and diagnostics"},
        {"name": "Emergency Help", "price": 50.0, "desc": "Roadside assistance"}
    ]

    for s in services:
        if not db.query(Service).filter(Service.service_name == s["name"]).first():
            new_service = Service(
                service_name=s["name"],
                description=s["desc"],
                base_price=s["price"],
                vehicle_type="All"
            )
            db.add(new_service)
            print(f"Created Service: {s['name']}")

    db.commit()
    db.close()
    print("Seeding Complete!")

if __name__ == "__main__":
    seed()
