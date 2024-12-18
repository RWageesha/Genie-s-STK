# ui/sell_product_dialog.py

from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QSpinBox, QMessageBox, QComboBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from domain.domain_models import SaleRecord, Product
from datetime import date

class SellProductDialog(QDialog):
    def __init__(self, parent=None, inventory_service=None):
        super().__init__(parent)
        self.inventory_service = inventory_service
        self.setWindowTitle("Sell Product")
        
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Load products into combo box
        self.product_combo = QComboBox()
        self.products = self.inventory_service.get_all_products()
        self.product_map = {product.name: product for product in self.products}
        self.product_combo.addItems([product.name for product in self.products])
        self.layout.addRow("Product:", self.product_combo)

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 1000000)
        self.layout.addRow("Quantity to Sell:", self.quantity_spin)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)

        self.apply_styles()

    def apply_styles(self):
        # Apply modern UI design based on the provided guidelines
        self.setFont(QFont("Roboto", 14))
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2d; 
                color: #c4c4c4; 
                font-family: "Roboto";
            }

            QFormLayout QLabel {
                color: #00adb5;
                font-size: 16px;
                font-weight: 600;
            }

            QComboBox {
                background-color: #2b2b3c; 
                color: #ffffff; 
                border: 1px solid #5a5f66; 
                padding: 4px;
            }

            QComboBox:focus {
                border: 1px solid #00adb5;
            }

            QComboBox QAbstractItemView {
                background-color: #1e1e2d; 
                selection-background-color: #323544; 
                color: #ffffff;
            }

            QSpinBox {
                background-color: #2b2b3c;
                color: #ffffff;
                border: 1px solid #5a5f66; 
                padding: 4px;
            }

            QSpinBox:focus {
                border: 1px solid #00adb5;
            }

            QDialogButtonBox QPushButton {
                background-color: #00adb5; 
                color: #ffffff; 
                border-radius: 5px; 
                padding: 8px 12px; 
                font-weight: bold;
            }

            QDialogButtonBox QPushButton:hover {
                background-color: #007f8b;
            }

            QMessageBox {
                background-color: #1e1e2d;
                color: #c4c4c4;
            }
        """)

    def validate_and_accept(self):
        product_name = self.product_combo.currentText()
        product = self.product_map.get(product_name)
        if not product:
            QMessageBox.warning(self, "Input Error", "Please select a valid product.")
            return

        quantity = self.quantity_spin.value()
        available = self.inventory_service.get_available_quantity(product.product_id)
        if quantity > available:
            QMessageBox.warning(self, "Insufficient Stock", f"Only {available} units available.")
            self.quantity_spin.setValue(available)
            return

        self.accept()

    def get_sale_record_data(self) -> SaleRecord:
        product_name = self.product_combo.currentText()
        product = self.product_map.get(product_name)
        quantity_sold = self.quantity_spin.value()
        sale_date = date.today()
        unit_price_at_sale = product.unit_price if product else 0.0
        return SaleRecord(
            sale_id=None,
            product_id=product.product_id if product else None,
            quantity_sold=quantity_sold,
            sale_date=sale_date,
            unit_price_at_sale=unit_price_at_sale
        )
