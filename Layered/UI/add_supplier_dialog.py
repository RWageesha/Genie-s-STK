# ui/add_supplier_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QMessageBox,
    QVBoxLayout, QLabel, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from domain.domain_models import Supplier


class AddSupplierDialog(QDialog):
    def __init__(self, parent=None, supplier: Supplier = None):
        super().__init__(parent)
        self.setWindowTitle("Add Supplier" if supplier is None else "Edit Supplier")
        self.setFixedWidth(500)  # Increased width for better layout
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
            QLineEdit {
                background-color: #3A3A4D;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 8px;
                font-size: 15px;
            }
            QLineEdit::placeholder {
                color: #B0B0B0;
            }
            QLineEdit:focus {
                border: 2px solid #00ADB5;
                outline: none;
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
        header = QLabel("Add Supplier" if supplier is None else "Edit Supplier")
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

        # Name Field
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter Supplier Name")
        form_layout.addRow("Name:", self.name_edit)

        # Contact Person Field
        self.contact_person_edit = QLineEdit()
        self.contact_person_edit.setPlaceholderText("Enter Contact Person")
        form_layout.addRow("Contact Person:", self.contact_person_edit)

        # Phone Field
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("Enter Phone Number")
        form_layout.addRow("Phone:", self.phone_edit)

        # Email Field
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Enter Email Address")
        form_layout.addRow("Email:", self.email_edit)

        # Dialog Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Save Supplier")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancel")
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setFixedHeight(40)
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setFixedHeight(40)
        self.main_layout.addWidget(self.button_box)

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
        if self.email_edit.text().strip() and not self.validate_email(self.email_edit.text().strip()):
            QMessageBox.warning(self, "Input Error", "Please enter a valid email address.")
            self.email_edit.setFocus()
            return
        # Optional: Add more validations (e.g., phone number format)
        self.accept()

    def validate_email(self, email: str) -> bool:
        import re
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_regex, email) is not None

    def get_supplier_data(self) -> Supplier:
        return Supplier(
            supplier_id=self.supplier_id,
            name=self.name_edit.text().strip(),
            contact_person=self.contact_person_edit.text().strip() or None,
            phone=self.phone_edit.text().strip() or None,
            email=self.email_edit.text().strip() or None,
            address=None  # Add address field if needed
        )
