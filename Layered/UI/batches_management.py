# ui/batches_management.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt

from .add_batch_dialog import AddBatchDialog

class BatchesManagement(QWidget):
    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Top buttons
        btn_layout = QHBoxLayout()
        self.add_batch_btn = QPushButton("Add Batch")
        self.edit_batch_btn = QPushButton("Edit Batch")
        self.delete_batch_btn = QPushButton("Delete Batch")
        
        self.add_batch_btn.clicked.connect(self.add_batch)
        self.edit_batch_btn.clicked.connect(self.edit_batch)
        self.delete_batch_btn.clicked.connect(self.delete_batch)
        
        btn_layout.addWidget(self.add_batch_btn)
        btn_layout.addWidget(self.edit_batch_btn)
        btn_layout.addWidget(self.delete_batch_btn)
        btn_layout.addStretch()
        
        self.layout.addLayout(btn_layout)
        
        # Batches table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Batch ID", "Product", "Quantity", "Manufacture Date", "Expiry Date"
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.table)
        
        self.load_batches()
    
    def load_batches(self):
        self.table.setRowCount(0)
        batches = self.inventory_service.get_all_batches()
        for batch in batches:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(batch.batch_id)))
            self.table.setItem(row_position, 1, QTableWidgetItem(batch.product.name if batch.product else ""))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(batch.quantity)))
            self.table.setItem(row_position, 3, QTableWidgetItem(batch.manufacture_date.strftime("%Y-%m-%d")))
            self.table.setItem(row_position, 4, QTableWidgetItem(batch.expiry_date.strftime("%Y-%m-%d")))
        self.table.resizeColumnsToContents()
    
    def add_batch(self):
        dialog = AddBatchDialog(self, self.inventory_service)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            batch = dialog.get_batch_data()
            try:
                self.inventory_service.add_batch(batch)
                QMessageBox.information(self, "Success", f"Batch ID {batch.batch_id} added successfully.")
                self.load_batches()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add batch: {e}")
    
    def edit_batch(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a batch to edit.")
            return
        row = selected_items[0].row()
        batch_id = int(self.table.item(row, 0).text())
        batch = self.inventory_service.get_batch_by_id(batch_id)
        if not batch:
            QMessageBox.critical(self, "Error", "Selected batch not found.")
            return
        dialog = AddBatchDialog(self, self.inventory_service, batch)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_batch = dialog.get_batch_data()
            try:
                self.inventory_service.update_batch(updated_batch)
                QMessageBox.information(self, "Success", f"Batch ID {updated_batch.batch_id} updated successfully.")
                self.load_batches()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update batch: {e}")
    
    def delete_batch(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a batch to delete.")
            return
        row = selected_items[0].row()
        batch_id = int(self.table.item(row, 0).text())
        batch = self.inventory_service.get_batch_by_id(batch_id)
        if not batch:
            QMessageBox.critical(self, "Error", "Selected batch not found.")
            return
        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f"Are you sure you want to delete Batch ID {batch.batch_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.inventory_service.delete_batch(batch_id)
                QMessageBox.information(self, "Success", f"Batch ID {batch_id} deleted successfully.")
                self.load_batches()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete batch: {e}")
