# UI/batches_management.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDialog
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from .edit_batch_dialog import EditBatchDialog  # Ensure correct import
from .add_batch_dialog import AddBatchDialog      # Ensure AddBatchDialog is imported

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
        self.refresh_data_btn = QPushButton("Refresh")  # New Refresh button
        
        self.add_batch_btn.clicked.connect(self.add_batch)
        self.edit_batch_btn.clicked.connect(self.edit_batch)
        self.delete_batch_btn.clicked.connect(self.delete_batch)
        self.refresh_data_btn.clicked.connect(self.refresh_data)  # Connect to a new method
        
        btn_layout.addWidget(self.add_batch_btn)
        btn_layout.addWidget(self.edit_batch_btn)
        btn_layout.addWidget(self.delete_batch_btn)
        btn_layout.addWidget(self.refresh_data_btn)  # Add Refresh button to layout
        btn_layout.addStretch()
        
        self.layout.addLayout(btn_layout)
        
        # Batches table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Batch ID", "Product ID", "Quantity", "Manufacture Date", "Expiry Date"
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.table)
        
        self.load_batches()
        self.apply_styles()

    def apply_styles(self):
        self.setFont(QFont("Roboto", 14))
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2d;
                color: #c4c4c4;
                font-family: "Roboto";
            }

            QPushButton {
                background-color: #00adb5;
                color: #ffffff;
                border-radius: 5px;
                padding: 8px 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #007f8b;
            }

            QTableWidget {
                background-color: #1e1e2d;
                gridline-color: #5a5f66;
                border: 1px solid #5a5f66;
                font-size: 14px;
            }

            QTableWidget::item {
                color: #ffffff;
            }

            QTableWidget::item:selected {
                background-color: #323544;
            }

            QHeaderView::section {
                background-color: #2b2b3c;
                color: #ffffff;
                font-weight: bold;
                border: none;
                padding: 4px;
            }

            QMessageBox {
                background-color: #1e1e2d;
                color: #c4c4c4;
            }
        """)

    def load_batches(self):
        self.table.setRowCount(0)
        batches = self.inventory_service.get_all_batches()
        for batch in batches:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(batch.batch_id)))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(batch.product_id)))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(batch.quantity)))
            self.table.setItem(row_position, 3, QTableWidgetItem(batch.manufacture_date.strftime("%Y-%m-%d")))
            self.table.setItem(row_position, 4, QTableWidgetItem(batch.expiry_date.strftime("%Y-%m-%d")))
        self.table.resizeColumnsToContents()
    
    def add_batch(self):
        dialog = AddBatchDialog(self, self.inventory_service.get_all_products())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            batch = dialog.get_batch_data()
            try:
                self.inventory_service.add_batch(batch)
                QMessageBox.information(self, "Success", f"Batch ID {batch.batch_id} added successfully.")
                self.load_batches()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add batch: {e}")
    
    def edit_batch(self):
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
            QMessageBox.critical(self, "Error", "Selected batch not found.")
            return
        # Corrected instantiation: pass self as parent
        dialog = EditBatchDialog(self, batch, self.inventory_service.get_all_products())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_batch = dialog.get_batch_data()
            try:
                self.inventory_service.update_batch(updated_batch)
                QMessageBox.information(self, "Success", f"Batch ID {updated_batch.batch_id} updated successfully.")
                self.load_batches()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update batch: {e}")
    
    def delete_batch(self):
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
                QMessageBox.critical(self, "Error", f"Failed to delete batch: {e}")
    
    def refresh_data(self):
        self.load_batches()
        QMessageBox.information(self, "Refreshed", "Batch data has been refreshed.")