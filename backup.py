from data.db_config import SessionLocal
from data.models import Product, Batch, SaleRecord, Supplier, Order, OrderItem
import json

def fetch_data():
    session = SessionLocal()
    data = {
        "products": session.query(Product).all(),
        "batches": session.query(Batch).all(),
        "sale_records": session.query(SaleRecord).all(),
        "suppliers": session.query(Supplier).all(),
        "orders": session.query(Order).all(),
        "order_items": session.query(OrderItem).all(),
    }
    session.close()
    return data

def to_dict(obj):
    if isinstance(obj, list):
        return [to_dict(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        data = {}
        for key, value in obj.__dict__.items():
            if not key.startswith('_'):
                data[key] = to_dict(value)
        return data
    else:
        return obj

def convert_data_to_dict(data):
    return {key: to_dict(value) for key, value in data.items()}

def save_to_json(data, filename='backup.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, default=str, indent=4)

if __name__ == "__main__":
    data = fetch_data()
    data_dict = convert_data_to_dict(data)
    save_to_json(data_dict)
    print("Data has been backed up to backup.json")