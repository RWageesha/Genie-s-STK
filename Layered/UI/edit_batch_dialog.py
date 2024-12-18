# UI/edit_batch_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit,
    QPushButton, QMessageBox, QHBoxLayout, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIntValidator
from domain.domain_models import Batch, Product
from datetime import datetime
from typing import List

class EditBatchDialog(QDialog):
    def __init__(self, batch: Batch, products: List[Product]):
        super().__init__()
        self.setWindowTitle(f"Edit Batch ID {batch.batch_id}")
        self.setFixedSize(400, 350)
        self.batch = batch
        self.products = products
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Product Selection
        product_label = QLabel("Select Product:")
        self.product_combo = QComboBox()
        for product in self.products:
            self.product_combo.addItem(product.name, userData=product.product_id)
            if product.product_id == self.batch.product_id:
                self.product_combo.setCurrentIndex(self.product_combo.count() - 1)
        layout.addWidget(product_label)
        layout.addWidget(self.product_combo)
        
        # Quantity
        quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter quantity")
        self.quantity_input.setValidator(QIntValidator(1, 1000000, self))
        self.quantity_input.setText(str(self.batch.quantity))
        layout.addWidget(quantity_label)
        layout.addWidget(self.quantity_input)
        
        # Manufacture Date
        mfg_label = QLabel("Manufacture Date:")
        self.mfg_input = QDateEdit()
        self.mfg_input.setCalendarPopup(True)
        self.mfg_input.setDate(QDate(self.batch.manufacture_date.year, self.batch.manufacture_date.month, self.batch.manufacture_date.day))
        layout.addWidget(mfg_label)
        layout.addWidget(self.mfg_input)
        
        # Expiry Date
        expiry_label = QLabel("Expiry Date:")
        self.expiry_input = QDateEdit()
        self.expiry_input.setCalendarPopup(True)
        self.expiry_input.setDate(QDate(self.batch.expiry_date.year, self.batch.expiry_date.month, self.batch.expiry_date.day))
        layout.addWidget(expiry_label)
        layout.addWidget(self.expiry_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # Connect buttons
        save_btn.clicked.connect(self.save_changes)
        cancel_btn.clicked.connect(self.reject)
    
    def save_changes(self):
        product_id = self.product_combo.currentData()
        quantity_text = self.quantity_input.text()
        manufacture_date = self.mfg_input.date().toPyDate()
        expiry_date = self.expiry_input.date().toPyDate()
        
        # Validate quantity
        if not quantity_text.isdigit():
            QMessageBox.warning(self, "Input Error", "Quantity must be a number.")
            return
        quantity = int(quantity_text)
        
        if expiry_date <= manufacture_date:
            QMessageBox.warning(self, "Input Error", "Expiry date must be after manufacture date.")
            return
        
        # Update Batch instance
        self.batch.product_id = product_id
        self.batch.quantity = quantity
        self.batch.manufacture_date = manufacture_date
        self.batch.expiry_date = expiry_date
        
        self.accept()
    
    def get_batch_data(self) -> Batch:
        return self.batch
