# services/inventory_service.py

from typing import List, Optional
from datetime import date
from domain.domain_models import (
    Product,
    Batch,
    SaleRecord,
    Supplier,
    Order,
    OrderItem,
    SalesReport
)
from data.repositories import (
    ProductRepository,
    BatchRepository,
    SaleRecordRepository,
    SupplierRepository,
    OrderRepository
)

class InventoryService:
    def __init__(
        self,
        product_repo: ProductRepository,
        batch_repo: BatchRepository,
        sale_repo: SaleRecordRepository,
        supplier_repo: SupplierRepository,
        order_repo: OrderRepository
    ):
        self.product_repo = product_repo
        self.batch_repo = batch_repo
        self.sale_repo = sale_repo
        self.supplier_repo = supplier_repo
        self.order_repo = order_repo

    # Product Management
    def get_all_products(self) -> List[Product]:
        return self.product_repo.get_all_products()

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self.product_repo.get_product_by_id(product_id)

    def add_product(self, product: Product) -> Product:
        return self.product_repo.add_product(product)

    def update_product(self, product: Product) -> None:
        self.product_repo.update_product(product)

    def delete_product(self, product_id: int) -> None:
        self.product_repo.delete_product(product_id)

    # Batch Management
    def get_all_batches(self) -> List[Batch]:
        return self.batch_repo.get_all_batches()

    def get_batch_by_id(self, batch_id: int) -> Optional[Batch]:
        return self.batch_repo.get_batch_by_id(batch_id)

    def add_batch(self, batch: Batch) -> Batch:
        return self.batch_repo.add_batch(batch)

    def update_batch(self, batch: Batch) -> None:
        self.batch_repo.update_batch(batch)

    def delete_batch(self, batch_id: int) -> None:
        self.batch_repo.delete_batch(batch_id)

    # Supplier Management
    def get_all_suppliers(self) -> List[Supplier]:
        return self.supplier_repo.get_all_suppliers()

    def get_supplier_by_id(self, supplier_id: int) -> Optional[Supplier]:
        return self.supplier_repo.get_supplier_by_id(supplier_id)

    def add_supplier(self, supplier: Supplier) -> Supplier:
        return self.supplier_repo.add_supplier(supplier)

    def update_supplier(self, supplier: Supplier) -> None:
        self.supplier_repo.update_supplier(supplier)

    def delete_supplier(self, supplier_id: int) -> None:
        self.supplier_repo.delete_supplier(supplier_id)

    # Order Management
    def get_all_orders(self) -> List[Order]:
        return self.order_repo.get_all_orders()

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        return self.order_repo.get_order_by_id(order_id)

    def add_order(self, order: Order) -> Order:
        return self.order_repo.add_order(order)

    def update_order(self, order: Order) -> None:
        self.order_repo.update_order(order)

    def delete_order(self, order_id: int) -> None:
        self.order_repo.delete_order(order_id)

    # Sales Management
    def get_all_sales(self) -> List[SaleRecord]:
        return self.sale_repo.get_all_sales()

    def get_sale_by_id(self, sale_id: int) -> Optional[SaleRecord]:
        return self.sale_repo.get_sale_by_id(sale_id)

    def record_sale(self, sale: SaleRecord) -> SaleRecord:
        # Use the batch_repo method to reduce quantity directly:
        self.batch_repo.reduce_quantity(sale.product_id, sale.quantity_sold)

        # Convert SaleRecord to dict for the repository:
        sale_dict = {
            "product_id": sale.product_id,
            "quantity_sold": sale.quantity_sold,
            "sale_date": sale.sale_date,
            "unit_price_at_sale": sale.unit_price_at_sale
        }
        return self.sale_repo.record_sale(sale_dict)

    
    def get_available_quantity(self, product_id: int) -> int:
        return self.batch_repo.get_available_quantity(product_id)

    # Reporting
    def get_sales_report(self, start_date: date, end_date: date) -> SalesReport:
        sales = self.sale_repo.get_sales_between_dates(start_date, end_date)
        total_sales = sum(sale.quantity_sold * sale.unit_price_at_sale for sale in sales)
        sales_by_product = {}
        for sale in sales:
            product_name = sale.product.name if sale.product else "Unknown"
            sales_by_product[product_name] = sales_by_product.get(product_name, 0) + sale.quantity_sold * sale.unit_price_at_sale
        return SalesReport(
            start_date=start_date,
            end_date=end_date,
            total_sales=total_sales,
            sales_by_product=sales_by_product
        )

    def get_inventory_status(self) -> List[Product]:
        products = self.product_repo.get_all_products()
        for product in products:
            total_quantity = self.batch_repo.get_available_quantity(product.product_id)
            product.total_quantity = total_quantity
        return products

    # Database Configuration
    def get_db_url(self) -> str:
        return self.batch_repo.session.bind.url.render_as_string(hide_password=True)

    def update_db_url(self, new_db_url: str) -> None:
        # Implement logic to update the database URL and reinitialize connections if necessary
        # This is a placeholder implementation
        raise NotImplementedError("Dynamic DB URL update not supported.")
