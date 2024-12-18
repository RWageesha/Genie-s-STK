# ui/products_management.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDialog
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from .add_product_dialog import AddProductDialog

class ProductsManagement(QWidget):
    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Top buttons
        btn_layout = QHBoxLayout()
        self.add_product_btn = QPushButton("Add Product")
        self.edit_product_btn = QPushButton("Edit Product")
        self.delete_product_btn = QPushButton("Delete Product")
        
        self.add_product_btn.clicked.connect(self.add_product)
        self.edit_product_btn.clicked.connect(self.edit_product)
        self.delete_product_btn.clicked.connect(self.delete_product)
        
        btn_layout.addWidget(self.add_product_btn)
        btn_layout.addWidget(self.edit_product_btn)
        btn_layout.addWidget(self.delete_product_btn)
        btn_layout.addStretch()
        
        self.layout.addLayout(btn_layout)
        
        # Products table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Product ID", "SKU", "Name", "Category", "Description", "Unit Price", "Reorder Level"
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.table)
        
        self.load_products()
        self.apply_styles()

    def apply_styles(self):
        # Apply modern UI design based on the provided guidelines
        self.setFont(QFont("Roboto", 14))
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2d;
                color: #c4c4c4;
                font-family: "Roboto";
            }

            QPushButton {
                background-color: #00adb5;
                color: #ffffff;
                border-radius: 5px;
                padding: 8px 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #007f8b;
            }

            QTableWidget {
                background-color: #1e1e2d;
                gridline-color: #5a5f66;
                border: 1px solid #5a5f66;
                font-size: 14px;
            }

            QTableWidget::item {
                color: #ffffff;
            }

            QTableWidget::item:selected {
                background-color: #323544;
            }

            QHeaderView::section {
                background-color: #2b2b3c;
                color: #ffffff;
                font-weight: bold;
                border: none;
                padding: 4px;
            }

            QMessageBox {
                background-color: #1e1e2d;
                color: #c4c4c4;
            }
        """)

    def load_products(self):
        self.table.setRowCount(0)
        products = self.inventory_service.get_all_products()
        for product in products:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(product.product_id)))
            self.table.setItem(row_position, 1, QTableWidgetItem(product.sku))
            self.table.setItem(row_position, 2, QTableWidgetItem(product.name))
            self.table.setItem(row_position, 3, QTableWidgetItem(product.category))
            self.table.setItem(row_position, 4, QTableWidgetItem(product.description or ""))
            self.table.setItem(row_position, 5, QTableWidgetItem(f"{product.unit_price:.2f}"))
            self.table.setItem(row_position, 6, QTableWidgetItem(str(product.reorder_level)))
        self.table.resizeColumnsToContents()
    
    def add_product(self):
        dialog = AddProductDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            product = dialog.get_product_data()
            try:
                self.inventory_service.add_product(product)
                QMessageBox.information(self, "Success", f"Product '{product.name}' added successfully.")
                self.load_products()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add product: {e}")
    
    def edit_product(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a product to edit.")
            return
        row = selected_items[0].row()
        product_id = int(self.table.item(row, 0).text())
        product = self.inventory_service.get_product_by_id(product_id)
        if not product:
            QMessageBox.critical(self, "Error", "Selected product not found.")
            return
        dialog = AddProductDialog(self, product)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_product = dialog.get_product_data()
            try:
                self.inventory_service.update_product(updated_product)
                QMessageBox.information(self, "Success", f"Product '{updated_product.name}' updated successfully.")
                self.load_products()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update product: {e}")
    
    def delete_product(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a product to delete.")
            return
        row = selected_items[0].row()
        product_id = int(self.table.item(row, 0).text())
        product = self.inventory_service.get_product_by_id(product_id)
        if not product:
            QMessageBox.critical(self, "Error", "Selected product not found.")
            return
        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f"Are you sure you want to delete product '{product.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.inventory_service.delete_product(product_id)
                QMessageBox.information(self, "Success", f"Product '{product.name}' deleted successfully.")
                self.load_products()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete product: {e}")
