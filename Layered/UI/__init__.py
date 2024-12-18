# ui/__init__.py

from .main_window import ModernSidebarUI, run_app
from .add_product_dialog import AddProductDialog
from .add_batch_dialog import AddBatchDialog
from .sell_product_dialog import SellProductDialog
from .suppliers_management import SuppliersManagement
from .add_supplier_dialog import AddSupplierDialog
from .orders_management import OrdersManagement
from .add_order_dialog import AddOrderDialog
from .reports import Reports
from .settings import Settings

__all__ = [
    'ModernSidebarUI',
    'run_app',
    'AddProductDialog',
    'AddBatchDialog',
    'SellProductDialog',
    'SuppliersManagement',
    'AddSupplierDialog',
    'OrdersManagement',
    'AddOrderDialog',
    'Reports',
    'Settings'
]
