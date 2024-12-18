# data/models.py

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class OrderStatus(enum.Enum):
    Pending = "Pending"
    Shipped = "Shipped"
    Delivered = "Delivered"

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String)
    unit_price = Column(Float, nullable=False)
    reorder_level = Column(Integer, nullable=False)

    batches = relationship("Batch", back_populates="product")
    sale_records = relationship("SaleRecord", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

class Batch(Base):
    __tablename__ = "batches"

    batch_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    manufacture_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)

    product = relationship("Product", back_populates="batches")

class SaleRecord(Base):
    __tablename__ = "sale_records"

    sale_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    sale_date = Column(Date, nullable=False)
    unit_price_at_sale = Column(Float, nullable=False)

    product = relationship("Product", back_populates="sale_records")

class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    contact_person = Column(String)
    phone = Column(String)
    email = Column(String)
    address = Column(String)  # Ensure this column exists

    orders = relationship("Order", back_populates="supplier")

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"), nullable=False)
    order_date = Column(Date, nullable=False)
    expected_delivery_date = Column(Date, nullable=False)
    total_cost = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.Pending, nullable=False)

    supplier = relationship("Supplier", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    cost_per_unit = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
