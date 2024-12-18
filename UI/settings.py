# ui/settings.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class Settings(QWidget):
    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        form_layout = QFormLayout()
        
        self.db_url_edit = QLineEdit()
        self.db_url_edit.setText(self.inventory_service.get_db_url())
        form_layout.addRow("Database URL:", self.db_url_edit)
        
        self.layout.addLayout(form_layout)
        
        # Save button
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Settings")
        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        self.layout.addLayout(btn_layout)
        
        self.save_btn.clicked.connect(self.save_settings)

        self.apply_styles()

    def apply_styles(self):
        # Apply modern UI design based on the provided guidelines
        self.setFont(QFont("Roboto", 14))
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2d;
                color: #c4c4c4;
                font-family: "Roboto";
                font-size: 14px;
            }

            QFormLayout QLabel {
                color: #00adb5;
                font-size: 16px;
                font-weight: 600;
            }

            QLineEdit {
                background-color: #2b2b3c;
                color: #ffffff;
                border: 1px solid #5a5f66;
                padding: 4px;
            }

            QLineEdit:focus {
                border: 1px solid #00adb5;
            }

            QPushButton {
                background-color: #00adb5;
                color: #ffffff;
                border-radius: 5px;
                padding: 8px 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #007f8b;
            }

            QMessageBox {
                background-color: #1e1e2d;
                color: #c4c4c4;
            }
        """)

    def save_settings(self):
        new_db_url = self.db_url_edit.text().strip()
        if not new_db_url:
            QMessageBox.warning(self, "Invalid Input", "Database URL cannot be empty.")
            return
        try:
            self.inventory_service.update_db_url(new_db_url)
            QMessageBox.information(self, "Success", "Settings updated successfully. Please restart the application for changes to take effect.")
        except NotImplementedError:
            QMessageBox.critical(self, "Error", "Dynamic DB URL update not supported.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update settings: {e}")
