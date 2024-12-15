from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox

from domain.domain_models import Product

class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Product")
        
        layout = QFormLayout(self)
        
        self.sku_edit = QLineEdit()
        layout.addRow("SKU:", self.sku_edit)
        
        self.name_edit = QLineEdit()
        layout.addRow("Name:", self.name_edit)
        
        self.category_edit = QLineEdit()
        layout.addRow("Category:", self.category_edit)
        
        self.description_edit = QLineEdit()
        layout.addRow("Description:", self.description_edit)
        
        self.unit_price_edit = QDoubleSpinBox()
        self.unit_price_edit.setRange(0, 999999.99)
        self.unit_price_edit.setDecimals(2)
        layout.addRow("Unit Price:", self.unit_price_edit)
        
        self.reorder_level_edit = QSpinBox()
        self.reorder_level_edit.setRange(0, 999999)
        layout.addRow("Reorder Level:", self.reorder_level_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
    
    def get_product_data(self) -> Product:
        return Product(
            product_id=None,
            sku=self.sku_edit.text().strip(),
            name=self.name_edit.text().strip(),
            category=self.category_edit.text().strip(),
            description=self.description_edit.text().strip() or None,
            unit_price=self.unit_price_edit.value(),
            reorder_level=self.reorder_level_edit.value()
        )
