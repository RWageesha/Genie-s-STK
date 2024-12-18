# ui/orders_management.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt

from .add_order_dialog import AddOrderDialog

class OrdersManagement(QWidget):
    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Top buttons
        btn_layout = QHBoxLayout()
        self.add_order_btn = QPushButton("Add Order")
        self.edit_order_btn = QPushButton("Edit Order")
        self.delete_order_btn = QPushButton("Delete Order")
        
        self.add_order_btn.clicked.connect(self.add_order)
        self.edit_order_btn.clicked.connect(self.edit_order)
        self.delete_order_btn.clicked.connect(self.delete_order)
        
        btn_layout.addWidget(self.add_order_btn)
        btn_layout.addWidget(self.edit_order_btn)
        btn_layout.addWidget(self.delete_order_btn)
        btn_layout.addStretch()
        
        self.layout.addLayout(btn_layout)
        
        # Orders table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Order ID", "Supplier", "Order Date", "Expected Delivery", "Total Cost", "Status"
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.table)
        
        self.load_orders()
    
    def load_orders(self):
        self.table.setRowCount(0)
        orders = self.inventory_service.get_all_orders()
        for order in orders:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(order.order_id)))
            self.table.setItem(row_position, 1, QTableWidgetItem(order.supplier.name if order.supplier else ""))
            self.table.setItem(row_position, 2, QTableWidgetItem(order.order_date.strftime("%Y-%m-%d")))
            self.table.setItem(row_position, 3, QTableWidgetItem(order.expected_delivery_date.strftime("%Y-%m-%d")))
            self.table.setItem(row_position, 4, QTableWidgetItem(f"{order.total_cost:.2f}"))
            self.table.setItem(row_position, 5, QTableWidgetItem(order.status.value))
        self.table.resizeColumnsToContents()
    
    def add_order(self):
        dialog = AddOrderDialog(self, self.inventory_service)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            order = dialog.get_order_data()
            try:
                self.inventory_service.add_order(order)
                QMessageBox.information(self, "Success", f"Order ID {order.order_id} added successfully.")
                self.load_orders()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add order: {e}")
    
    def edit_order(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select an order to edit.")
            return
        row = selected_items[0].row()
        order_id = int(self.table.item(row, 0).text())
        order = self.inventory_service.get_order_by_id(order_id)
        if not order:
            QMessageBox.critical(self, "Error", "Selected order not found.")
            return
        dialog = AddOrderDialog(self, self.inventory_service, order)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_order = dialog.get_order_data()
            try:
                self.inventory_service.update_order(updated_order)
                QMessageBox.information(self, "Success", f"Order ID {updated_order.order_id} updated successfully.")
                self.load_orders()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update order: {e}")
    
    def delete_order(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select an order to delete.")
            return
        row = selected_items[0].row()
        order_id = int(self.table.item(row, 0).text())
        order = self.inventory_service.get_order_by_id(order_id)
        if not order:
            QMessageBox.critical(self, "Error", "Selected order not found.")
            return
        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f"Are you sure you want to delete Order ID {order.order_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.inventory_service.delete_order(order_id)
                QMessageBox.information(self, "Success", f"Order ID {order_id} deleted successfully.")
                self.load_orders()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete order: {e}")
