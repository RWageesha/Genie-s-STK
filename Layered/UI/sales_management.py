# ui/sales_management.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt

from .sell_product_dialog import SellProductDialog

class SalesManagement(QWidget):
    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Top buttons
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
        self.layout.addWidget(self.table)
        
        self.load_sales()
    
    def load_sales(self):
        self.table.setRowCount(0)
        sales = self.inventory_service.get_all_sales()
        for sale in sales:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(sale.sale_id)))
            self.table.setItem(row_position, 1, QTableWidgetItem(sale.product.name if sale.product else ""))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(sale.quantity_sold)))
            self.table.setItem(row_position, 3, QTableWidgetItem(sale.sale_date.strftime("%Y-%m-%d")))
            self.table.setItem(row_position, 4, QTableWidgetItem(f"{sale.unit_price_at_sale:.2f}"))
            total_value = sale.quantity_sold * sale.unit_price_at_sale
            self.table.setItem(row_position, 5, QTableWidgetItem(f"{total_value:.2f}"))
        self.table.resizeColumnsToContents()
    
    def record_sale(self):
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
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a sale to view details.")
            return
        row = selected_items[0].row()
        sale_id = int(self.table.item(row, 0).text())
        sale = self.inventory_service.get_sale_by_id(sale_id)
        if not sale:
            QMessageBox.critical(self, "Error", "Selected sale not found.")
            return
        details = (
            f"Sale ID: {sale.sale_id}\n"
            f"Product: {sale.product.name if sale.product else ''}\n"
            f"Quantity Sold: {sale.quantity_sold}\n"
            f"Sale Date: {sale.sale_date}\n"
            f"Unit Price at Sale: {sale.unit_price_at_sale}\n"
            f"Total Sale Value: {sale.quantity_sold * sale.unit_price_at_sale:.2f}"
        )
        QMessageBox.information(self, "Sale Details", details)
