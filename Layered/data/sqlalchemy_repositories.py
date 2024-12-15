# data/sqlalchemy_repositories.py

from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from domain.domain_models import OrderItem, Product, Batch, SaleRecord, Order, SalesReport
from data.repositories import ProductRepository, BatchRepository, SaleRecordRepository, OrderRepository
from data.models import ProductModel, BatchModel, SaleRecordModel, OrderModel, OrderItemModel, SalesReportModel


class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all_products(self) -> List[Product]:
        product_models = self.session.query(ProductModel).all()
        return [self._map_to_domain(p) for p in product_models]

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        product_model = self.session.query(ProductModel).filter_by(product_id=product_id).first()
        return self._map_to_domain(product_model) if product_model else None

    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        product_model = self.session.query(ProductModel).filter_by(sku=sku).first()
        return self._map_to_domain(product_model) if product_model else None

    def add_product(self, product: Product) -> Product:
        product_model = self._map_to_model(product)
        self.session.add(product_model)
        self.session.commit()
        return self._map_to_domain(product_model)

    def update_product(self, product: Product) -> None:
        product_model = self.session.query(ProductModel).filter_by(product_id=product.product_id).first()
        if product_model:
            product_model.sku = product.sku
            product_model.name = product.name
            product_model.category = product.category
            product_model.description = product.description
            product_model.unit_price = product.unit_price
            product_model.reorder_level = product.reorder_level
            self.session.commit()

    def delete_product(self, product_id: int) -> None:
        product_model = self.session.query(ProductModel).filter_by(product_id=product_id).first()
        if product_model:
            self.session.delete(product_model)
            self.session.commit()

    def _map_to_domain(self, model: ProductModel) -> Product:
        return Product(
            product_id=model.product_id,
            sku=model.sku,
            name=model.name,
            category=model.category,
            description=model.description,
            unit_price=model.unit_price,
            reorder_level=model.reorder_level
        )

    def _map_to_model(self, product: Product) -> ProductModel:
        return ProductModel(
            sku=product.sku,
            name=product.name,
            category=product.category,
            description=product.description,
            unit_price=product.unit_price,
            reorder_level=product.reorder_level
        )


class SQLAlchemyBatchRepository(BatchRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all_batches(self) -> List[Batch]:
        batch_models = self.session.query(BatchModel).all()
        return [self._map_to_domain(b) for b in batch_models]

    def get_batch_by_id(self, batch_id: int) -> Optional[Batch]:
        batch_model = self.session.query(BatchModel).filter_by(batch_id=batch_id).first()
        return self._map_to_domain(batch_model) if batch_model else None

    def add_batch(self, batch: Batch) -> Batch:
        batch_model = self._map_to_model(batch)
        self.session.add(batch_model)
        self.session.commit()
        return self._map_to_domain(batch_model)

    def update_batch(self, batch: Batch) -> None:
        batch_model = self.session.query(BatchModel).filter_by(batch_id=batch.batch_id).first()
        if batch_model:
            batch_model.product_id = batch.product_id
            batch_model.quantity = batch.quantity
            batch_model.manufacture_date = batch.manufacture_date
            batch_model.expiry_date = batch.expiry_date
            self.session.commit()

    def delete_batch(self, batch_id: int) -> None:
        batch_model = self.session.query(BatchModel).filter_by(batch_id=batch_id).first()
        if batch_model:
            self.session.delete(batch_model)
            self.session.commit()

    def _map_to_domain(self, model: BatchModel) -> Batch:
        return Batch(
            batch_id=model.batch_id,
            product_id=model.product_id,
            quantity=model.quantity,
            manufacture_date=model.manufacture_date,
            expiry_date=model.expiry_date
        )

    def _map_to_model(self, batch: Batch) -> BatchModel:
        return BatchModel(
            product_id=batch.product_id,
            quantity=batch.quantity,
            manufacture_date=batch.manufacture_date,
            expiry_date=batch.expiry_date
        )


class SQLAlchemySaleRecordRepository(SaleRecordRepository):
    def __init__(self, session: Session):
        self.session = session

    def record_sale(self, sale_record: SaleRecord) -> SaleRecord:
        sale_model = self._map_to_model(sale_record)
        self.session.add(sale_model)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        return self._map_to_domain(sale_model)

    def get_sales_between_dates(self, start_date: date, end_date: date) -> List[SaleRecord]:
        sale_models = self.session.query(SaleRecordModel).filter(
            SaleRecordModel.sale_date >= start_date,
            SaleRecordModel.sale_date <= end_date
        ).all()
        return [self._map_to_domain(s) for s in sale_models]

    def _map_to_domain(self, model: SaleRecordModel) -> SaleRecord:
        return SaleRecord(
            sale_id=model.sale_id,
            product_id=model.product_id,
            quantity_sold=model.quantity_sold,
            sale_date=model.sale_date,
            unit_price_at_sale=model.unit_price_at_sale
        )

    def _map_to_model(self, sale: SaleRecord) -> SaleRecordModel:
        return SaleRecordModel(
            product_id=sale.product_id,
            quantity_sold=sale.quantity_sold,
            sale_date=sale.sale_date,
            unit_price_at_sale=sale.unit_price_at_sale,
            report_id=None  # Explicitly setting to None; adjust as needed
        )


class SQLAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def add_order(self, order: Order) -> Order:
        order_model = self._map_to_model(order)
        self.session.add(order_model)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        return self._map_to_domain(order_model)

    def get_orders(self) -> List[Order]:
        order_models = self.session.query(OrderModel).all()
        return [self._map_to_domain(o) for o in order_models]

    def _map_to_domain(self, model: OrderModel) -> Order:
        return Order(
            order_id=model.order_id,
            supplier_id=model.supplier_id,
            order_date=model.order_date,
            expected_delivery_date=model.expected_delivery_date,
            items=[
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    cost_per_unit=item.cost_per_unit
                ) for item in model.items
            ]
        )

    def _map_to_model(self, order: Order) -> OrderModel:
        order_model = OrderModel(
            supplier_id=order.supplier_id,
            order_date=order.order_date,
            expected_delivery_date=order.expected_delivery_date,
            items=[
                OrderItemModel(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    cost_per_unit=item.cost_per_unit
                ) for item in order.items
            ]
        )
        return order_model
