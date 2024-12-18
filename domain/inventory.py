# domain/inventory.py

from typing import List
from domain.domain_models import Product, Batch, Supplier, Order, SaleRecord

class Inventory:
    def __init__(self):
        self.products: List[Product] = []
        self.batches: List[Batch] = []
        self.suppliers: List[Supplier] = []
        self.orders: List[Order] = []
        self.sales: List[SaleRecord] = []

    def add_product(self, product: Product):
        self.products.append(product)

    def add_batch(self, batch: Batch):
        self.batches.append(batch)

    def add_supplier(self, supplier: Supplier):
        self.suppliers.append(supplier)

    def add_order(self, order: Order):
        self.orders.append(order)

    def record_sale(self, sale: SaleRecord):
        self.sales.append(sale)
