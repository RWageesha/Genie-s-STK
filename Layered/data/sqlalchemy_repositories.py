# data/sqlalchemy_repositories.py

from data.repositories import (
    ProductRepository,
    BatchRepository,
    SaleRecordRepository,
    SupplierRepository,
    OrderRepository
)
from data.models import (
    Product as ORMProduct,
    Batch as ORMBatch,
    SaleRecord as ORMSaleRecord,
    Supplier as ORMSupplier,
    Order as ORMOrder,
    OrderItem as ORMOrderItem,
    OrderStatus
)
from data.db_config import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from domain.domain_models import (
    Product as DomainProduct,
    Batch as DomainBatch,
    SaleRecord as DomainSaleRecord,
    Supplier as DomainSupplier,
    Order as DomainOrder,
    OrderItem as DomainOrderItem
)
from datetime import date

# Ensure all repository classes are defined below

class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self):
        self.session: Session = SessionLocal()

    def get_all_products(self) -> List[DomainProduct]:
        orm_products = self.session.query(ORMProduct).all()
        domain_products = [self.to_domain_model(p) for p in orm_products]
        return domain_products

    def get_product_by_id(self, product_id: int) -> Optional[DomainProduct]:
        orm_product = self.session.query(ORMProduct).filter(ORMProduct.product_id == product_id).first()
        return self.to_domain_model(orm_product) if orm_product else None

    def get_product_by_sku(self, sku: str) -> Optional[DomainProduct]:
        orm_product = self.session.query(ORMProduct).filter(ORMProduct.sku == sku).first()
        return self.to_domain_model(orm_product) if orm_product else None

    def add_product(self, product: DomainProduct) -> DomainProduct:
        # Convert DomainProduct to ORMProduct
        orm_product = ORMProduct(
            sku=product.sku,
            name=product.name,
            category=product.category,
            description=product.description,
            unit_price=product.unit_price,
            reorder_level=product.reorder_level
        )
        self.session.add(orm_product)
        self.session.commit()
        self.session.refresh(orm_product)
        product.product_id = orm_product.product_id
        return product

    def update_product(self, product: DomainProduct) -> None:
        orm_product = self.session.query(ORMProduct).filter(ORMProduct.product_id == product.product_id).first()
        if orm_product:
            orm_product.sku = product.sku
            orm_product.name = product.name
            orm_product.category = product.category
            orm_product.description = product.description
            orm_product.unit_price = product.unit_price
            orm_product.reorder_level = product.reorder_level
            self.session.commit()

    def delete_product(self, product_id: int) -> None:
        orm_product = self.session.query(ORMProduct).filter(ORMProduct.product_id == product_id).first()
        if orm_product:
            self.session.delete(orm_product)
            self.session.commit()

    def to_domain_model(self, orm_product: ORMProduct) -> DomainProduct:
        if not orm_product:
            return None
        return DomainProduct(
            product_id=orm_product.product_id,
            sku=orm_product.sku,
            name=orm_product.name,
            category=orm_product.category,
            description=orm_product.description,
            unit_price=orm_product.unit_price,
            reorder_level=orm_product.reorder_level,
            total_quantity=0  # This can be set separately if needed
        )


class SQLAlchemyBatchRepository(BatchRepository):
    def __init__(self):
        self.session: Session = SessionLocal()

    def get_all_batches(self) -> List[DomainBatch]:
        orm_batches = self.session.query(ORMBatch).all()
        domain_batches = [self.to_domain_model(b) for b in orm_batches]
        return domain_batches

    def get_batch_by_id(self, batch_id: int) -> Optional[DomainBatch]:
        orm_batch = self.session.query(ORMBatch).filter(ORMBatch.batch_id == batch_id).first()
        return self.to_domain_model(orm_batch) if orm_batch else None

    def add_batch(self, batch: DomainBatch) -> DomainBatch:
        orm_batch = ORMBatch(
            product_id=batch.product_id,
            quantity=batch.quantity,
            manufacture_date=batch.manufacture_date,
            expiry_date=batch.expiry_date
        )
        self.session.add(orm_batch)
        self.session.commit()
        self.session.refresh(orm_batch)
        batch.batch_id = orm_batch.batch_id
        return batch

    def update_batch(self, batch: DomainBatch) -> None:
        orm_batch = self.session.query(ORMBatch).filter(ORMBatch.batch_id == batch.batch_id).first()
        if orm_batch:
            orm_batch.product_id = batch.product_id
            orm_batch.quantity = batch.quantity
            orm_batch.manufacture_date = batch.manufacture_date
            orm_batch.expiry_date = batch.expiry_date
            self.session.commit()

    def delete_batch(self, batch_id: int) -> None:
        orm_batch = self.session.query(ORMBatch).filter(ORMBatch.batch_id == batch_id).first()
        if orm_batch:
            self.session.delete(orm_batch)
            self.session.commit()

    def get_available_quantity(self, product_id: int) -> int:
        total = self.session.query(func.sum(ORMBatch.quantity)).filter(ORMBatch.product_id == product_id).scalar()
        return total if total else 0

    def to_domain_model(self, orm_batch: ORMBatch) -> DomainBatch:
        if not orm_batch:
            return None
        return DomainBatch(
            batch_id=orm_batch.batch_id,
            product_id=orm_batch.product_id,
            quantity=orm_batch.quantity,
            manufacture_date=orm_batch.manufacture_date,
            expiry_date=orm_batch.expiry_date
        )


class SQLAlchemySaleRecordRepository(SaleRecordRepository):
    def __init__(self):
        self.session: Session = SessionLocal()

    def get_all_sales(self) -> List[DomainSaleRecord]:
        orm_sales = self.session.query(ORMSaleRecord).all()
        domain_sales = [self.to_domain_model(s) for s in orm_sales]
        return domain_sales

    def get_sale_by_id(self, sale_id: int) -> Optional[DomainSaleRecord]:
        orm_sale = self.session.query(ORMSaleRecord).filter(ORMSaleRecord.sale_id == sale_id).first()
        return self.to_domain_model(orm_sale) if orm_sale else None

    def record_sale(self, sale_record: DomainSaleRecord) -> DomainSaleRecord:
        orm_sale = ORMSaleRecord(
            product_id=sale_record.product_id,
            quantity_sold=sale_record.quantity_sold,
            sale_date=sale_record.sale_date,
            unit_price_at_sale=sale_record.unit_price_at_sale
        )
        self.session.add(orm_sale)
        self.session.commit()
        self.session.refresh(orm_sale)
        sale_record.sale_id = orm_sale.sale_id
        return sale_record

    def get_sales_between_dates(self, start_date: date, end_date: date) -> List[DomainSaleRecord]:
        orm_sales = self.session.query(ORMSaleRecord).filter(ORMSaleRecord.sale_date.between(start_date, end_date)).all()
        domain_sales = [self.to_domain_model(s) for s in orm_sales]
        return domain_sales

    def to_domain_model(self, orm_sale: ORMSaleRecord) -> DomainSaleRecord:
        if not orm_sale:
            return None
        return DomainSaleRecord(
            sale_id=orm_sale.sale_id,
            product_id=orm_sale.product_id,
            quantity_sold=orm_sale.quantity_sold,
            sale_date=orm_sale.sale_date,
            unit_price_at_sale=orm_sale.unit_price_at_sale
        )


class SQLAlchemySupplierRepository(SupplierRepository):
    def __init__(self):
        self.session: Session = SessionLocal()

    def get_all_suppliers(self) -> List[DomainSupplier]:
        orm_suppliers = self.session.query(ORMSupplier).all()
        domain_suppliers = [self.to_domain_model(s) for s in orm_suppliers]
        return domain_suppliers

    def get_supplier_by_id(self, supplier_id: int) -> Optional[DomainSupplier]:
        orm_supplier = self.session.query(ORMSupplier).filter(ORMSupplier.supplier_id == supplier_id).first()
        return self.to_domain_model(orm_supplier) if orm_supplier else None

    def get_supplier_by_name(self, name: str) -> Optional[DomainSupplier]:
        orm_supplier = self.session.query(ORMSupplier).filter(ORMSupplier.name == name).first()
        return self.to_domain_model(orm_supplier) if orm_supplier else None

    def add_supplier(self, supplier: DomainSupplier) -> DomainSupplier:
        orm_supplier = ORMSupplier(
            name=supplier.name,
            contact_person=supplier.contact_person,
            phone=supplier.phone,
            email=supplier.email,
            address=supplier.address
        )
        self.session.add(orm_supplier)
        self.session.commit()
        self.session.refresh(orm_supplier)
        supplier.supplier_id = orm_supplier.supplier_id
        return supplier

    def update_supplier(self, supplier: DomainSupplier) -> None:
        orm_supplier = self.session.query(ORMSupplier).filter(ORMSupplier.supplier_id == supplier.supplier_id).first()
        if orm_supplier:
            orm_supplier.name = supplier.name
            orm_supplier.contact_person = supplier.contact_person
            orm_supplier.phone = supplier.phone
            orm_supplier.email = supplier.email
            orm_supplier.address = supplier.address
            self.session.commit()

    def delete_supplier(self, supplier_id: int) -> None:
        orm_supplier = self.session.query(ORMSupplier).filter(ORMSupplier.supplier_id == supplier_id).first()
        if orm_supplier:
            self.session.delete(orm_supplier)
            self.session.commit()

    def to_domain_model(self, orm_supplier: ORMSupplier) -> DomainSupplier:
        if not orm_supplier:
            return None
        return DomainSupplier(
            supplier_id=orm_supplier.supplier_id,
            name=orm_supplier.name,
            contact_person=orm_supplier.contact_person,
            phone=orm_supplier.phone,
            email=orm_supplier.email,
            address=orm_supplier.address
        )


class SQLAlchemyOrderRepository(OrderRepository):
    def __init__(self):
        self.session: Session = SessionLocal()

    def get_all_orders(self) -> List[DomainOrder]:
        orm_orders = self.session.query(ORMOrder).all()
        domain_orders = [self.to_domain_model(o) for o in orm_orders]
        return domain_orders

    def get_order_by_id(self, order_id: int) -> Optional[DomainOrder]:
        orm_order = self.session.query(ORMOrder).filter(ORMOrder.order_id == order_id).first()
        return self.to_domain_model(orm_order) if orm_order else None

    def add_order(self, order: DomainOrder) -> DomainOrder:
        orm_order = ORMOrder(
            supplier_id=order.supplier_id,
            order_date=order.order_date,
            expected_delivery_date=order.expected_delivery_date,
            total_cost=order.total_cost,
            status=OrderStatus(order.status.value)
        )
        self.session.add(orm_order)
        self.session.commit()
        self.session.refresh(orm_order)
        
        # Add order items
        for item in order.items:
            orm_item = ORMOrderItem(
                order_id=orm_order.order_id,
                product_id=item.product_id,
                quantity=item.quantity,
                cost_per_unit=item.cost_per_unit
            )
            self.session.add(orm_item)
        self.session.commit()
        
        order.order_id = orm_order.order_id
        return order

    def update_order(self, order: DomainOrder) -> None:
        orm_order = self.session.query(ORMOrder).filter(ORMOrder.order_id == order.order_id).first()
        if orm_order:
            orm_order.supplier_id = order.supplier_id
            orm_order.order_date = order.order_date
            orm_order.expected_delivery_date = order.expected_delivery_date
            orm_order.total_cost = order.total_cost
            orm_order.status = OrderStatus(order.status.value)
            
            # Handle order items
            # For simplicity, delete existing items and add new ones
            orm_order.items = []
            for item in order.items:
                orm_item = ORMOrderItem(
                    order_id=orm_order.order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    cost_per_unit=item.cost_per_unit
                )
                self.session.add(orm_item)
            self.session.commit()

    def delete_order(self, order_id: int) -> None:
        orm_order = self.session.query(ORMOrder).filter(ORMOrder.order_id == order_id).first()
        if orm_order:
            self.session.delete(orm_order)
            self.session.commit()

    def to_domain_model(self, orm_order: ORMOrder) -> DomainOrder:
        if not orm_order:
            return None
        return DomainOrder(
            order_id=orm_order.order_id,
            supplier_id=orm_order.supplier_id,
            order_date=orm_order.order_date,
            expected_delivery_date=orm_order.expected_delivery_date,
            items=[
                DomainOrderItem(
                    order_item_id=item.order_item_id,
                    order_id=item.order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    cost_per_unit=item.cost_per_unit
                ) for item in orm_order.items
            ],
            total_cost=orm_order.total_cost,
            status=orm_order.status.value  # Assuming OrderStatus is Enum
        )
