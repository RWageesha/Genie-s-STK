from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class ProductModel(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String, unique=True, nullable=False)  # Ensuring SKU is unique
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    unit_price = Column(Float, nullable=False)
    reorder_level = Column(Integer, default=0)

    batches = relationship("BatchModel", back_populates="product")


class BatchModel(Base):
    __tablename__ = 'batches'

    batch_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    manufacture_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)

    product = relationship("ProductModel", back_populates="batches")


class SaleRecordModel(Base):
    __tablename__ = 'sale_records'

    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    sale_date = Column(Date, nullable=False)
    unit_price_at_sale = Column(Float, nullable=False)

    product = relationship("ProductModel")


class OrderModel(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'), nullable=False)
    order_date = Column(Date, nullable=False)
    expected_delivery_date = Column(Date, nullable=False)

    items = relationship("OrderItemModel", back_populates="order")


class OrderItemModel(Base):
    __tablename__ = 'order_items'

    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    cost_per_unit = Column(Float, nullable=False)

    order = relationship("OrderModel", back_populates="items")
    product = relationship("ProductModel")

class SalesReportModel(Base):
    __tablename__ = 'sales_reports'

    report_id = Column(Integer, primary_key=True, autoincrement=True)
    report_date = Column(Date, nullable=False)
    total_sales = Column(Float, nullable=False)

    sales = relationship("SaleRecordModel", back_populates="report")
