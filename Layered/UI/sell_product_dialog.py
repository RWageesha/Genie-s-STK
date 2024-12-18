# ui/sell_product_dialog.py

from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QSpinBox, QMessageBox, QComboBox
from domain.domain_models import SaleRecord, Product
from datetime import date

class SellProductDialog(QDialog):
    def __init__(self, parent=None, inventory_service=None):
        super().__init__(parent)
        self.inventory_service = inventory_service
        self.setWindowTitle("Sell Product")
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        
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
