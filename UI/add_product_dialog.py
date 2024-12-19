from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QSpinBox,
    QDoubleSpinBox, QMessageBox, QVBoxLayout, QLabel, QFrame
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
from domain.domain_models import Product


class AddProductDialog(QDialog):
    def __init__(self, parent=None, product: Product = None):
        super().__init__(parent)
        self.setWindowTitle("Add Product" if product is None else f"Edit Product: {product.name}")
        self.setFixedWidth(450)  # Increased width for better spacing
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
            QLineEdit, QSpinBox, QDoubleSpinBox {
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
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
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
                min-width: 100px;
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
        header = QLabel("Add Product" if product is None else "Edit Product")
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
        self.form_layout = QFormLayout()
        self.form_layout.setVerticalSpacing(15)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.form_layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(self.form_layout)

        # Fields
        self.sku_edit = QLineEdit()
        self.sku_edit.setPlaceholderText("Enter SKU")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter Product Name")
        self.category_edit = QLineEdit()
        self.category_edit.setPlaceholderText("Enter Category")
        self.description_edit = QLineEdit()
        self.description_edit.setPlaceholderText("Enter Description")
        self.unit_price_edit = QDoubleSpinBox()
        self.unit_price_edit.setRange(0.01, 1000000.00)
        self.unit_price_edit.setDecimals(2)
        self.unit_price_edit.setSingleStep(0.10)
        self.unit_price_edit.setPrefix("Rs. ")
        self.unit_price_edit.setStyleSheet("padding-right: 20px;")
        self.reorder_level_edit = QSpinBox()
        self.reorder_level_edit.setRange(0, 1000000)
        self.reorder_level_edit.setSuffix(" units")

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
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setFixedHeight(40)
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setFixedHeight(40)
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)

        # Button Layout Adjustment
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.button_box)
        self.main_layout.addLayout(button_layout)

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
