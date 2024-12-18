from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
import sys


class ModernSidebarUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modern Sidebar UI")
        self.setGeometry(100, 100, 1200, 700)

        # Main Widget
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
                border-right: 1px solid #2b2b3c;
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
                border-left: 3px solid #00adb5;
                color: #00adb5;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(10)

        # Add Buttons with Icons
        self.add_menu_button("  Home", sidebar_layout, "icons/home.svg")
        self.add_menu_button("  Product Management", sidebar_layout, "icons/product.svg")
        self.add_menu_button("  Batch Management", sidebar_layout, "icons/batch.svg")
        self.add_menu_button("  Sales Management", sidebar_layout, "icons/sales.svg")
        self.add_menu_button("  Reports", sidebar_layout, "icons/reports.svg")

        # Spacer to push items to the bottom
        sidebar_layout.addStretch()

        # Bottom Buttons
        self.add_menu_button("  Settings", sidebar_layout, "icons/settings.svg")
        self.add_menu_button("  Contact", sidebar_layout, "icons/contact.svg")

        # Add Sidebar to Main Layout
        main_layout.addWidget(sidebar)

        # Main Content Area
        main_content = QFrame()
        main_content.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: none;
            }
        """)
        main_layout.addWidget(main_content)

    def add_menu_button(self, text, layout, icon_path=None):
        button = QPushButton(text)
        button.setFixedHeight(40)
        if icon_path:
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(20, 20))
        layout.addWidget(button)

# Run the App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernSidebarUI()
    window.show()
    sys.exit(app.exec())
