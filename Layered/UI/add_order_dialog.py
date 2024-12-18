# ui/add_order_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QComboBox, QDateEdit,
    QSpinBox, QDoubleSpinBox, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QFrame
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont
from domain.domain_models import Order, OrderItem, Supplier, Product, OrderStatus


class AddOrderDialog(QDialog):
    def __init__(self, parent=None, inventory_service=None, order: Order = None):
        super().__init__(parent)
        self.inventory_service = inventory_service
        self.order = order
        self.setWindowTitle("Add Order" if order is None else f"Edit Order ID {order.order_id}")
        self.setFixedWidth(600)  # Increased width for better layout
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)  # Remove help button

        self.setStyleSheet("""
            QDialog {
                background-color: #2C2C3E;
                color: #E0E0E0;
                border-radius: 12px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 15px;
            }
            QLabel {
                font-size: 15px;
                color: #E0E0E0;
                background-color: transparent;
            }
            QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox {
                background-color: #3A3A4D;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 8px;
                font-size: 15px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #555555;
                border-left-style: solid;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }
            QComboBox::down-arrow {
                image: url(:/icons/down_arrow.png); /* Replace with your arrow icon path */
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #555555;
                border-left-style: solid;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }
            QPushButton {
                background-color: #00ADB5;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 15px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #009A9C;
            }
            QPushButton:pressed {
                background-color: #007F7F;
            }
            QDialogButtonBox {
                border: none;
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
            }
        """)

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("Add Order" if order is None else "Edit Order")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header.setStyleSheet("color: #00ADB5;")
        self.main_layout.addWidget(header)

        # Separator Line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #555555;")
        self.main_layout.addWidget(separator)

        # Form Layout
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(form_layout)

        # Supplier Selection
        self.supplier_combo = QComboBox()
        self.suppliers = self.inventory_service.get_all_suppliers()
        self.supplier_map = {supplier.name: supplier for supplier in self.suppliers}
        self.supplier_combo.addItems([supplier.name for supplier in self.suppliers])
        self.supplier_combo.setPlaceholderText("Select Supplier")
        form_layout.addRow("Supplier:", self.supplier_combo)

        # Order Date
        self.order_date_edit = QDateEdit(QDate.currentDate())
        self.order_date_edit.setCalendarPopup(True)
        self.order_date_edit.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow("Order Date:", self.order_date_edit)

        # Expected Delivery Date
        self.expected_delivery_edit = QDateEdit(QDate.currentDate().addDays(7))
        self.expected_delivery_edit.setCalendarPopup(True)
        self.expected_delivery_edit.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow("Expected Delivery Date:", self.expected_delivery_edit)

        # Order Items Table
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(4)
        self.items_table.setHorizontalHeaderLabels(["Product", "Quantity", "Cost per Unit", "Total Cost"])
        self.items_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.items_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.items_table.horizontalHeader().setStretchLastSection(True)
        self.items_table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.items_table.setAlternatingRowColors(True)
        self.main_layout.addWidget(self.items_table)

        # Buttons to Add/Remove Items
        items_btn_layout = QHBoxLayout()
        self.add_item_btn = QPushButton("Add Item")
        self.remove_item_btn = QPushButton("Remove Selected Item")
        items_btn_layout.addWidget(self.add_item_btn)
        items_btn_layout.addWidget(self.remove_item_btn)
        items_btn_layout.addStretch()
        self.main_layout.addLayout(items_btn_layout)

        self.add_item_btn.clicked.connect(self.add_item)
        self.remove_item_btn.clicked.connect(self.remove_item)

        # Total Cost Display
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        self.total_label = QLabel("Total Cost: $0.00")
        self.total_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        total_layout.addWidget(self.total_label)
        self.main_layout.addLayout(total_layout)

        # Dialog Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Save Order")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancel")
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setFixedHeight(40)
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setFixedHeight(40)
        self.main_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)

        if self.order:
            self.populate_order()

    def populate_order(self):
        """Populate the dialog with existing order data for editing."""
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
        """Open the AddOrderItemDialog to add a new order item."""
        dialog = AddOrderItemDialog(self, self.inventory_service)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            order_item = dialog.get_order_item_data()
            self.insert_order_item(order_item)
            self.update_total_cost()

    def insert_order_item(self, order_item: OrderItem):
        """Insert an order item into the items table."""
        row_position = self.items_table.rowCount()
        self.items_table.insertRow(row_position)
        self.items_table.setItem(row_position, 0, QTableWidgetItem(order_item.product.name))
        self.items_table.setItem(row_position, 1, QTableWidgetItem(str(order_item.quantity)))
        self.items_table.setItem(row_position, 2, QTableWidgetItem(f"${order_item.cost_per_unit:.2f}"))
        total_cost = order_item.quantity * order_item.cost_per_unit
        self.items_table.setItem(row_position, 3, QTableWidgetItem(f"${total_cost:.2f}"))

    def remove_item(self):
        """Remove the selected order item from the items table."""
        selected_items = self.items_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select an item to remove.")
            return
        row = selected_items[0].row()
        self.items_table.removeRow(row)
        self.update_total_cost()

    def update_total_cost(self):
        """Calculate and update the total cost of the order."""
        total = 0.0
        for row in range(self.items_table.rowCount()):
            total_text = self.items_table.item(row, 3).text().replace('$', '').strip()
            try:
                total += float(total_text)
            except ValueError:
                continue
        self.total_label.setText(f"Total Cost: ${total:.2f}")

    def validate_and_accept(self):
        """Validate inputs and accept the dialog if all checks pass."""
        if self.items_table.rowCount() == 0:
            QMessageBox.warning(self, "No Items", "Please add at least one order item.")
            return
        self.accept()

    def get_order_data(self) -> Order:
        """Retrieve the order data from the dialog."""
        supplier_name = self.supplier_combo.currentText()
        supplier = self.supplier_map.get(supplier_name)
        order_date = self.order_date_edit.date().toPyDate()
        expected_delivery = self.expected_delivery_edit.date().toPyDate()
        items = []
        for row in range(self.items_table.rowCount()):
            product_name = self.items_table.item(row, 0).text()
            quantity = int(self.items_table.item(row, 1).text())
            cost_per_unit_text = self.items_table.item(row, 2).text().replace('$', '').strip()
            try:
                cost_per_unit = float(cost_per_unit_text)
            except ValueError:
                cost_per_unit = 0.0
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
        self.setFixedWidth(400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)  # Remove help button

        self.setStyleSheet("""
            QDialog {
                background-color: #2C2C3E;
                color: #E0E0E0;
                border-radius: 12px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 15px;
            }
            QLabel {
                font-size: 15px;
                color: #E0E0E0;
                background-color: transparent;
            }
            QComboBox, QSpinBox, QDoubleSpinBox {
                background-color: #3A3A4D;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 8px;
                font-size: 15px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #555555;
                border-left-style: solid;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }
            QComboBox::down-arrow {
                image: url(:/icons/down_arrow.png); /* Replace with your arrow icon path */
            }
            QPushButton {
                background-color: #00ADB5;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 15px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #009A9C;
            }
            QPushButton:pressed {
                background-color: #007F7F;
            }
            QDialogButtonBox {
                border: none;
            }
        """)

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("Add Order Item")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header.setStyleSheet("color: #00ADB5;")
        self.main_layout.addWidget(header)

        # Separator Line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #555555;")
        self.main_layout.addWidget(separator)

        # Form Layout
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(form_layout)

        # Product Selection
        self.product_combo = QComboBox()
        self.products = self.inventory_service.get_all_products()
        self.product_map = {product.name: product for product in self.products}
        self.product_combo.addItems([product.name for product in self.products])
        self.product_combo.setPlaceholderText("Select Product")
        form_layout.addRow("Product:", self.product_combo)

        # Quantity SpinBox
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 1000000)
        self.quantity_spin.setValue(1)
        form_layout.addRow("Quantity:", self.quantity_spin)

        # Cost per Unit SpinBox
        self.cost_spin = QDoubleSpinBox()
        self.cost_spin.setRange(0.01, 1000000.00)
        self.cost_spin.setDecimals(2)
        self.cost_spin.setPrefix("$ ")
        self.cost_spin.setSingleStep(0.10)
        form_layout.addRow("Cost per Unit:", self.cost_spin)

        # Dialog Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Add Item")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancel")
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setFixedHeight(40)
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setFixedHeight(40)
        self.main_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)

    def validate_and_accept(self):
        """Validate inputs and accept the dialog if all checks pass."""
        if not self.product_combo.currentText().strip():
            QMessageBox.warning(self, "Input Error", "Product must be selected.")
            self.product_combo.setFocus()
            return
        if self.cost_spin.value() <= 0:
            QMessageBox.warning(self, "Input Error", "Cost per unit must be greater than zero.")
            self.cost_spin.setFocus()
            return
        self.accept()

    def get_order_item_data(self) -> OrderItem:
        """Retrieve the order item data from the dialog."""
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
