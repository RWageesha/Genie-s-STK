# ui/add_batch_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QSpinBox, QDateEdit, QComboBox, QMessageBox
)
from PyQt6.QtCore import QDate
from domain.domain_models import Batch, Product

class AddBatchDialog(QDialog):
    def __init__(self, parent=None, inventory_service=None, batch: Batch = None):
        super().__init__(parent)
        self.inventory_service = inventory_service
        self.batch = batch
        self.setWindowTitle("Add Batch" if batch is None else f"Edit Batch ID {batch.batch_id}")
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
        
        self.manufacture_date_edit = QDateEdit(QDate.currentDate())
        self.manufacture_date_edit.setCalendarPopup(True)
        self.manufacture_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.layout.addRow("Manufacture Date:", self.manufacture_date_edit)
        
        self.expiry_date_edit = QDateEdit(QDate.currentDate().addYears(1))
        self.expiry_date_edit.setCalendarPopup(True)
        self.expiry_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.layout.addRow("Expiry Date:", self.expiry_date_edit)
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.button_box)
        
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)
        
        if self.batch:
            product_name = self.batch.product.name if self.batch.product else ""
            index = self.product_combo.findText(product_name)
            if index != -1:
                self.product_combo.setCurrentIndex(index)
            self.product_combo.setEnabled(False)  # Prevent changing product once set
            self.quantity_spin.setValue(self.batch.quantity)
            self.manufacture_date_edit.setDate(QDate(self.batch.manufacture_date.year, self.batch.manufacture_date.month, self.batch.manufacture_date.day))
            self.expiry_date_edit.setDate(QDate(self.batch.expiry_date.year, self.batch.expiry_date.month, self.batch.expiry_date.day))
            self.batch_id = self.batch.batch_id
        else:
            self.batch_id = None
    
    def validate_and_accept(self):
        if not self.product_combo.currentText().strip():
            QMessageBox.warning(self, "Input Error", "Product must be selected.")
            self.product_combo.setFocus()
            return
        if self.manufacture_date_edit.date() > self.expiry_date_edit.date():
            QMessageBox.warning(self, "Date Error", "Expiry date must be after manufacture date.")
            self.expiry_date_edit.setFocus()
            return
        self.accept()
    
    def get_batch_data(self) -> Batch:
        product_name = self.product_combo.currentText()
        product = self.product_map.get(product_name)
        quantity = self.quantity_spin.value()
        manufacture_date = self.manufacture_date_edit.date().toPyDate()
        expiry_date = self.expiry_date_edit.date().toPyDate()
        return Batch(
            batch_id=self.batch_id,
            product=product,
            quantity=quantity,
            manufacture_date=manufacture_date,
            expiry_date=expiry_date
        )
