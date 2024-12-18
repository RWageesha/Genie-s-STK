# ui/add_supplier_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QMessageBox
)
from domain.domain_models import Supplier

class AddSupplierDialog(QDialog):
    def __init__(self, parent=None, supplier: Supplier = None):
        super().__init__(parent)
        self.setWindowTitle("Add Supplier" if supplier is None else "Edit Supplier")
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        
        self.name_edit = QLineEdit()
        self.contact_person_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.email_edit = QLineEdit()
        
        self.layout.addRow("Name:", self.name_edit)
        self.layout.addRow("Contact Person:", self.contact_person_edit)
        self.layout.addRow("Phone:", self.phone_edit)
        self.layout.addRow("Email:", self.email_edit)
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.button_box)
        
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)
        
        if supplier:
            self.name_edit.setText(supplier.name)
            self.contact_person_edit.setText(supplier.contact_person or "")
            self.phone_edit.setText(supplier.phone or "")
            self.email_edit.setText(supplier.email or "")
            self.supplier_id = supplier.supplier_id
        else:
            self.supplier_id = None
    
    def validate_and_accept(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Input Error", "Name cannot be empty.")
            self.name_edit.setFocus()
            return
        # Optional: Add more validations (e.g., valid email format)
        self.accept()
    
    def get_supplier_data(self) -> Supplier:
        return Supplier(
            supplier_id=self.supplier_id,
            name=self.name_edit.text().strip(),
            contact_person=self.contact_person_edit.text().strip() or None,
            phone=self.phone_edit.text().strip() or None,
            email=self.email_edit.text().strip() or None,
            address=None  # Add address field if needed
        )
