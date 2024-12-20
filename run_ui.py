# run_ui.py

import sys
from data.sqlalchemy_repositories import (
    SQLAlchemyProductRepository,
    SQLAlchemyBatchRepository,
    SQLAlchemySaleRecordRepository,
    SQLAlchemySupplierRepository,
    SQLAlchemyOrderRepository
)
from services.inventory_service import InventoryService
from PyQt5.QtWidgets import QApplication

def setup_inventory_service() -> InventoryService:
    product_repo = SQLAlchemyProductRepository()
    batch_repo = SQLAlchemyBatchRepository()
    sale_repo = SQLAlchemySaleRecordRepository()
    supplier_repo = SQLAlchemySupplierRepository()
    order_repo = SQLAlchemyOrderRepository()
    
    inventory_service = InventoryService(
        product_repo=product_repo,
        batch_repo=batch_repo,
        sale_repo=sale_repo,
        supplier_repo=supplier_repo,
        order_repo=order_repo
    )
    
    return inventory_service

def main():
    from login_window import LoginWindow
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()