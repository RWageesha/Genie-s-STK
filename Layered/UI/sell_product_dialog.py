from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QSpinBox

class SellProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sell Product")
        
        layout = QFormLayout(self)
        
        self.quantity_edit = QSpinBox()
        self.quantity_edit.setRange(1, 999999)
        layout.addRow("Quantity to Sell:", self.quantity_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
    
    def get_quantity(self) -> int:
        return self.quantity_edit.value()
