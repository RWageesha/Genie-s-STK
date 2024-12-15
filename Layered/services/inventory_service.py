
from contextlib import contextmanager
from typing import List, Optional ,Dict
from datetime import date
from collections import defaultdict


from sqlalchemy.orm import Session

from domain.domain_models import Product, Batch, SaleRecord, SalesReport
from domain.inventory import Inventory
from data.repositories import ProductRepository, BatchRepository, SaleRecordRepository

class InventoryService:
    def __init__(self, 
                 product_repo: ProductRepository, 
                 batch_repo: BatchRepository, 
                 sale_repo: SaleRecordRepository):
        self.product_repo = product_repo
        self.batch_repo = batch_repo
        self.sale_repo = sale_repo

        # Initialize Inventory from database data
        products = self.product_repo.get_all_products()
        batches = self.batch_repo.get_all_batches()
        self.inventory = Inventory(products=products, batches=batches)

    # Product Operations
    def add_product(self, product: Product) -> Product:
        # Make sure SKU is unique (the repository or database unique constraint will also enforce this)
        existing = self.product_repo.get_product_by_sku(product.sku)
        if existing:
            raise ValueError(f"Product with SKU '{product.sku}' already exists.")

        saved_product = self.product_repo.add_product(product)
        self.inventory.add_product(saved_product)
        return saved_product

    def update_product(self, product_id: int, **kwargs) -> Optional[Product]:
        product = self.product_repo.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} does not exist.")

        if 'sku' in kwargs:
            # Check if new SKU conflicts with another product
            new_sku = kwargs['sku']
            other_product = self.product_repo.get_product_by_sku(new_sku)
            if other_product and other_product.product_id != product_id:
                raise ValueError(f"Another product with SKU '{new_sku}' already exists.")

        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
            else:
                raise AttributeError(f"Product has no attribute '{key}'.")

        self.product_repo.update_product(product)
        # Update in-memory inventory
        inventory_product = next((p for p in self.inventory.products if p.product_id == product_id), None)
        if inventory_product:
            for key, value in kwargs.items():
                setattr(inventory_product, key, value)
        return product

    def delete_product(self, product_id: int) -> None:
        self.product_repo.delete_product(product_id)
        self.inventory.delete_product(product_id)

    def search_product_by_sku(self, sku: str) -> Optional[Product]:
        # Quick lookup in memory
        found_product = self.inventory.search_product_by_sku(sku)
        if found_product:
            return found_product
        # If not found in memory (unlikely if inventory is always synced), try repository
        return self.product_repo.get_product_by_sku(sku)

    # Batch Operations--------------------------------------------
    def add_batch(self, batch: Batch) -> Batch:
        # Ensure the product exists
        product = self.product_repo.get_product_by_id(batch.product_id)
        if not product:
            raise ValueError(f"Product with ID {batch.product_id} does not exist.")

        saved_batch = self.batch_repo.add_batch(batch)
        self.inventory.add_batch(saved_batch)
        return saved_batch

    def update_batch(self, batch_id: int, **kwargs) -> Optional[Batch]:
        batch = self.batch_repo.get_batch_by_id(batch_id)
        if not batch:
            raise ValueError(f"Batch with ID {batch_id} does not exist.")

        for key, value in kwargs.items():
            if hasattr(batch, key):
                setattr(batch, key, value)
            else:
                raise AttributeError(f"Batch has no attribute '{key}'.")

        self.batch_repo.update_batch(batch)
        # Update in-memory inventory
        inventory_batch = next((b for b in self.inventory.batches if b.batch_id == batch_id), None)
        if inventory_batch:
            for key, value in kwargs.items():
                setattr(inventory_batch, key, value)
        return batch

    def delete_batch(self, batch_id: int) -> None:
        self.batch_repo.delete_batch(batch_id)
        self.inventory.delete_batch(batch_id)

    # Stock Level Tracking
    def get_stock_level(self, product_id: int) -> int:
        return self.inventory.get_stock_level(product_id)

    # Searching and Filtering
    def search_products(self, keyword: str) -> List[Product]:
        return self.inventory.search_products(keyword)

    def filter_batches_by_expiry(self, before_date: date) -> List[Batch]:
        return self.inventory.filter_batches_by_expiry(before_date)

    # Selling Products 
    def sell_product(self, product_id: int, quantity: int) -> SaleRecord:
        if quantity <= 0:
            raise ValueError("Quantity to sell must be positive.")

        product = self.product_repo.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} does not exist.")

        # Check if enough stock is available
        current_stock = self.get_stock_level(product_id)
        if current_stock < quantity:
            raise ValueError(f"Insufficient stock for product ID {product_id}. Available: {current_stock}, Requested: {quantity}")

        # Reduce stock in Inventory
        self.inventory.reduce_stock(product_id, quantity)

        # Update batches in the repository
        for batch in self.inventory.batches:
            if batch.product_id == product_id:
                self.batch_repo.update_batch(batch)

        # Record the sale
        sale_record = SaleRecord(
            sale_id=None,  # Will be set by the repository
            product_id=product_id,
            quantity_sold=quantity,
            sale_date=date.today(),
            unit_price_at_sale=product.unit_price
        )
        saved_sale = self.sale_repo.record_sale(sale_record)

        return saved_sale

    # Reorder Management
    def reorder_if_needed(self) -> List[Product]:
        low_stock_products = [p for p in self.inventory.products if self._is_below_reorder(p)]
        # Implement reordering logic here, e.g., create orders
        # For simplicity, we'll just return the list of products to reorder
        return low_stock_products

    def _is_below_reorder(self, product: Product) -> bool:
        total_quantity = self.get_stock_level(product.product_id)
        return total_quantity <= product.reorder_level
    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session: Session = self.product_repo.session
        try:
            yield
            session.commit()
        except Exception:
            session.rollback()
            raise
    
    def generate_sales_report(self, start_date: date, end_date: date) -> SalesReport:
        sales = self.sale_repo.get_sales_between_dates(start_date, end_date)
        report_data = defaultdict(float)

        for sale in sales:
            report_data[sale.product_id] += sale.quantity_sold * sale.unit_price_at_sale

        # Map product IDs to product names
        products = {p.product_id: p.name for p in self.inventory.products}

        sales_summary = {products.get(pid, "Unknown"): total for pid, total in report_data.items()}

        return SalesReport(
            start_date=start_date,
            end_date=end_date,
            total_sales=sum(sales_summary.values()),
            sales_by_product=sales_summary
        )