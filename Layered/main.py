from datetime import date
from data.db_config import init_db, SessionLocal
from data.sqlalchemy_repositories import SQLAlchemyProductRepository, SQLAlchemyBatchRepository, SQLAlchemySaleRecordRepository
from domain.domain_models import Batch, Product
from services.inventory_service import InventoryService

def main():
    # Initialize the database (create tables)
    init_db()

    # Create a new session
    session = SessionLocal()

    try:
        # Initialize repositories
        product_repo = SQLAlchemyProductRepository(session)
        batch_repo = SQLAlchemyBatchRepository(session)
        sale_repo = SQLAlchemySaleRecordRepository(session)

        # Initialize the InventoryService with repositories
        inventory_service = InventoryService(
            product_repo=product_repo,
            batch_repo=batch_repo,
            sale_repo=sale_repo
        )

        # Example usage:
        # Add a new product
        new_product = Product(
            product_id=None,  # Will be set by the repository
            sku="P001",
            name="Paracetamol",
            category="Painkiller",
            description="Used to treat pain and fever",
            unit_price=0.10,
            reorder_level=100
        )
        saved_product = inventory_service.add_product(new_product)
        print(f"Added Product: {saved_product}")

        # Add a batch for the product
        new_batch = Batch(
            batch_id=None,  # Will be set by the repository
            product_id=saved_product.product_id,
            quantity=500,
            manufacture_date=date(2024, 1, 1),
            expiry_date=date(2025, 1, 1)
        )
        saved_batch = inventory_service.add_batch(new_batch)
        print(f"Added Batch: {saved_batch}")

        # Sell some product
        sale_record = inventory_service.sell_product(product_id=saved_product.product_id, quantity=50)
        print(f"Recorded Sale: {sale_record}")

    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()
