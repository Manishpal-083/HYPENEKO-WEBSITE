import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from models import db, Product, CartItem, User
from utils import create_token, hash_password, verify_password

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'hypeneko.db')

def create_app():
    # STATIC FOLDER FIXED (always points to project root)
    ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

    app = Flask(
        __name__,
        static_folder=ROOT_DIR,          # serve index.html, images, css
        static_url_path="/"
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)
    db.init_app(app)

    # ------- TEST ROUTE --------
    @app.route("/api/test")
    def test():
        return jsonify({"msg": "API working"}), 200

    # ------- PRODUCTS ROUTES --------
    @app.route('/api/products', methods=['GET'])
    def get_products():
        products = Product.query.all()
        out = []
        for p in products:
            out.append({
                "id": p.id,
                "sku": p.sku,
                "name": p.name,
                "description": p.description,
                "price": p.price,
                "image": p.image
            })
        return jsonify(out), 200

    @app.route('/api/product/<int:pid>', methods=['GET'])
    def get_product(pid):
        p = Product.query.get(pid)
        if not p:
            return jsonify({"error": "product not found"}), 404
        return jsonify({
            "id": p.id,
            "sku": p.sku,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "image": p.image
        }), 200

    # ------- CART ROUTES --------
    @app.route('/api/cart', methods=['POST'])
    def add_to_cart():
        data = request.json
        pid = data.get("product_id")
        qty = int(data.get("qty", 1))

        item = CartItem(product_id=pid, qty=qty)
        db.session.add(item)
        db.session.commit()
        return jsonify({"ok": True}), 200

    @app.route('/api/cart', methods=['GET'])
    def get_cart():
        items = CartItem.query.all()
        out = []
        total = 0
        for i in items:
            out.append({
                "id": i.id,
                "qty": i.qty,
                "product": {
                    "name": i.product.name,
                    "price": i.product.price,
                    "image": i.product.image
                }
            })
            total += i.product.price * i.qty
        return jsonify({"items": out, "total": total}), 200

    # ------- SERVE INDEX --------
    @app.route("/")
    def home():
        return app.send_static_file("index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    print("Server running at http://127.0.0.1:5000")
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

