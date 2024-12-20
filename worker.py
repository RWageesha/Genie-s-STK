from PyQt6.QtCore import QThread, pyqtSignal

class DataLoader(QThread):
    finished = pyqtSignal()

    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service

    def run(self):
        # Place your data loading logic here
        self.inventory_service.load_all_data()  # Example method
        self.finished.emit()