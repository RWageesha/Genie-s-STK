import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QListWidget, QMessageBox
)
from PyQt5.QtCore import Qt

from .add_product_dialog import AddProductDialog
from .add_batch_dialog import AddBatchDialog
from .sell_product_dialog import SellProductDialog

class MainWindow(QMainWindow):
    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service
        self.setWindowTitle("Pharmacy Inventory Management")
        
        # Main widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Product list
        self.product_list = QListWidget()
        main_layout.addWidget(self.product_list)
        
        # Load products
        self.load_products()
        
        # Buttons layout
        btn_layout = QHBoxLayout()
        
        self.add_product_btn = QPushButton("Add Product")
        self.add_product_btn.clicked.connect(self.add_product)
        btn_layout.addWidget(self.add_product_btn)
        
        self.add_batch_btn = QPushButton("Add Batch")
        self.add_batch_btn.clicked.connect(self.add_batch)
        btn_layout.addWidget(self.add_batch_btn)
        
        self.sell_product_btn = QPushButton("Sell Product")
        self.sell_product_btn.clicked.connect(self.sell_product)
        btn_layout.addWidget(self.sell_product_btn)

        main_layout.addLayout(btn_layout)
    
    def load_products(self):
        """Load products from the inventory_service into the product_list."""
        self.product_list.clear()
        # Assume inventory_service has all products loaded in memory
        for product in self.inventory_service.inventory.products:
            self.product_list.addItem(f"{product.product_id}: {product.sku} - {product.name}")
    
    def get_selected_product_id(self):
        current_item = self.product_list.currentItem()
        if not current_item:
            return None
        # Format: "product_id: sku - name"
        text = current_item.text()
        product_id_str = text.split(":")[0]
        return int(product_id_str)
    
    def add_product(self):
        dialog = AddProductDialog(self)
        if dialog.exec_() == dialog.Accepted:
            product = dialog.get_product_data()
            try:
                saved_product = self.inventory_service.add_product(product)
                QMessageBox.information(self, "Success", f"Product Added: {saved_product.name}")
                self.load_products()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add product: {e}")
    
    def add_batch(self):
        product_id = self.get_selected_product_id()
        if product_id is None:
            QMessageBox.warning(self, "No Product Selected", "Please select a product first.")
            return
        
        dialog = AddBatchDialog(self)
        if dialog.exec_() == dialog.Accepted:
            batch = dialog.get_batch_data(product_id)
            try:
                saved_batch = self.inventory_service.add_batch(batch)
                QMessageBox.information(self, "Success", f"Batch Added. Quantity: {saved_batch.quantity}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add batch: {e}")
    
    def sell_product(self):
        product_id = self.get_selected_product_id()
        if product_id is None:
            QMessageBox.warning(self, "No Product Selected", "Please select a product first.")
            return
        
        dialog = SellProductDialog(self)
        if dialog.exec_() == dialog.Accepted:
            quantity = dialog.get_quantity()
            try:
                sale_record = self.inventory_service.sell_product(product_id, quantity)
                QMessageBox.information(self, "Success", f"Sale Recorded. Sold {quantity} units.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to sell product: {e}")

def run_app(inventory_service):
    app = QApplication(sys.argv)
    window = MainWindow(inventory_service)
    window.show()
    sys.exit(app.exec_())
