# ui/sales_management.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QHeaderView
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from .sell_product_dialog import SellProductDialog

class SalesManagement(QWidget):
    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Top buttons layout
        btn_layout = QHBoxLayout()
        self.record_sale_btn = QPushButton("Record Sale")
        self.view_details_btn = QPushButton("View Sale Details")
        
        self.record_sale_btn.clicked.connect(self.record_sale)
        self.view_details_btn.clicked.connect(self.view_sale_details)
        
        btn_layout.addWidget(self.record_sale_btn)
        btn_layout.addWidget(self.view_details_btn)
        btn_layout.addStretch()
        
        self.layout.addLayout(btn_layout)
        
        # Sales table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Sale ID", "Product", "Quantity Sold", "Sale Date", "Unit Price", "Total Sale Value"
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.layout.addWidget(self.table)
        
        self.load_sales()
        self.apply_styles()

    def apply_styles(self):
        # Apply modern UI design based on the provided guidelines
        self.setFont(QFont("Roboto", 14))
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2d;
                color: #c4c4c4;
                font-family: "Roboto";
                font-size: 14px;
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

    def load_sales(self):
        """
        Loads all sales from the inventory service and displays them in the table.
        """
        try:
            self.table.setRowCount(0)
            sales = self.inventory_service.get_all_sales()
            for sale in sales:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                
                # Fetch product name using product_id
                product = self.inventory_service.get_product_by_id(sale.product_id)
                product_name = product.name if product else "Unknown"
                
                self.table.setItem(row_position, 0, QTableWidgetItem(str(sale.sale_id)))
                self.table.setItem(row_position, 1, QTableWidgetItem(product_name))
                self.table.setItem(row_position, 2, QTableWidgetItem(str(sale.quantity_sold)))
                self.table.setItem(row_position, 3, QTableWidgetItem(sale.sale_date.strftime("%Y-%m-%d")))
                self.table.setItem(row_position, 4, QTableWidgetItem(f"{sale.unit_price_at_sale:.2f}"))
                total_value = sale.quantity_sold * sale.unit_price_at_sale
                self.table.setItem(row_position, 5, QTableWidgetItem(f"{total_value:.2f}"))
            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load sales: {str(e)}")

    def record_sale(self):
        """
        Opens the SellProductDialog to record a new sale.
        """
        dialog = SellProductDialog(self, self.inventory_service)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            sale_record = dialog.get_sale_record_data()
            try:
                self.inventory_service.record_sale(sale_record)
                QMessageBox.information(self, "Success", f"Sale ID {sale_record.sale_id} recorded successfully.")
                self.load_sales()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to record sale: {e}")

    def view_sale_details(self):
        """
        Displays the details of the selected sale.
        """
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a sale to view details.")
            return
        row = selected_items[0].row()
        sale_id_item = self.table.item(row, 0)
        if not sale_id_item:
            QMessageBox.critical(self, "Error", "Failed to retrieve selected sale ID.")
            return
        try:
            sale_id = int(sale_id_item.text())
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid Sale ID.")
            return

        try:
            sale = self.inventory_service.get_sale_by_id(sale_id)
            if not sale:
                QMessageBox.critical(self, "Error", "Selected sale not found.")
                return
            # Fetch product name using product_id
            product = self.inventory_service.get_product_by_id(sale.product_id)
            product_name = product.name if product else "Unknown"
            details = (
                f"Sale ID: {sale.sale_id}\n"
                f"Product: {product_name}\n"
                f"Quantity Sold: {sale.quantity_sold}\n"
                f"Sale Date: {sale.sale_date.strftime('%Y-%m-%d')}\n"
                f"Unit Price at Sale: {sale.unit_price_at_sale:.2f}\n"
                f"Total Sale Value: {sale.quantity_sold * sale.unit_price_at_sale:.2f}"
            )
            QMessageBox.information(self, "Sale Details", details)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to retrieve sale details: {e}")