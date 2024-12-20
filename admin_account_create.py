import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
import hashlib
import json
import os

class AdminAccountCreationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Admin Account")
        self.init_ui()
        self.apply_styles()
        self.setFixedSize(400, 500)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(20)

        title = QLabel("Create Admin Account")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Username")
        self.username_edit.setFixedHeight(40)
        main_layout.addWidget(self.username_edit)

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setFixedHeight(40)
        main_layout.addWidget(self.password_edit)

        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_edit.setPlaceholderText("Confirm Password")
        self.confirm_password_edit.setFixedHeight(40)
        main_layout.addWidget(self.confirm_password_edit)

        create_button = QPushButton("Create Admin")
        create_button.setObjectName("primaryButton")
        create_button.clicked.connect(self.create_admin)
        create_button.setFixedHeight(40)
        main_layout.addWidget(create_button)

        self.setLayout(main_layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2d;
                color: #c4c4c4;
                font-family: Arial, Helvetica, sans-serif;
                font-size: 14px;
            }
            QLabel#titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #00adb5;
                margin-bottom: 20px;
            }
            QLineEdit {
                background-color: #2b2b3c;
                color: #ffffff;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 1px solid #00adb5;
            }
            QPushButton#primaryButton {
                background-color: #00adb5;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#primaryButton:hover {
                background-color: #007f8b;
            }
            QPushButton {
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
            }
        """)

    def create_admin(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        confirm_password = self.confirm_password_edit.text().strip()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Input Error", "Please fill out all fields.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Input Error", "Passwords do not match.")
            return

        users = self.load_users()
        if any(user['username'] == username for user in users):
            QMessageBox.warning(self, "Error", "Username already exists.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        new_user = {'username': username, 'password': hashed_password, 'role': 'admin'}
        users.append(new_user)
        self.save_users(users)

        QMessageBox.information(self, "Success", "Admin account created successfully.")
        self.close()

    def load_users(self):
        if not os.path.exists('users.json'):
            return []
        with open('users.json', 'r') as f:
            return json.load(f)

    def save_users(self, users):
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)

# Add the following lines to allow running this file directly
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminAccountCreationWindow()
    window.show()
    sys.exit(app.exec())