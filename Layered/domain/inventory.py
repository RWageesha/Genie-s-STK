# domain/inventory.py

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date

from .domain_models import Product, Batch


@dataclass
class Inventory:
    products: List[Product] = field(default_factory=list)
    batches: List[Batch] = field(default_factory=list)

    def add_product(self, product: Product):
        self.products.append(product)

    def add_batch(self, batch: Batch):
        self.batches.append(batch)
        self.batches.sort(key=lambda b: b.expiry_date)

    def search_product(self, name: str) -> Optional[Product]:
        return next((product for product in self.products if product.name.lower() == name.lower()), None)

    def search_product_by_sku(self, sku: str) -> Optional[Product]:
        return next((product for product in self.products if product.sku.lower() == sku.lower()), None)

    def get_stock_level(self, product_id: int) -> int:
        return sum(batch.quantity for batch in self.batches if batch.product_id == product_id)

    def delete_product(self, product_id: int):
        self.products = [p for p in self.products if p.product_id != product_id]
        self.batches = [b for b in self.batches if b.product_id != product_id]

    def filter_batches_by_expiry(self, before_date: date) -> List[Batch]:
        return [b for b in self.batches if b.expiry_date <= before_date]

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
