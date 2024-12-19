# UI/add_batch_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, 
    QPushButton, QMessageBox, QHBoxLayout, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIntValidator, QFont
from domain.domain_models import Batch

class AddBatchDialog(QDialog):
    def __init__(self, products):
        super().__init__()
        self.setWindowTitle("Add Batch")
        self.setFixedSize(450, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #1f1f2e;
                border-radius: 10px;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
                margin-bottom: 5px;
            }
            QComboBox, QLineEdit, QDateEdit {
                background-color: #2b2b3c;
                color: #ffffff;
                border: 1px solid #5a5f66;
                border-radius: 5px;
                padding: 6px;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                background-color: #2b2b3c;
                selection-background-color: #00adb5;
                color: #ffffff;
            }
            QPushButton {
                background-color: #00adb5;
                color: #ffffff;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #007f8b;
            }
            QPushButton:pressed {
                background-color: #006f7a;
            }
        """)
        self.products = products  # List of Product objects
        self.batch = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Header
        header_label = QLabel("Add New Batch")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #00adb5; margin-bottom: 10px;")
        layout.addWidget(header_label)

        # Product Selection
        product_label = QLabel("Select Product:")
        self.product_combo = QComboBox()
        for product in self.products:
            self.product_combo.addItem(product.name, userData=product.product_id)
        layout.addWidget(product_label)
        layout.addWidget(self.product_combo)

        # Quantity Input
        quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter quantity")
        self.quantity_input.setValidator(QIntValidator(1, 1000000, self))
        layout.addWidget(quantity_label)
        layout.addWidget(self.quantity_input)

        # Manufacture Date
        mfg_label = QLabel("Manufacture Date:")
        self.mfg_input = QDateEdit()
        self.mfg_input.setCalendarPopup(True)
        self.mfg_input.setDate(QDate.currentDate())
        layout.addWidget(mfg_label)
        layout.addWidget(self.mfg_input)

        # Expiry Date
        expiry_label = QLabel("Expiry Date:")
        self.expiry_input = QDateEdit()
        self.expiry_input.setCalendarPopup(True)
        self.expiry_input.setDate(QDate.currentDate().addYears(1))
        layout.addWidget(expiry_label)
        layout.addWidget(self.expiry_input)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        self.add_btn = QPushButton("Add")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addStretch()
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Button Connections
        self.add_btn.clicked.connect(self.add_batch)
        self.cancel_btn.clicked.connect(self.reject)

    def add_batch(self):
        product_id = self.product_combo.currentData()
        quantity_text = self.quantity_input.text()
        manufacture_date = self.mfg_input.date().toPyDate()
        expiry_date = self.expiry_input.date().toPyDate()

        # Validate Quantity
        if not quantity_text.isdigit():
            QMessageBox.warning(self, "Input Error", "Quantity must be a number.")
            return
        quantity = int(quantity_text)

        if expiry_date <= manufacture_date:
            QMessageBox.warning(self, "Input Error", "Expiry date must be after manufacture date.")
            return

        # Create Batch Instance
        self.batch = Batch(
            batch_id=None,
            product_id=product_id,
            quantity=quantity,
            manufacture_date=manufacture_date,
            expiry_date=expiry_date
        )
        self.accept()

    def get_batch_data(self):
        return self.batch
