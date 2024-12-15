from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class Product:
    product_id: int
    sku: str  # Stock Keeping Unit
    name: str
    category: str
    description: str
    unit_price: float
    reorder_level: int = 0  # Threshold for reordering

    def __post_init__(self):
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative.")
        if self.reorder_level < 0:
            raise ValueError("Reorder level cannot be negative.")
        
    # make a function to calc discounted prices if needed


@dataclass
class Batch:
    batch_id: str
    product_id: int
    quantity: int
    manufacture_date: date
    expiry_date: date

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        if self.expiry_date <= self.manufacture_date:
            raise ValueError("Expiry date must be after manufacture date.")

    def is_expiring_soon(self, days_threshold: int = 30) -> bool:
        """Check if the batch is nearing expiry within the given threshold."""
        return (self.expiry_date - date.today()).days <= days_threshold

    def reduce_quantity(self, amount: int):
        if amount < 0:
            raise ValueError("Reduction amount cannot be negative.")
        if amount > self.quantity:
            raise ValueError("Cannot reduce more than current quantity.")
        self.quantity -= amount


@dataclass
class SaleRecord:
    sale_id: int
    product_id: int
    quantity_sold: int
    sale_date: date
    unit_price_at_sale: float

    def __post_init__(self):
        if self.quantity_sold <= 0:
            raise ValueError("Quantity sold must be positive.")
        if self.unit_price_at_sale < 0:
            raise ValueError("Unit price at sale cannot be negative.")

    def total_sale_value(self) -> float:
        return self.quantity_sold * self.unit_price_at_sale


@dataclass
class Supplier:
    supplier_id: int
    name: str
    contact_info: str
    address: str

    def __post_init__(self):
        if not self.name:
            raise ValueError("Supplier name cannot be empty.")
        if not self.contact_info:
            raise ValueError("Contact info cannot be empty.")


@dataclass
class OrderItem:
    product_id: int
    quantity: int
    cost_per_unit: float

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Order item quantity must be positive.")
        if self.cost_per_unit < 0:
            raise ValueError("Cost per unit cannot be negative.")

    def total_cost(self) -> float:
        return self.quantity * self.cost_per_unit


@dataclass
class Order:
    order_id: int
    supplier_id: int
    order_date: date
    expected_delivery_date: date
    items: List[OrderItem] = field(default_factory=list)

    def __post_init__(self):
        if self.expected_delivery_date < self.order_date:
            raise ValueError("Expected delivery date cannot be before the order date.")
        if not self.items:
            raise ValueError("Order must contain at least one item.")

    def total_order_cost(self) -> float:
        return sum(item.total_cost() for item in self.items)

@dataclass
class Inventory:
    products: List[Product] = field(default_factory=list)
    batches: List[Batch] = field(default_factory=list)

    def add_product(self, product: Product):
        self.products.append(product)

    def add_batch(self, batch: Batch):
        self.batches.append(batch)
        self.batches.sort(key=lambda b: b.expiry_date)  # Prioritize older stocks

    def get_expiring_soon(self, days_threshold: int = 30) -> List[Batch]:
        """Return batches expiring within the given threshold."""
        return [batch for batch in self.batches if batch.is_expiring_soon(days_threshold)]

    def search_product(self, name: str) -> Optional[Product]:
        """Search for a product by name."""
        return next((product for product in self.products if product.name == name), None)

    def reduce_stock(self, product_id: int, quantity: int):
        """Reduce stock using FIFO to ensure older stocks are sold first."""
        relevant_batches = [batch for batch in self.batches if batch.product_id == product_id and batch.quantity > 0]
        relevant_batches.sort(key=lambda b: b.manufacture_date)
        for batch in relevant_batches:
            if batch.quantity >= quantity:
                batch.reduce_quantity(quantity)
                break
            else:
                quantity -= batch.quantity
                batch.reduce_quantity(batch.quantity)
