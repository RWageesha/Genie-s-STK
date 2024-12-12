import json
import os
from src.product import Product  # Import Product class

class Inventory:
    def __init__(self, data_file="data/inventory.json"):
        self.products = []  # List to store products
        self.data_file = data_file  # Path to the file where inventory is stored
        self.load_from_file()  # Load the inventory from file when initialized

    def add_product(self, product):
        """Add a new product to the inventory."""
        self.products.append(product)
        self.save_to_file()

    def remove_product(self, product_id):
        """Remove a product from the inventory by its product_id."""
        self.products = [product for product in self.products if product.product_id != product_id]
        self.save_to_file()

    def save_to_file(self):
        """Save the current inventory to a JSON file."""
        with open(self.data_file, "w") as file:
            # Save each product as a dictionary (by calling __dict__ on the product)
            json.dump([product.__dict__ for product in self.products], file, indent=4)

    def load_from_file(self):
        """Load the inventory from a JSON file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                data = json.load(file)
                self.products = [Product(**item) for item in data]  # Convert dict to Product instances

    def list_products(self):
        """List all products in the inventory."""
        return self.products
