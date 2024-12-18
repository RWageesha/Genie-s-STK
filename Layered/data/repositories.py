# data/repositories.py

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.domain_models import Product, Batch, SaleRecord, Supplier, Order
from datetime import date

class ProductRepository(ABC):
    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        pass

    @abstractmethod
    def add_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    def update_product(self, product: Product) -> None:
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> None:
        pass

class BatchRepository(ABC):
    @abstractmethod
    def get_all_batches(self) -> List[Batch]:
        pass

    @abstractmethod
    def get_batch_by_id(self, batch_id: int) -> Optional[Batch]:
        pass

    @abstractmethod
    def add_batch(self, batch: Batch) -> Batch:
        pass

    @abstractmethod
    def update_batch(self, batch: Batch) -> None:
        pass

    @abstractmethod
    def delete_batch(self, batch_id: int) -> None:
        pass

class SaleRecordRepository(ABC):
    @abstractmethod
    def get_all_sales(self) -> List[SaleRecord]:
        pass

    @abstractmethod
    def get_sale_by_id(self, sale_id: int) -> Optional[SaleRecord]:
        pass

    @abstractmethod
    def record_sale(self, sale_record: SaleRecord) -> SaleRecord:
        pass

    @abstractmethod
    def get_sales_between_dates(self, start_date: date, end_date: date) -> List[SaleRecord]:
        pass

class SupplierRepository(ABC):
    @abstractmethod
    def get_all_suppliers(self) -> List[Supplier]:
        pass

    @abstractmethod
    def get_supplier_by_id(self, supplier_id: int) -> Optional[Supplier]:
        pass

    @abstractmethod
    def get_supplier_by_name(self, name: str) -> Optional[Supplier]:
        pass

    @abstractmethod
    def add_supplier(self, supplier: Supplier) -> Supplier:
        pass

    @abstractmethod
    def update_supplier(self, supplier: Supplier) -> None:
        pass

    @abstractmethod
    def delete_supplier(self, supplier_id: int) -> None:
        pass

class OrderRepository(ABC):
    @abstractmethod
    def get_all_orders(self) -> List[Order]:
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def add_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    def update_order(self, order: Order) -> None:
        pass

    @abstractmethod
    def delete_order(self, order_id: int) -> None:
        pass
