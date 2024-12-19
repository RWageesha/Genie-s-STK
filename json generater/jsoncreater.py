import json
from datetime import datetime, timedelta
import random

def read_products(file_path):
    """
    Reads the product data from a file.
    Each line in the file should contain SKU and Product Name separated by a tab.
    
    :param file_path: Path to the products file.
    :return: List of tuples (sku, name).
    """
    products = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, start=1):
            parts = line.strip().split('\t')
            if len(parts) < 2:
                print(f"Skipping malformed line {line_number}: {line.strip()}")
                continue
            sku, name = parts[0], parts[1]
            products.append((sku, name))
    return products

def generate_products(products_data):
    """
    Generates the products list with required fields.
    
    :param products_data: List of tuples (sku, name).
    :return: List of product dictionaries.
    """
    products = []
    product_id = 1
    for sku, name in products_data:
        category = sku[:2]  # Assuming category is the first two characters of SKU
        unit_price = round(random.uniform(5.0, 100.0), 2)  # Random unit price between $5 and $100
        reorder_level = random.randint(10, 100)  # Random reorder level between 10 and 100
        
        product = {
            "name": name,
            "description": None,
            "reorder_level": reorder_level,
            "sku": sku,
            "product_id": product_id,
            "category": category,
            "unit_price": unit_price
        }
        products.append(product)
        product_id += 1
    return products

def generate_batches(products, start_batch_id=1):
    """
    Generates batches for each product.
    Each product gets one batch with random quantity.
    
    :param products: List of product dictionaries.
    :param start_batch_id: Starting batch ID.
    :return: List of batch dictionaries.
    """
    batches = []
    batch_id = start_batch_id
    for product in products:
        manufacture_date = datetime.now().strftime("%Y-%m-%d")
        expiry_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")  # 1 year later
        quantity = random.randint(100, 1000)  # Random quantity between 100 and 1000
        
        batch = {
            "manufacture_date": manufacture_date,
            "batch_id": batch_id,
            "quantity": quantity,
            "product_id": product["product_id"],
            "expiry_date": expiry_date
        }
        batches.append(batch)
        batch_id += 1
    return batches

def generate_inventory_json(products, batches):
    """
    Assembles the inventory JSON structure.
    
    :param products: List of product dictionaries.
    :param batches: List of batch dictionaries.
    :return: Dictionary representing the inventory JSON.
    """
    inventory = {
        "products": products,
        "batches": batches,
        "sale_records": [],  # Empty as per your request
        "suppliers": [],
        "orders": [],
        "order_items": []
    }
    return inventory

def write_json(data, output_file):
    """
    Writes the data to a JSON file.
    
    :param data: Data to write.
    :param output_file: Output JSON file path.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"JSON file '{output_file}' created successfully.")

def main():
    # Paths to input and output files
    products_file = 'c:/Users/ASUS/Desktop/Layered/json generater/products.txt' # Ensure this file exists with correct data
    output_file = 'inventory.json'
    
    # Read product data
    products_data = read_products(products_file)
    if not products_data:
        print("No valid product data found. Exiting.")
        return
    
    # Generate products list
    products = generate_products(products_data)
    
    # Generate batches list
    batches = generate_batches(products)
    
    # Assemble inventory JSON
    inventory_json = generate_inventory_json(products, batches)
    
    # Write to JSON file
    write_json(inventory_json, output_file)

if __name__ == "__main__":
    main()
