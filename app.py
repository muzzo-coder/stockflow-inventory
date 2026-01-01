from flask import Flask, request, jsonify
from sqlalchemy import func
from datetime import datetime, timedelta
from models import db, Company, Warehouse, Product, Inventory, Supplier, ProductSupplier, Sale

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json() or {}

    required = ["name", "sku", "company_id"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if Product.query.filter_by(sku=data["sku"]).first():
        return jsonify({"error": "SKU already exists"}), 409

    try:
        product = Product(
            name=data["name"],
            sku=data["sku"],
            company_id=data["company_id"],
            price=data.get("price", 0.00)
        )
        db.session.add(product)

        if "warehouse_id" in data and "initial_quantity" in data:
            inventory = Inventory(
                product_id=product.id,
                warehouse_id=data["warehouse_id"],
                quantity=data.get("initial_quantity", 0)
            )
            db.session.add(inventory)

        db.session.commit()
        return jsonify({"message": "Product created", "product_id": product.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/api/companies/<int:company_id>/alerts/low-stock", methods=["GET"])
def get_low_stock_alerts(company_id):
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    results = (
        db.session.query(
            Product.id,
            Product.name,
            Product.sku,
            Product.low_stock_threshold,
            Inventory.quantity,
            Inventory.warehouse_id,
            Warehouse.name.label("warehouse_name"),
        )
        .join(Inventory, Inventory.product_id == Product.id)
        .join(Warehouse, Warehouse.id == Inventory.warehouse_id)
        .filter(Product.company_id == company_id)
        .filter(Inventory.quantity < Product.low_stock_threshold)
        .all()
    )

    alerts = []
    for row in results:
        sales = db.session.query(func.sum(Sale.quantity)).filter(
            Sale.product_id == row.id,
            Sale.warehouse_id == row.warehouse_id,
            Sale.created_at >= thirty_days_ago
        ).scalar()

        if not sales:
            continue

        avg_daily = sales / 30
        days_left = int(row.quantity / avg_daily) if avg_daily else None

        supplier = db.session.query(Supplier).join(
            ProductSupplier, ProductSupplier.supplier_id == Supplier.id
        ).filter(ProductSupplier.product_id == row.id).first()

        alerts.append({
            "product_id": row.id,
            "product_name": row.name,
            "sku": row.sku,
            "warehouse_id": row.warehouse_id,
            "warehouse_name": row.warehouse_name,
            "current_stock": row.quantity,
            "threshold": row.low_stock_threshold,
            "days_until_stockout": days_left,
            "supplier": {
                "id": supplier.id,
                "name": supplier.name,
                "contact_email": supplier.contact_email
            } if supplier else None
        })

    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
