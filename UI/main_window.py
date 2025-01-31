import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFrame, QStackedWidget, QLabel, QDialog, QMessageBox, QButtonGroup
)
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSignal
from PyQt6.QtSvg import QSvgRenderer  # Corrected import

from .products_management import ProductsManagement
from .batches_management import BatchesManagement
from .sales_management import SalesManagement
from .suppliers_management import SuppliersManagement
from .orders_management import OrdersManagement
from .reports import Reports
from backup import fetch_data, convert_data_to_dict, save_to_json
from restore import restore_data_from_json
from .settings import Settings  # Ensure this module exists and is correctly implemented
from .sell_product_widget import SellProductWidget  # Import the SellProductWidget

def load_white_icon(svg_path, size=QSize(20, 20)):
    """
    Loads an SVG icon, renders it to a pixmap, and recolors it to white.
    
    :param svg_path: Path to the SVG file.
    :param size: Desired size of the icon.
    :return: QIcon with white color.
    """
    renderer = QSvgRenderer(svg_path)
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    # Convert pixmap to QImage and recolor
    image = pixmap.toImage()
    width, height = image.width(), image.height()
    for x in range(width):
        for y in range(height):
            pixel = image.pixelColor(x, y)
            # If pixel is non-transparent, set it to white
            if pixel.alpha() > 0:
                image.setPixelColor(x, y, QColor("#ffffff"))

    # Convert the recolored image back to pixmap and then to QIcon
    pixmap = QPixmap.fromImage(image)
    return QIcon(pixmap)

class ContactDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contact Us")
        self.setFixedSize(450, 300)

        # Apply modern style
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2d; 
                border-radius: 10px;
                color: #c4c4c4;
                font-family: "Roboto", Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #ffffff;
                padding: 10px;
            }
            QLabel#title {
                font-size: 18px;
                font-weight: bold;
                color: #00adb5;
            }
            QLabel#footer {
                font-size: 12px;
                color: #5a5f66;
                padding: 10px;
            }
        """)

        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title_label = QLabel("Contact Us")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Roboto", 18, QFont.Weight.Bold))

        # Contact Information
        contact_info = QLabel(
            "For support, reach out to us:\n\n"
            "📧 Email: teamclaptac@gmail.com\n"
            "📞 Phone: +94 71 848 33 55\n"
            "🏢 Address: Claptac Inc\n"
            "Sri Lanka"
        )
        contact_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contact_info.setWordWrap(True)

        # Footer
        footer_label = QLabel("We are here to help you 24/7.")
        footer_label.setObjectName("footer")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(contact_info)
        layout.addStretch()
        layout.addWidget(footer_label)

        self.setLayout(layout)

from UI.loading_dialog import LoadingDialog
from worker import DataLoader

class ModernSidebarUI(QMainWindow):
    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service
        self.setWindowTitle("Pharmacy Inventory Management")
        self.setGeometry(100, 100, 1200, 700)

        # Initialize Loading Dialog
        self.loading_dialog = LoadingDialog()
        self.loading_dialog.show()

        # Initialize and start the worker thread
        self.worker = DataLoader(self.inventory_service)
        self.worker.finished.connect(self.on_data_loaded)
        self.worker.start()

        # Central Widget
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #f4f4f4;")
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1e1e2d;
                border-right: 0.5px solid #2b2b3c;
            }
            QPushButton {
                background-color: transparent;
                color: #ffffff;
                text-align: left;
                padding: 10px 20px;
                border: none;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2b2b3c;
                border-left: 2px solid #00adb5;
                color: #00adb5;
            }
            QPushButton:checked {
                background-color: #2b2b3c;
                border-left: 2px solid #00adb5;
                color: #00adb5;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(10)

        # Initialize Navigational Buttons
        self.nav_buttons = {}
        self.init_sidebar_buttons(sidebar_layout)

        # Spacer to push items to the bottom
        sidebar_layout.addStretch()

        # Initialize Bottom Action Buttons
        self.init_bottom_buttons(sidebar_layout)

        # Add Sidebar to Main Layout
        main_layout.addWidget(sidebar)

        # Main Content Area
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("""
            QStackedWidget {
                background-color: #1e1e2d;
            }
        """)

        # Initialize Modules
        self.init_modules()

        # Add Stacked Widget to Main Layout
        main_layout.addWidget(self.stack)

        # Connect Buttons to Slots
        self.connect_buttons()

        # Set Home as the default selected button
        self.nav_buttons["Home"].setChecked(True)
        self.stack.setCurrentIndex(0)

        # Initialize and start the auto backup timer
        self.init_auto_backup()

    def on_data_loaded(self):
        self.loading_dialog.close()

    def init_sidebar_buttons(self, layout):
        # Define button labels and corresponding icon paths
        button_info = [
            ("Home", "icons/home.svg"),
            ("Product Management", "icons/product.svg"),
            ("Batch Management", "icons/batch.svg"),
            ("Sales Management", "icons/sales.svg"),
            ("Reports", "icons/reports.svg"),
            ("Backup", "icons/backup.svg"),      # Added Backup button
            ("Restore", "icons/restore.svg"),    # Added Restore button
        ]

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for label, icon_path in button_info:
            btn = QPushButton(f"  {label}")
            btn.setFixedHeight(40)
            btn.setIcon(load_white_icon(icon_path))
            btn.setIconSize(QSize(20, 20))
            if label in ["Backup", "Restore"]:
                btn.setCheckable(False)  # Make Backup and Restore non-checkable
            else:
                btn.setCheckable(True)
                self.button_group.addButton(btn)
            btn.setStyleSheet("QPushButton { text-align: left; }")
            layout.addWidget(btn)
            self.nav_buttons[label] = btn

    def init_bottom_buttons(self, layout):
        # Define bottom button labels and icon paths
        bottom_button_info = [
            ("Settings", "icons/settings.svg"),
            ("Contact", "icons/contact.svg"),
            ("Log Out", "icons/logout.svg"),  # Added Log Out button
        ]

        for label, icon_path in bottom_button_info:
            btn = QPushButton(f"  {label}")
            btn.setFixedHeight(40)
            btn.setIcon(load_white_icon(icon_path))
            btn.setIconSize(QSize(20, 20))
            btn.setCheckable(False)
            btn.setStyleSheet("QPushButton { text-align: left; }")
            layout.addWidget(btn)
            # Connect buttons to respective slots
            if label == "Settings":
                btn.clicked.connect(self.open_settings)
            elif label == "Contact":
                btn.clicked.connect(self.open_contact)
            elif label == "Log Out":
                btn.clicked.connect(self.logout)  # Connect Log Out button

    def init_modules(self):
        # Initialize each module and add to the stacked widget
        self.home_page = SellProductWidget(self.inventory_service)  # Updated to SellProductWidget

        self.products_management = ProductsManagement(self.inventory_service)
        self.batches_management = BatchesManagement(self.inventory_service)
        self.sales_management = SalesManagement(self.inventory_service)
        self.reports = Reports(self.inventory_service)
        self.settings_page = Settings(self.inventory_service)  # Assuming Settings module exists

        # Connect the Settings dialog signal to the toggle_auto_backup_slot
        self.settings_page.auto_backup_toggled.connect(self.toggle_auto_backup_slot)

        # Add widgets to the stack in the same order as buttons
        self.stack.addWidget(self.home_page)               # Index 0 (Home)
        self.stack.addWidget(self.products_management)     # Index 1
        self.stack.addWidget(self.batches_management)      # Index 2
        self.stack.addWidget(self.sales_management)        # Index 3
        self.stack.addWidget(self.reports)                 # Index 4
        self.stack.addWidget(self.settings_page)           # Index 5

    def connect_buttons(self):
        # Connect navigational buttons to switch pages
        self.nav_buttons["Home"].clicked.connect(lambda: self.switch_page(0))
        self.nav_buttons["Product Management"].clicked.connect(lambda: self.switch_page(1))
        self.nav_buttons["Batch Management"].clicked.connect(lambda: self.switch_page(2))
        self.nav_buttons["Sales Management"].clicked.connect(lambda: self.switch_page(3))
        self.nav_buttons["Reports"].clicked.connect(lambda: self.switch_page(4))
        
        # Connect Backup and Restore buttons to their functions
        self.nav_buttons["Backup"].clicked.connect(self.backup_data)
        self.nav_buttons["Restore"].clicked.connect(self.restore_data)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)

    def open_settings(self):
        # Navigate to the Settings page
        self.switch_page(5)  # Assuming Settings is at index 5
        # Update button states
        for btn_label, btn in self.nav_buttons.items():
            if btn_label not in ["Backup", "Restore"]:
                btn.setChecked(False)

    def open_contact(self):
        # Open the Contact Dialog
        contact_dialog = ContactDialog()
        contact_dialog.exec()

    def backup_data(self):
        try:
            data = fetch_data()
            data_dict = convert_data_to_dict(data)
            save_to_json(data_dict)
            QMessageBox.information(self, "Backup", "Data has been backed up successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Backup Error", f"An error occurred during backup: {e}")

    def restore_data(self):
        try:
            message = restore_data_from_json()
            QMessageBox.information(self, "Restore", message)
        except Exception as e:
            QMessageBox.critical(self, "Restore Error", f"An error occurred during restore: {e}")

    def logout(self):
        """
        Logs out the current user by closing the main window and opening the login window.
        """
        from login_window import LoginWindow  # Local import to avoid circular dependency
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def init_auto_backup(self):
        """
        Initializes the automatic backup timer.
        """
        self.auto_backup_timer = QTimer(self)
        self.auto_backup_timer.timeout.connect(self.auto_backup)
        
        # Load auto backup setting
        self.load_auto_backup_setting()

    def auto_backup(self):
        """
        Performs an automatic backup without notifying the user.
        """
        try:
            data = fetch_data()
            data_dict = convert_data_to_dict(data)
            save_to_json(data_dict)
            # No notification to the user
        except Exception as e:
            # Optionally log the error to a file or console
            print(f"Auto Backup Error: {e}")

    def load_auto_backup_setting(self):
        """
        Loads the auto backup setting from a config file.
        """
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
                auto_backup_enabled = config.get('auto_backup_enabled', True)
        except (FileNotFoundError, json.JSONDecodeError):
            auto_backup_enabled = True  # Default to enabled

        if auto_backup_enabled:
            self.auto_backup_timer.start(10000)  # 5 minutes in milliseconds
        else:
            self.auto_backup_timer.stop()

    def save_auto_backup_setting(self, enabled):
        """
        Saves the auto backup setting to a config file.
        """
        config = {}
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Use default if config file doesn't exist or is corrupted

        config['auto_backup_enabled'] = enabled

        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)

    def toggle_auto_backup_slot(self, enabled):
        """
        Slot to handle auto backup toggle from the Settings dialog.
        
        :param enabled: Boolean indicating whether to enable auto backup.
        """
        if enabled:
            self.auto_backup_timer.start(300000)  # 5 minutes in milliseconds
            QMessageBox.information(self, "Auto Backup", "Auto Backup has been enabled.")
        else:
            self.auto_backup_timer.stop()
            QMessageBox.information(self, "Auto Backup", "Auto Backup has been disabled.")
        
        self.save_auto_backup_setting(enabled)

# Run the App
def run_app(inventory_service):
    app = QApplication(sys.argv)
    window = ModernSidebarUI(inventory_service)
    window.show()
    sys.exit(app.exec())

# Run the application
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    inventory_service = None  # Initialize your inventory_service appropriately
    run_app(inventory_service)