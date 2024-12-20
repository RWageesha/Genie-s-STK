# ui/edit_batch_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QMessageBox, QHBoxLayout, QDateEdit,
    QFormLayout, QFrame, QSpinBox, QDialogButtonBox, QLineEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QIcon
from domain.domain_models import Batch, Product
from typing import List


class EditBatchDialog(QDialog):
    def __init__(self, parent=None, batch: Batch = None, products: List[Product] = None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit Batch ID {batch.batch_id}" if batch else "Edit Batch")
        self.setFixedWidth(500)  # Increased width for better layout
        self.batch = batch
        self.products = products or []
        self.init_ui()

    def init_ui(self):
        # Apply stylesheet for consistent styling
        self.setStyleSheet("""
            QDialog {
                background-color: #2C2C3E;
                color: #E0E0E0;
                border-radius: 12px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 15px;
            }
            QLabel {
                font-size: 16px;
                color: #00ADB5;
                font-weight: bold;
                background-color: transparent;
            }
            QComboBox, QSpinBox, QDateEdit {
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
            QFrame {
                border: 1px solid #555555;
                margin-top: 10px;
                margin-bottom: 10px;
            }
            QLineEdit, QSpinBox {
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
            QLineEdit:focus, QSpinBox:focus, QDateEdit:focus {
                border: 2px solid #00ADB5;
                outline: none;
            }
        """)

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel(f"Edit Batch ID {self.batch.batch_id}" if self.batch else "Edit Batch")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
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
        self.populate_product_combo()
        self.product_combo.setPlaceholderText("Select Product")
        form_layout.addRow("Product:", self.product_combo)

        # Quantity SpinBox
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 1000000)
        self.quantity_spin.setValue(self.batch.quantity if self.batch else 1)
        form_layout.addRow("Quantity:", self.quantity_spin)

        # Manufacture Date
        self.manufacture_date_edit = QDateEdit()
        self.manufacture_date_edit.setCalendarPopup(True)
        self.manufacture_date_edit.setDisplayFormat("yyyy-MM-dd")
        if self.batch:
            self.manufacture_date_edit.setDate(QDate(
                self.batch.manufacture_date.year,
                self.batch.manufacture_date.month,
                self.batch.manufacture_date.day
            ))
        else:
            self.manufacture_date_edit.setDate(QDate.currentDate())
        form_layout.addRow("Manufacture Date:", self.manufacture_date_edit)

        # Expiry Date
        self.expiry_date_edit = QDateEdit()
        self.expiry_date_edit.setCalendarPopup(True)
        self.expiry_date_edit.setDisplayFormat("yyyy-MM-dd")
        if self.batch:
            self.expiry_date_edit.setDate(QDate(
                self.batch.expiry_date.year,
                self.batch.expiry_date.month,
                self.batch.expiry_date.day
            ))
        else:
            self.expiry_date_edit.setDate(QDate.currentDate().addDays(365))
        form_layout.addRow("Expiry Date:", self.expiry_date_edit)

        # Dialog Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Update Batch")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancel")
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setFixedHeight(40)
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setFixedHeight(40)
        self.main_layout.addWidget(self.button_box)

        # Connect buttons
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)

        # Pre-fill form with existing batch data
        if self.batch:
            product = next((p for p in self.products if p.product_id == self.batch.product_id), None)
            if product:
                index = self.product_combo.findData(product.product_id)
                if index != -1:
                    self.product_combo.setCurrentIndex(index)

    def populate_product_combo(self):
        """
        Populates the product_combo with product names and sets the product_id as user data.
        """
        self.product_combo.clear()
        for product in self.products:
            self.product_combo.addItem(product.name, product.product_id)
        if not self.products:
            self.product_combo.setEnabled(False)
            QMessageBox.warning(self, "No Products", "No products available to select.")

    def validate_and_accept(self):
        product_id = self.product_combo.currentData()
        product_name = self.product_combo.currentText().strip()
        quantity = self.quantity_spin.value()
        manufacture_date = self.manufacture_date_edit.date().toPyDate()
        expiry_date = self.expiry_date_edit.date().toPyDate()

        # Validate product selection
        if not product_name:
            QMessageBox.warning(self, "Input Error", "Please select a product.")
            self.product_combo.setFocus()
            return

        # Validate quantity
        if quantity <= 0:
            QMessageBox.warning(self, "Input Error", "Quantity must be greater than zero.")
            self.quantity_spin.setFocus()
            return

        # Validate dates
        if expiry_date <= manufacture_date:
            QMessageBox.warning(self, "Input Error", "Expiry date must be after manufacture date.")
            self.expiry_date_edit.setFocus()
            return

        self.accept()

    def get_batch_data(self) -> Batch:
        """
        Retrieve the updated batch data from the dialog.
        """
        product_id = self.product_combo.currentData()
        quantity = self.quantity_spin.value()
        manufacture_date = self.manufacture_date_edit.date().toPyDate()
        expiry_date = self.expiry_date_edit.date().toPyDate()

        return Batch(
            batch_id=self.batch.batch_id if self.batch else None,
            product_id=product_id,
            quantity=quantity,
            manufacture_date=manufacture_date,
            expiry_date=expiry_date
        )