from app import create_app
from models import db, Product, User
from utils import hash_password, create_token
import os

app = create_app()

with app.app_context():
    # create DB and tables
    db.create_all()

    # Seed admin user if not exists
    admin_email = "admin@hypeneko.local"
    if not User.query.filter_by(email=admin_email).first():
        admin = User(
            email=admin_email,
            password_hash=hash_password("admin123"),
            is_admin=True,
            token=create_token()
        )
        db.session.add(admin)
        print("Seeded admin:", admin_email)
    else:
        admin = User.query.filter_by(email=admin_email).first()

    # Seed sample products (if none exist)
    if Product.query.count() == 0:
        sample_products = [
            {"sku": "HYP-ANGEL", "name": "ANGEL Black Tee", "description": "Premium cotton black tee with minimal chest logo.", "price": 699.0, "image": "images/ANGEL_FRONT.png"},
            {"sku": "HYP-MOON", "name": "Moon Graphic Tee", "description": "Oversized streetwear with bold moon back print.", "price": 699.0, "image": "images/MOON_FRONT.png"},
            {"sku": "HYP-STAR", "name": "Star Cap", "description": "Embroidered cap with premium stitching.", "price": 399.0, "image": "images/STAR_CAP.png"},
        ]
        for p in sample_products:
            prod = Product(sku=p['sku'], name=p['name'], description=p['description'], price=p['price'], image=p['image'])
            db.session.add(prod)
        print("Seeded sample products.")

    db.session.commit()
    print("DB initialization done.")
    print("Admin token (for testing):", admin.token)
