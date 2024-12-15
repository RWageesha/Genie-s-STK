# domain/domain_models.py

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional


@dataclass
class Product:
    product_id: Optional[int]
    sku: str
    name: str
    category: str
    description: Optional[str]
    unit_price: float
    reorder_level: int = 0

    def __post_init__(self):
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative.")
        if self.reorder_level < 0:
            raise ValueError("Reorder level cannot be negative.")
        if not self.sku:
            raise ValueError("SKU cannot be empty.")
    # Add methods as needed


@dataclass
class Batch:
    batch_id: Optional[int]
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
    sale_id: Optional[int]
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
    supplier_id: Optional[int]
    name: str
    contact_person: Optional[str]
    phone: Optional[str]
    email: Optional[str]

    def __post_init__(self):
        if not self.name:
            raise ValueError("Supplier name cannot be empty.")


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
    order_id: Optional[int]
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
class SalesReport:
    start_date: date
    end_date: date
    total_sales: float
    sales_by_product: Dict[str, float]
