# ui/orders_management.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QHBoxLayout, QHeaderView, QLabel, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from .add_order_dialog import AddOrderDialog
from domain.domain_models import Order  # Ensure Order model is correctly imported
from typing import List


class OrdersManagement(QWidget):
    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service
        self.init_ui()

    def init_ui(self):
        # Apply stylesheet for consistent styling
        self.setStyleSheet("""
            QWidget {
                background-color: #2C2C3E;
                color: #E0E0E0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 15px;
            }
            QPushButton {
                background-color: #00ADB5;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: #009A9C;
            }
            QPushButton:pressed {
                background-color: #007F7F;
            }
            QTableWidget {
                background-color: #3A3A4D;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 6px;
                font-size: 14px;
            }
            QTableWidget::item:selected {
                background-color: #00ADB5;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #555555;
                color: #FFFFFF;
                padding: 5px;
                border: 1px solid #3A3A4D;
                font-weight: bold;
            }
            QLabel {
                font-size: 18px;
                color: #00ADB5;
                font-weight: bold;
                background-color: transparent;
            }
            QFrame {
                border: 1px solid #555555;
                margin-top: 10px;
                margin-bottom: 10px;
            }
        """)

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("Orders Management")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.main_layout.addWidget(header)

        # Separator Line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.main_layout.addWidget(separator)

        # Buttons Layout
        buttons_layout = QHBoxLayout()

        # Add Order Button
        add_order_btn = QPushButton("Add Order")
        add_order_btn.setIcon(QIcon(":/icons/add.png"))  # Replace with your icon path
        add_order_btn.setToolTip("Add a new order")
        add_order_btn.clicked.connect(self.add_order)
        buttons_layout.addWidget(add_order_btn)

        # Edit Order Button
        edit_order_btn = QPushButton("Edit Order")
        edit_order_btn.setIcon(QIcon(":/icons/edit.png"))  # Replace with your icon path
        edit_order_btn.setToolTip("Edit the selected order")
        edit_order_btn.clicked.connect(self.edit_order)
        buttons_layout.addWidget(edit_order_btn)

        # Delete Order Button
        delete_order_btn = QPushButton("Delete Order")
        delete_order_btn.setIcon(QIcon(":/icons/delete.png"))  # Replace with your icon path
        delete_order_btn.setToolTip("Delete the selected order")
        delete_order_btn.clicked.connect(self.delete_order)
        buttons_layout.addWidget(delete_order_btn)

        # Refresh Button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setIcon(QIcon(":/icons/refresh.png"))  # Replace with your icon path
        refresh_btn.setToolTip("Refresh the orders list")
        refresh_btn.clicked.connect(self.load_orders)
        buttons_layout.addWidget(refresh_btn)

        # Stretch to push buttons to the left
        buttons_layout.addStretch()

        self.main_layout.addLayout(buttons_layout)

        # Orders Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Order ID", "Supplier", "Order Date", "Expected Delivery", "Total Cost", "Status"
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #3A3A4D;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 6px;
            }
            QTableWidget::item:selected {
                background-color: #00ADB5;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #555555;
                color: #FFFFFF;
                padding: 5px;
                border: 1px solid #3A3A4D;
                font-weight: bold;
            }
        """)
        self.main_layout.addWidget(self.table)

        # Load orders initially
        self.load_orders()

    def load_orders(self):
        """
        Loads all orders from the inventory service and displays them in the table.
        """
        try:
            orders = self.inventory_service.get_all_orders()
            self.table.setRowCount(0)  # Clear existing rows
            for order in orders:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)

                # Populate table cells
                self.table.setItem(row_position, 0, QTableWidgetItem(str(order.order_id)))
                self.table.setItem(row_position, 1, QTableWidgetItem(order.supplier.name if order.supplier else "N/A"))
                self.table.setItem(row_position, 2, QTableWidgetItem(order.order_date.strftime("%Y-%m-%d")))
                self.table.setItem(row_position, 3, QTableWidgetItem(order.expected_delivery_date.strftime("%Y-%m-%d")))
                self.table.setItem(row_position, 4, QTableWidgetItem(f"Rs.{order.total_cost:.2f}"))
                self.table.setItem(row_position, 5, QTableWidgetItem(order.status.value))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load orders: {str(e)}")

    def add_order(self):
        """
        Opens the AddOrderDialog to collect order details and adds the order upon successful input.
        """
        dialog = AddOrderDialog(self, self.inventory_service)
        dialog.setModal(True)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            order = dialog.get_order_data()
            try:
                self.inventory_service.add_order(order)
                QMessageBox.information(self, "Success", f"Order ID {order.order_id} added successfully.")
                self.load_orders()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add order: {str(e)}")

    def edit_order(self):
        """
        Opens the AddOrderDialog to modify the selected order's details.
        """
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select an order to edit.")
            return

        row = selected_items[0].row()
        order_id_item = self.table.item(row, 0)
        if not order_id_item:
            QMessageBox.warning(self, "Error", "Failed to retrieve selected order ID.")
            return

        order_id = int(order_id_item.text())
        order = self.inventory_service.get_order_by_id(order_id)
        if not order:
            QMessageBox.warning(self, "Error", "Selected order not found.")
            return

        dialog = AddOrderDialog(self, self.inventory_service, order)
        dialog.setModal(True)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_order = dialog.get_order_data()
            try:
                self.inventory_service.update_order(updated_order)
                QMessageBox.information(self, "Success", f"Order ID {updated_order.order_id} updated successfully.")
                self.load_orders()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update order: {str(e)}")

    def delete_order(self):
        """
        Deletes the selected order after confirmation.
        """
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select an order to delete.")
            return

        row = selected_items[0].row()
        order_id_item = self.table.item(row, 0)
        if not order_id_item:
            QMessageBox.warning(self, "Error", "Failed to retrieve selected order ID.")
            return

        order_id = int(order_id_item.text())
        order = self.inventory_service.get_order_by_id(order_id)
        if not order:
            QMessageBox.warning(self, "Error", "Selected order not found.")
            return

        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f"Are you sure you want to delete Order ID {order.order_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.inventory_service.delete_order(order_id)
                QMessageBox.information(self, "Success", f"Order ID {order_id} deleted successfully.")
                self.load_orders()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete order: {e}")
