from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QSpinBox,
    QDoubleSpinBox, QMessageBox, QVBoxLayout, QLabel, QFrame
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from domain.domain_models import Product


class AddProductDialog(QDialog):
    def __init__(self, parent=None, product: Product = None):
        super().__init__(parent)
        self.setWindowTitle("Add Product" if product is None else f"Edit Product: {product.name}")
        self.setFixedWidth(400)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2d;
                color: #ffffff;
                border-radius: 10px;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                color: #ffffff; /* Ensures text is white */
                background-color: transparent; /* Fixes white background issue */
            }
            QLineEdit, QSpinBox, QDoubleSpinBox {
                background-color: #2b2b3c;
                color: #ffffff;
                border: 1px solid #5a5f66;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 1px solid #00adb5;
            }
            QPushButton {
                background-color: #00adb5;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 8px 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #007f8b;
            }
            QDialogButtonBox QPushButton {
                background-color: #00adb5;
                color: #ffffff;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #007f8b;
            }
        """)



        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(15)

        # Header
        header = QLabel("Add Product" if product is None else "Edit Product")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #00adb5;")
        self.main_layout.addWidget(header)

        # Form Layout
        self.form_layout = QFormLayout()
        self.form_layout.setVerticalSpacing(10)
        self.main_layout.addLayout(self.form_layout)

        # Fields
        self.sku_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.category_edit = QLineEdit()
        self.description_edit = QLineEdit()
        self.unit_price_edit = QDoubleSpinBox()
        self.unit_price_edit.setRange(0.01, 1000000.00)
        self.unit_price_edit.setDecimals(2)
        self.unit_price_edit.setSingleStep(0.10)
        self.reorder_level_edit = QSpinBox()
        self.reorder_level_edit.setRange(0, 1000000)

        # Add Fields to Form
        self.form_layout.addRow("SKU:", self.sku_edit)
        self.form_layout.addRow("Name:", self.name_edit)
        self.form_layout.addRow("Category:", self.category_edit)
        self.form_layout.addRow("Description:", self.description_edit)
        self.form_layout.addRow("Unit Price:", self.unit_price_edit)
        self.form_layout.addRow("Reorder Level:", self.reorder_level_edit)

        # Button Box
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Save")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancel")
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(self.button_box)

        # Pre-fill form if editing an existing product
        if product:
            self.sku_edit.setText(product.sku)
            self.sku_edit.setReadOnly(True)  # SKU should be unique and immutable
            self.name_edit.setText(product.name)
            self.category_edit.setText(product.category)
            self.description_edit.setText(product.description or "")
            self.unit_price_edit.setValue(product.unit_price)
            self.reorder_level_edit.setValue(product.reorder_level)
            self.product_id = product.product_id
        else:
            self.product_id = None

    def validate_and_accept(self):
        if not self.sku_edit.text().strip():
            QMessageBox.warning(self, "Input Error", "SKU cannot be empty.")
            self.sku_edit.setFocus()
            return
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Input Error", "Name cannot be empty.")
            self.name_edit.setFocus()
            return
        if not self.category_edit.text().strip():
            QMessageBox.warning(self, "Input Error", "Category cannot be empty.")
            self.category_edit.setFocus()
            return
        self.accept()

    def get_product_data(self) -> Product:
        return Product(
            product_id=self.product_id,
            sku=self.sku_edit.text().strip(),
            name=self.name_edit.text().strip(),
            category=self.category_edit.text().strip(),
            description=self.description_edit.text().strip() or None,
            unit_price=self.unit_price_edit.value(),
            reorder_level=self.reorder_level_edit.value()
        )
