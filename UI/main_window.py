# UI/main_window.py

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFrame, QStackedWidget, QLabel, QDialog
)
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtSvg import QSvgRenderer  # Corrected import

from .products_management import ProductsManagement
from .batches_management import BatchesManagement
from .sales_management import SalesManagement
from .suppliers_management import SuppliersManagement
from .orders_management import OrdersManagement
from .reports import Reports
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

class ModernSidebarUI(QMainWindow):
    def __init__(self, inventory_service):
        super().__init__()

        self.inventory_service = inventory_service

        self.setWindowTitle("Pharmacy Inventory Management")
        self.setGeometry(100, 100, 1200, 700)

        # Central Widget
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #f4f4f4;")
        self.setCentralWidget(self.central_widget)

        # Main Layout
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1e1e2d;
                border-right: 0.5px solid #2b2b3c; /* Reduced from 1px to 0.5px */
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
                border-left: 2px solid #00adb5; /* Reduced from 3px to 2px */
                color: #00adb5;
            }
            QPushButton:checked {
                background-color: #2b2b3c;
                border-left: 2px solid #00adb5; /* Reduced from 3px to 2px */
                color: #00adb5;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(10)

        # Initialize Buttons
        self.buttons = {}
        self.init_sidebar_buttons(sidebar_layout)

        # Spacer to push items to the bottom
        sidebar_layout.addStretch()

        # Bottom Buttons
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
        self.buttons["Home"].setChecked(True)
        self.stack.setCurrentIndex(0)

    def init_sidebar_buttons(self, layout):
        # Define button labels and corresponding icon paths
        button_info = [
            ("Home", "icons/home.svg"),
            ("Product Management", "icons/product.svg"),
            ("Batch Management", "icons/batch.svg"),
            ("Sales Management", "icons/sales.svg"),
            ("Reports", "icons/reports.svg"),
        ]

        for label, icon_path in button_info:
            btn = QPushButton(f"  {label}")
            btn.setFixedHeight(40)
            btn.setIcon(load_white_icon(icon_path))
            btn.setIconSize(QSize(20, 20))
            btn.setCheckable(True)
            btn.setStyleSheet("QPushButton { text-align: left; }")
            layout.addWidget(btn)
            self.buttons[label] = btn

    def init_bottom_buttons(self, layout):
        # Define bottom button labels and icon paths
        bottom_button_info = [
            ("Settings", "icons/settings.svg"),
            ("Contact", "icons/contact.svg"),
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

    def init_modules(self):
        # Initialize each module and add to the stacked widget
        self.home_page = SellProductWidget(self.inventory_service)  # Updated to SellProductWidget

        self.products_management = ProductsManagement(self.inventory_service)
        self.batches_management = BatchesManagement(self.inventory_service)
        self.sales_management = SalesManagement(self.inventory_service)
        self.reports = Reports(self.inventory_service)
        self.settings_page = Settings(self.inventory_service)  # Assuming Settings module exists

        # Add widgets to the stack in the same order as buttons
        self.stack.addWidget(self.home_page)               # Index 0 (Home)
        self.stack.addWidget(self.products_management)     # Index 1
        self.stack.addWidget(self.batches_management)      # Index 2
        self.stack.addWidget(self.sales_management)        # Index 3
        self.stack.addWidget(self.reports)                 # Index 4
        self.stack.addWidget(self.settings_page)           # Index 5 (for Settings)

    def connect_buttons(self):
        # Connect each button to change the stacked widget
        self.buttons["Home"].clicked.connect(lambda: self.switch_page(0))
        self.buttons["Product Management"].clicked.connect(lambda: self.switch_page(1))
        self.buttons["Batch Management"].clicked.connect(lambda: self.switch_page(2))
        self.buttons["Sales Management"].clicked.connect(lambda: self.switch_page(3))
        self.buttons["Reports"].clicked.connect(lambda: self.switch_page(4))

        # Ensure only one button is checked at a time
        for label, btn in self.buttons.items():
            if label != "Home":  # Home is set as default
                btn.setAutoExclusive(False)
                btn.clicked.connect(self.update_button_states)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)

    def update_button_states(self):
        # Uncheck all buttons except the one clicked
        for label, btn in self.buttons.items():
            if btn.isChecked():
                for other_label, other_btn in self.buttons.items():
                    if other_btn != btn:
                        other_btn.setChecked(False)

    def open_settings(self):
        # Navigate to the Settings page
        self.stack.setCurrentWidget(self.settings_page)

    def open_contact(self):
        # Open the Contact Dialog
        contact_dialog = ContactDialog()
        contact_dialog.exec()

# Run the App
def run_app(inventory_service):
    app = QApplication(sys.argv)
    window = ModernSidebarUI(inventory_service)
    window.show()
    sys.exit(app.exec())