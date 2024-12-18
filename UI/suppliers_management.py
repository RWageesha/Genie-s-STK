# ui/suppliers_management.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt

from .add_supplier_dialog import AddSupplierDialog

class SuppliersManagement(QWidget):
    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Top buttons
        btn_layout = QHBoxLayout()
        self.add_supplier_btn = QPushButton("Add Supplier")
        self.edit_supplier_btn = QPushButton("Edit Supplier")
        self.delete_supplier_btn = QPushButton("Delete Supplier")
        
        self.add_supplier_btn.clicked.connect(self.add_supplier)
        self.edit_supplier_btn.clicked.connect(self.edit_supplier)
        self.delete_supplier_btn.clicked.connect(self.delete_supplier)
        
        btn_layout.addWidget(self.add_supplier_btn)
        btn_layout.addWidget(self.edit_supplier_btn)
        btn_layout.addWidget(self.delete_supplier_btn)
        btn_layout.addStretch()
        
        self.layout.addLayout(btn_layout)
        
        # Suppliers table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Supplier ID", "Name", "Contact Person", "Phone", "Email"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.table)
        
        self.load_suppliers()
    
    def load_suppliers(self):
        self.table.setRowCount(0)
        suppliers = self.inventory_service.get_all_suppliers()
        for supplier in suppliers:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(supplier.supplier_id)))
            self.table.setItem(row_position, 1, QTableWidgetItem(supplier.name))
            self.table.setItem(row_position, 2, QTableWidgetItem(supplier.contact_person or ""))
            self.table.setItem(row_position, 3, QTableWidgetItem(supplier.phone or ""))
            self.table.setItem(row_position, 4, QTableWidgetItem(supplier.email or ""))
        self.table.resizeColumnsToContents()
    
    def add_supplier(self):
        dialog = AddSupplierDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            supplier = dialog.get_supplier_data()
            try:
                self.inventory_service.add_supplier(supplier)
                QMessageBox.information(self, "Success", f"Supplier '{supplier.name}' added successfully.")
                self.load_suppliers()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add supplier: {e}")
    
    def edit_supplier(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a supplier to edit.")
            return
        row = selected_items[0].row()
        supplier_id = int(self.table.item(row, 0).text())
        supplier = self.inventory_service.get_supplier_by_id(supplier_id)
        if not supplier:
            QMessageBox.critical(self, "Error", "Selected supplier not found.")
            return
        dialog = AddSupplierDialog(self, supplier)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_supplier = dialog.get_supplier_data()
            try:
                self.inventory_service.update_supplier(updated_supplier)
                QMessageBox.information(self, "Success", f"Supplier '{updated_supplier.name}' updated successfully.")
                self.load_suppliers()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update supplier: {e}")
    
    def delete_supplier(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a supplier to delete.")
            return
        row = selected_items[0].row()
        supplier_id = int(self.table.item(row, 0).text())
        supplier = self.inventory_service.get_supplier_by_id(supplier_id)
        if not supplier:
            QMessageBox.critical(self, "Error", "Selected supplier not found.")
            return
        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f"Are you sure you want to delete supplier '{supplier.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.inventory_service.delete_supplier(supplier_id)
                QMessageBox.information(self, "Success", f"Supplier '{supplier.name}' deleted successfully.")
                self.load_suppliers()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete supplier: {e}")