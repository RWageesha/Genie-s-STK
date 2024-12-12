import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.inventory import Inventory  # Now this should work
from src.inventory import Inventory
from src.product import Product

def main():
    # Create an inventory object
    inventory = Inventory()

    # Create some sample products
    product1 = Product("P001", "Laptop", 1200, 10, "Electronics")
    product2 = Product("P002", "Phone", 800, 5, "Electronics")

    # Add products to inventory
    inventory.add_product(product1)
    inventory.add_product(product2)

    # List products after adding
    print("Inventory after adding products:")
    for product in inventory.list_products():
        print(product)

    # Remove a product by ID
    inventory.remove_product("P002")

    # List products after removal
    print("\nInventory after removing product P002:")
    for product in inventory.list_products():
        print(product)

if __name__ == "__main__":
    main()
