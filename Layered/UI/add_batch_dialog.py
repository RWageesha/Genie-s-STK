from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QSpinBox, QDateEdit
from PyQt5.QtCore import QDate
from domain.domain_models import Batch

class AddBatchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Batch")
        
        layout = QFormLayout(self)
        
        self.quantity_edit = QSpinBox()
        self.quantity_edit.setRange(1, 999999)
        layout.addRow("Quantity:", self.quantity_edit)
        
        self.manufacture_date_edit = QDateEdit(QDate.currentDate())
        self.manufacture_date_edit.setCalendarPopup(True)
        layout.addRow("Manufacture Date:", self.manufacture_date_edit)
        
        self.expiry_date_edit = QDateEdit(QDate.currentDate().addDays(365))
        self.expiry_date_edit.setCalendarPopup(True)
        layout.addRow("Expiry Date:", self.expiry_date_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
    
    def get_batch_data(self, product_id: int) -> Batch:
        return Batch(
            batch_id=None,
            product_id=product_id,
            quantity=self.quantity_edit.value(),
            manufacture_date=self.manufacture_date_edit.date().toPyDate(),
            expiry_date=self.expiry_date_edit.date().toPyDate()
        )
