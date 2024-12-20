import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from data.models import Product, Batch, SaleRecord, Supplier, Order, OrderItem
from data.db_config import engine
import tkinter as tk
from tkinter import filedialog

# Create a new session
SessionLocal = sessionmaker(bind=engine)

def restore_data_from_json(filename='backupbyUser.json'):
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    filename = filedialog.askopenfilename(
        title="Select backup JSON file",
        filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
    )

    if not filename:
        return "No file selected."
    try:
        with open(filename, 'r') as f:
            data_dict = json.load(f)
        
        session = SessionLocal()
        
        # Start a transaction
        with session.begin():
            # Delete records in the correct order to avoid foreign key violations
            session.query(OrderItem).delete()
            session.query(Order).delete()
            session.query(SaleRecord).delete()
            session.query(Batch).delete()
            session.query(Supplier).delete()
            session.query(Product).delete()
            
            # Insert data in the correct order (parent tables first)
            for product_data in data_dict.get('products', []):
                product = Product(**product_data)
                session.add(product)
            
            for supplier_data in data_dict.get('suppliers', []):
                supplier = Supplier(**supplier_data)
                session.add(supplier)
            
            for order_data in data_dict.get('orders', []):
                order = Order(**order_data)
                session.add(order)
            
            for batch_data in data_dict.get('batches', []):
                batch = Batch(**batch_data)
                session.add(batch)
            
            for sale_record_data in data_dict.get('sale_records', []):
                sale_record = SaleRecord(**sale_record_data)
                session.add(sale_record)
            
            for order_item_data in data_dict.get('order_items', []):
                order_item = OrderItem(**order_item_data)
                session.add(order_item)
        
        # Commit the transaction
        session.commit()

        # Reset sequences for PostgreSQL
        if session.bind.dialect.name == 'postgresql':
            sequences = [
                {'table': 'products', 'pk': 'product_id'},
                {'table': 'batches', 'pk': 'batch_id'},
                {'table': 'sale_records', 'pk': 'sale_id'},
                {'table': 'suppliers', 'pk': 'supplier_id'},
                {'table': 'orders', 'pk': 'order_id'},
                {'table': 'order_items', 'pk': 'order_item_id'},
            ]
            for seq in sequences:
                sql = text(f"""
                    SELECT setval(
                        pg_get_serial_sequence('{seq['table']}', '{seq['pk']}'),
                        COALESCE(MAX("{seq['pk']}"), 1),
                        COALESCE(MAX("{seq['pk']}"), 1) IS NOT NULL
                    ) FROM {seq['table']};
                """)
                session.execute(sql)
            session.commit()
        
        session.close()
        return "Data has been restored successfully."
    except Exception as e:
        return f"An error occurred during restore: {e}"

if __name__ == "__main__":
    result = restore_data_from_json()
    print(result)