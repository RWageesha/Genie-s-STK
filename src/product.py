class Product:
    def __init__(self, product_id, name, price, quantity, category):
        self.product_id = product_id  # Unique identifier for the product
        self.name = name  # Name of the product
        self.price = price  # Price of the product
        self.quantity = quantity  # Quantity available in the inventory
        self.category = category  # Category of the product

    def __repr__(self):
        return f"({self.product_id}) {self.name} - ${self.price} - {self.quantity} pcs - Category: {self.category}"
