# run_ui.py

from data.sqlalchemy_repositories import (
    SQLAlchemyProductRepository,
    SQLAlchemyBatchRepository,
    SQLAlchemySaleRecordRepository,
    SQLAlchemySupplierRepository,
    SQLAlchemyOrderRepository
)
from services.inventory_service import InventoryService

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
    inventory_service = setup_inventory_service()
    from UI.main_window import run_app
    run_app(inventory_service)

if __name__ == "__main__":
    main()