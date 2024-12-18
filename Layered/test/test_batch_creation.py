# tests/test_batch_management.py

import unittest
from unittest.mock import MagicMock
from domain.domain_models import Batch
from data.sqlalchemy_repositories import SQLAlchemyBatchRepository
from services.inventory_service import InventoryService
from datetime import date

class TestBatchManagement(unittest.TestCase):
    def setUp(self):
        # Setup mock repositories
        self.mock_product_repo = MagicMock()
        self.mock_batch_repo = MagicMock()
        self.mock_sale_repo = MagicMock()
        self.mock_supplier_repo = MagicMock()
        self.mock_order_repo = MagicMock()

        # Initialize InventoryService with mocks
        self.inventory_service = InventoryService(
            product_repo=self.mock_product_repo,
            batch_repo=self.mock_batch_repo,
            sale_repo=self.mock_sale_repo,
            supplier_repo=self.mock_supplier_repo,
            order_repo=self.mock_order_repo
        )
    
    def test_add_batch_success(self):
        # Create a sample batch
        batch = Batch(
            batch_id=None,
            product_id=1,
            quantity=100,
            manufacture_date=date(2024, 1, 1),
            expiry_date=date(2025, 1, 1)
        )

        # Configure the mock to return the batch with an ID
        self.mock_batch_repo.add_batch.return_value = Batch(
            batch_id=1,
            product_id=1,
            quantity=100,
            manufacture_date=date(2024, 1, 1),
            expiry_date=date(2025, 1, 1)
        )

        # Call add_batch
        result = self.inventory_service.add_batch(batch)

        # Assertions
        self.mock_batch_repo.add_batch.assert_called_once_with(batch)
        self.assertEqual(result.batch_id, 1)
        self.assertEqual(result.product_id, 1)
        self.assertEqual(result.quantity, 100)

if __name__ == "__main__":
    unittest.main()
