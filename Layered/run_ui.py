# run_ui.py

from data.db_config import init_db, SessionLocal
from data.sqlalchemy_repositories import (
    SQLAlchemyProductRepository,
    SQLAlchemyBatchRepository,
    SQLAlchemySaleRecordRepository
)
from services.inventory_service import InventoryService
from UI.main_window import run_app  # The function we defined in main_window.py

def setup_inventory_service():
    # Initialize DB
    init_db()

    session = SessionLocal()
    product_repo = SQLAlchemyProductRepository(session)
    batch_repo = SQLAlchemyBatchRepository(session)
    sale_repo = SQLAlchemySaleRecordRepository(session)

    inventory_service = InventoryService(
        product_repo=product_repo,
        batch_repo=batch_repo,
        sale_repo=sale_repo
    )
    return inventory_service

if __name__ == "__main__":
    inventory_service = setup_inventory_service()
    run_app(inventory_service)
