# UI/batches_management.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QHBoxLayout, QHeaderView  # Import QHeaderView
)
from PyQt6.QtCore import Qt
from .add_batch_dialog import AddBatchDialog
from .edit_batch_dialog import EditBatchDialog  # Ensure this dialog exists
from domain.domain_models import Batch, Product
from typing import List, Optional

class BatchesManagement(QWidget):
    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Buttons Layout
        buttons_layout = QHBoxLayout()
        
        # Add Batch Button
        add_button = QPushButton("Add Batch")
        add_button.clicked.connect(self.add_batch)
        buttons_layout.addWidget(add_button)
        
        # Edit Batch Button
        edit_button = QPushButton("Edit Batch")
        edit_button.clicked.connect(self.edit_batch)
        buttons_layout.addWidget(edit_button)
        
        # Delete Batch Button
        delete_button = QPushButton("Delete Batch")
        delete_button.clicked.connect(self.delete_batch)
        buttons_layout.addWidget(delete_button)
        
        # Refresh Button
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.load_batches)
        buttons_layout.addWidget(refresh_button)
        
        layout.addLayout(buttons_layout)
        
        # Batches Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Batch ID", "Product ID", "Quantity",
            "Manufacture Date", "Expiry Date"
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Updated line
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        self.load_batches()
    
    def load_batches(self):
        """
        Loads all batches from the inventory service and displays them in the table.
        """
        try:
            batches = self.inventory_service.get_all_batches()
            self.table.setRowCount(len(batches))
            for row, batch in enumerate(batches):
                self.table.setItem(row, 0, QTableWidgetItem(str(batch.batch_id)))
                self.table.setItem(row, 1, QTableWidgetItem(str(batch.product_id)))
                self.table.setItem(row, 2, QTableWidgetItem(str(batch.quantity)))
                self.table.setItem(row, 3, QTableWidgetItem(batch.manufacture_date.strftime("%Y-%m-%d")))
                self.table.setItem(row, 4, QTableWidgetItem(batch.expiry_date.strftime("%Y-%m-%d")))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load batches: {str(e)}")
    
    def add_batch(self):
        """
        Opens the AddBatchDialog to collect batch details and adds the batch upon successful input.
        """
        products = self.inventory_service.get_all_products()
        if not products:
            QMessageBox.warning(self, "No Products", "No products available. Please add products first.")
            return
        
        dialog = AddBatchDialog(products)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            batch = dialog.get_batch_data()
            try:
                self.inventory_service.add_batch(batch)
                QMessageBox.information(self, "Success", "Batch added successfully.")
                self.load_batches()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add batch: {str(e)}")
    
    def edit_batch(self):
        """
        Opens the EditBatchDialog to modify the selected batch's details.
        """
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a batch to edit.")
            return
        
        batch_id_item = self.table.item(selected_row, 0)
        if not batch_id_item:
            QMessageBox.warning(self, "Error", "Failed to retrieve selected batch ID.")
            return
        
        batch_id = int(batch_id_item.text())
        batch = self.inventory_service.get_batch_by_id(batch_id)
        if not batch:
            QMessageBox.warning(self, "Error", "Selected batch not found.")
            return
        
        dialog = EditBatchDialog(batch, self.inventory_service.get_all_products())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_batch = dialog.get_batch_data()
            try:
                self.inventory_service.update_batch(updated_batch)
                QMessageBox.information(self, "Success", "Batch updated successfully.")
                self.load_batches()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update batch: {str(e)}")
    
    def delete_batch(self):
        """
        Deletes the selected batch after confirmation.
        """
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a batch to delete.")
            return
        
        batch_id_item = self.table.item(selected_row, 0)
        if not batch_id_item:
            QMessageBox.warning(self, "Error", "Failed to retrieve selected batch ID.")
            return
        
        batch_id = int(batch_id_item.text())
        
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete Batch ID {batch_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.inventory_service.delete_batch(batch_id)
                QMessageBox.information(self, "Success", "Batch deleted successfully.")
                self.load_batches()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete batch: {str(e)}")
