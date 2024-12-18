# domain/domain_models.py

from dataclasses import dataclass
from typing import Optional, List, Dict
from datetime import date
from enum import Enum

@dataclass
class Product:
    product_id: Optional[int]
    sku: str
    name: str
    category: str
    description: Optional[str]
    unit_price: float
    reorder_level: int
    total_quantity: int = 0  # Added for inventory status

@dataclass
class Batch:
    batch_id: Optional[int]
    product_id: int
    quantity: int
    manufacture_date: date
    expiry_date: date
    product: Optional[Product] = None

@dataclass
class SaleRecord:
    sale_id: Optional[int]
    product_id: int
    quantity_sold: int
    sale_date: date
    unit_price_at_sale: float
    product: Optional[Product] = None

@dataclass
class SalesReport:
    start_date: date
    end_date: date
    total_sales: float
    sales_by_product: Dict[str, float]

@dataclass
class Supplier:
    supplier_id: Optional[int]
    name: str
    contact_person: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]

@dataclass
class OrderItem:
    order_item_id: Optional[int]
    order_id: int
    product_id: int
    quantity: int
    cost_per_unit: float
    product: Optional[Product] = None

class OrderStatus(Enum):
    Pending = "Pending"
    Shipped = "Shipped"
    Delivered = "Delivered"

@dataclass
class Order:
    order_id: Optional[int]
    supplier_id: int
    order_date: date
    expected_delivery_date: date
    items: List[OrderItem]
    total_cost: float
    status: OrderStatus
    supplier: Optional[Supplier] = None
