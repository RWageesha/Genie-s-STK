# UI/sell_product_widget.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt
from domain.domain_models import Product
from typing import List
from datetime import date

class SellProductWidget(QWidget):
    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service
        self.cart = []  # List to store cart items
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Product Selection Layout
        product_layout = QHBoxLayout()
        
        product_label = QLabel("Select Product:")
        self.product_combo = QComboBox()
        self.load_products()
        
        quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter quantity")
        self.quantity_input.setValidator(QIntValidator(1, 1000000, self))
        
        add_button = QPushButton("Add to Cart")
        add_button.clicked.connect(self.add_to_cart)
        
        product_layout.addWidget(product_label)
        product_layout.addWidget(self.product_combo)
        product_layout.addWidget(quantity_label)
        product_layout.addWidget(self.quantity_input)
        product_layout.addWidget(add_button)
        
        main_layout.addLayout(product_layout)
        
        # Cart Table
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(4)
        self.cart_table.setHorizontalHeaderLabels([
            "Product ID", "Product Name", "Quantity", "Unit Price"
        ])
        self.cart_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.cart_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.cart_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.cart_table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.cart_table)
        
        # Total and Finalize Sale Layout
        finalize_layout = QHBoxLayout()
        
        self.total_label = QLabel("Total: $0.00")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        finalize_button = QPushButton("Finalize Sale")
        finalize_button.clicked.connect(self.finalize_sale)
        
        finalize_layout.addStretch()
        finalize_layout.addWidget(self.total_label)
        finalize_layout.addWidget(finalize_button)
        
        main_layout.addLayout(finalize_layout)
        
        self.setLayout(main_layout)
    
    def load_products(self):
        """
        Loads all products into the product_combo dropdown.
        """
        try:
            products: List[Product] = self.inventory_service.get_all_products()
            self.product_combo.clear()
            for product in products:
                display_text = f"{product.name} (SKU: {product.sku})"
                self.product_combo.addItem(display_text, userData=product.product_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load products: {str(e)}")
    
    def add_to_cart(self):
        """
        Adds the selected product and quantity to the cart.
        """
        product_id = self.product_combo.currentData()
        quantity_text = self.quantity_input.text()
        
        if not quantity_text.isdigit():
            QMessageBox.warning(self, "Input Error", "Please enter a valid quantity.")
            return
        
        quantity = int(quantity_text)
        if quantity <= 0:
            QMessageBox.warning(self, "Input Error", "Quantity must be greater than zero.")
            return
        
        try:
            product = self.inventory_service.get_product_by_id(product_id)
            if not product:
                QMessageBox.warning(self, "Error", "Selected product not found.")
                return
            
            available_quantity = self.inventory_service.get_available_quantity(product_id)
            if quantity > available_quantity:
                QMessageBox.warning(
                    self, "Insufficient Stock",
                    f"Only {available_quantity} units of '{product.name}' are available."
                )
                return
            
            # Add to cart
            self.cart.append({
                "product_id": product.product_id,
                "product_name": product.name,
                "quantity": quantity,
                "unit_price": product.unit_price
            })
            
            self.update_cart_table()
            self.quantity_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add to cart: {str(e)}")
    
    def update_cart_table(self):
        """
        Updates the cart_table to display current cart items and calculates the total.
        """
        self.cart_table.setRowCount(len(self.cart))
        total = 0.0
        for row, item in enumerate(self.cart):
            self.cart_table.setItem(row, 0, QTableWidgetItem(str(item["product_id"])))
            self.cart_table.setItem(row, 1, QTableWidgetItem(item["product_name"]))
            self.cart_table.setItem(row, 2, QTableWidgetItem(str(item["quantity"])))
            self.cart_table.setItem(row, 3, QTableWidgetItem(f"${item['unit_price']:.2f}"))
            total += item["quantity"] * item["unit_price"]
        
        self.total_label.setText(f"Total: ${total:.2f}")
    
    def finalize_sale(self):
        """
        Processes the sale by recording each item in the cart.
        """
        if not self.cart:
            QMessageBox.warning(self, "Empty Cart", "No items in the cart to sell.")
            return
        
        try:
            for item in self.cart:
                sale_record = {
                    "product_id": item["product_id"],
                    "quantity_sold": item["quantity"],
                    "sale_date": date.today(),
                    "unit_price_at_sale": item["unit_price"]
                }
                self.inventory_service.record_sale(sale_record)
                self.inventory_service.reduce_batch_quantity(item["product_id"], item["quantity"])
            
            QMessageBox.information(self, "Success", "Sale completed successfully.")
            self.cart.clear()
            self.update_cart_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to finalize sale: {str(e)}")
