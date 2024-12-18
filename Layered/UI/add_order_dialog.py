# ui/add_order_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import QDate

from domain.domain_models import Order, OrderItem, Supplier, Product, OrderStatus


class AddOrderDialog(QDialog):
    def __init__(self, parent=None, inventory_service=None, order: Order = None):
        super().__init__(parent)
        self.inventory_service = inventory_service
        self.order = order
        self.setWindowTitle("Add Order" if order is None else f"Edit Order ID {order.order_id}")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        form_layout = QFormLayout()
        
        self.supplier_combo = QComboBox()
        self.suppliers = self.inventory_service.get_all_suppliers()
        self.supplier_map = {supplier.name: supplier for supplier in self.suppliers}
        self.supplier_combo.addItems([supplier.name for supplier in self.suppliers])
        form_layout.addRow("Supplier:", self.supplier_combo)
        
        self.order_date_edit = QDateEdit(QDate.currentDate())
        self.order_date_edit.setCalendarPopup(True)
        self.order_date_edit.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow("Order Date:", self.order_date_edit)
        
        self.expected_delivery_edit = QDateEdit(QDate.currentDate().addDays(7))
        self.expected_delivery_edit.setCalendarPopup(True)
        self.expected_delivery_edit.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow("Expected Delivery Date:", self.expected_delivery_edit)
        
        self.layout.addLayout(form_layout)
        
        # Order items table
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(4)
        self.items_table.setHorizontalHeaderLabels(["Product", "Quantity", "Cost per Unit", "Total Cost"])
        self.items_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.items_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.items_table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.items_table)
        
        # Buttons to add/remove items
        items_btn_layout = QHBoxLayout()
        self.add_item_btn = QPushButton("Add Item")
        self.remove_item_btn = QPushButton("Remove Selected Item")
        items_btn_layout.addWidget(self.add_item_btn)
        items_btn_layout.addWidget(self.remove_item_btn)
        items_btn_layout.addStretch()
        self.layout.addLayout(items_btn_layout)
        
        self.add_item_btn.clicked.connect(self.add_item)
        self.remove_item_btn.clicked.connect(self.remove_item)
        
        # Total cost display
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        self.total_label = QLabel("Total Cost: 0.00")
        total_layout.addWidget(self.total_label)
        self.layout.addLayout(total_layout)
        
        # Dialog buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.button_box)
        
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)
        
        if self.order:
            self.populate_order()
    
    def populate_order(self):
        supplier_name = self.order.supplier.name if self.order.supplier else ""
        index = self.supplier_combo.findText(supplier_name)
        if index != -1:
            self.supplier_combo.setCurrentIndex(index)
        self.order_date_edit.setDate(QDate(self.order.order_date.year, self.order.order_date.month, self.order.order_date.day))
        self.expected_delivery_edit.setDate(QDate(self.order.expected_delivery_date.year, self.order.expected_delivery_date.month, self.order.expected_delivery_date.day))
        for item in self.order.items:
            self.insert_order_item(item)
        self.update_total_cost()
    
    def add_item(self):
        dialog = AddOrderItemDialog(self, self.inventory_service)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            order_item = dialog.get_order_item_data()
            self.insert_order_item(order_item)
            self.update_total_cost()
    
    def insert_order_item(self, order_item: OrderItem):
        row_position = self.items_table.rowCount()
        self.items_table.insertRow(row_position)
        self.items_table.setItem(row_position, 0, QTableWidgetItem(order_item.product.name))
        self.items_table.setItem(row_position, 1, QTableWidgetItem(str(order_item.quantity)))
        self.items_table.setItem(row_position, 2, QTableWidgetItem(f"{order_item.cost_per_unit:.2f}"))
        total_cost = order_item.quantity * order_item.cost_per_unit
        self.items_table.setItem(row_position, 3, QTableWidgetItem(f"{total_cost:.2f}"))
    
    def remove_item(self):
        selected_items = self.items_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select an item to remove.")
            return
        row = selected_items[0].row()
        self.items_table.removeRow(row)
        self.update_total_cost()
    
    def update_total_cost(self):
        total = 0.0
        for row in range(self.items_table.rowCount()):
            total += float(self.items_table.item(row, 3).text())
        self.total_label.setText(f"Total Cost: {total:.2f}")
    
    def validate_and_accept(self):
        if self.items_table.rowCount() == 0:
            QMessageBox.warning(self, "No Items", "Please add at least one order item.")
            return
        self.accept()
    
    def get_order_data(self) -> Order:
        supplier_name = self.supplier_combo.currentText()
        supplier = self.supplier_map.get(supplier_name)
        order_date = self.order_date_edit.date().toPyDate()
        expected_delivery = self.expected_delivery_edit.date().toPyDate()
        items = []
        for row in range(self.items_table.rowCount()):
            product_name = self.items_table.item(row, 0).text()
            quantity = int(self.items_table.item(row, 1).text())
            cost_per_unit = float(self.items_table.item(row, 2).text())
            product = self.inventory_service.get_product_by_name(product_name)
            if not product:
                continue
            items.append(OrderItem(
                order_item_id=None,  # Assuming new items have no ID yet
                order_id=self.order.order_id if self.order else None,
                product_id=product.product_id,
                quantity=quantity,
                cost_per_unit=cost_per_unit
            ))
        total_cost = sum(item.quantity * item.cost_per_unit for item in items)
        return Order(
            order_id=self.order.order_id if self.order else None,
            supplier_id=supplier.supplier_id if supplier else None,
            order_date=order_date,
            expected_delivery_date=expected_delivery,
            items=items,
            total_cost=total_cost,
            status=self.order.status if self.order else OrderStatus.Pending
        )

class AddOrderItemDialog(QDialog):
    def __init__(self, parent=None, inventory_service=None):
        super().__init__(parent)
        self.inventory_service = inventory_service
        self.setWindowTitle("Add Order Item")
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        
        self.product_combo = QComboBox()
        self.products = self.inventory_service.get_all_products()
        self.product_map = {product.name: product for product in self.products}
        self.product_combo.addItems([product.name for product in self.products])
        self.layout.addRow("Product:", self.product_combo)
        
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 1000000)
        self.layout.addRow("Quantity:", self.quantity_spin)
        
        self.cost_spin = QDoubleSpinBox()
        self.cost_spin.setRange(0.01, 1000000.00)
        self.cost_spin.setDecimals(2)
        self.layout.addRow("Cost per Unit:", self.cost_spin)
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.button_box)
        
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)
    
    def validate_and_accept(self):
        if not self.product_combo.currentText().strip():
            QMessageBox.warning(self, "Input Error", "Product must be selected.")
            self.product_combo.setFocus()
            return
        self.accept()
    
    def get_order_item_data(self) -> OrderItem:
        product_name = self.product_combo.currentText()
        product = self.product_map.get(product_name)
        quantity = self.quantity_spin.value()
        cost_per_unit = self.cost_spin.value()
        return OrderItem(
            order_item_id=None,  # Assuming new items have no ID yet
            order_id=None,        # Will be set when adding to order
            product_id=product.product_id if product else None,
            quantity=quantity,
            cost_per_unit=cost_per_unit
        )
