import sys
import os
import json
import hashlib

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
    QApplication, QHBoxLayout, QGraphicsOpacityEffect, QToolButton
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QIcon

# Import your UI classes and setup function
from UI.main_window import ModernSidebarUI
from services.inventory_service import InventoryService  # Adjust path as needed
from run_ui import setup_inventory_service


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)  # Ensure style is applied immediately
        self.init_ui()
        self.apply_styles()
        self.setFixedSize(400, 500)

        # Fade-in animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()

    def init_ui(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(15)

        title = QLabel("Pharmacy Inventory \nManagement System")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Username")
        self.username_edit.setFixedHeight(40)
        main_layout.addWidget(self.username_edit)

        # Connect returnPressed signal to authenticate
        self.username_edit.returnPressed.connect(self.authenticate)

        password_layout = QHBoxLayout()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setFixedHeight(40)
        password_layout.addWidget(self.password_edit)

        # Connect returnPressed signal to authenticate
        self.password_edit.returnPressed.connect(self.authenticate)

        self.toggle_password_btn = QToolButton()
        self.toggle_password_btn.setIcon(QIcon(os.path.join(script_dir, "icons", "eye_closed.png")))
        self.toggle_password_btn.setCheckable(True)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.toggle_password_btn)

        main_layout.addLayout(password_layout)

        login_button = QPushButton("Login")
        login_button.setObjectName("primaryButton")
        login_button.clicked.connect(self.authenticate)
        login_button.setFixedHeight(40)
        main_layout.addWidget(login_button)

        # Set the Login button as the default button
        login_button.setDefault(True)

        signup_layout = QHBoxLayout()
        signup_label = QLabel("Don't have an account?")
        signup_button = QPushButton("Sign Up")
        signup_button.setFlat(True)
        signup_button.setStyleSheet("color: #00adb5;")
        signup_button.clicked.connect(self.open_signup_window)
        signup_layout.addStretch()
        signup_layout.addWidget(signup_label)
        signup_layout.addWidget(signup_button)
        signup_layout.addStretch()
        main_layout.addLayout(signup_layout)

        # Connect returnPressed signal in signup fields to register_user
        signup_button.setDefault(True)

        # Admin creation link
        admin_layout = QHBoxLayout()
        admin_label = QLabel("Create an Admin Account?")
        admin_button = QPushButton("Create Admin")
        admin_button.setFlat(True)
        admin_button.setStyleSheet("color: #f08a5d;")
        admin_button.clicked.connect(self.open_admin_create)
        admin_layout.addStretch()
        admin_layout.addWidget(admin_label)
        admin_layout.addWidget(admin_button)
        admin_layout.addStretch()
        main_layout.addLayout(admin_layout)

        self.setLayout(main_layout)

    def toggle_password_visibility(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if self.toggle_password_btn.isChecked():
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_btn.setIcon(QIcon(os.path.join(script_dir, "icons", "eye_open.png")))
        else:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_btn.setIcon(QIcon(os.path.join(script_dir, "icons", "eye_closed.png")))

    def open_admin_create(self):
        from admin_account_create import AdminAccountCreationWindow
        self.admin_window = AdminAccountCreationWindow()
        self.admin_window.show()

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
            QToolButton {
                border: none;
                background: transparent;
            }
        """)

    def authenticate(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        user = self.get_user(username)
        if user and self.verify_password(password, user['password']):
            QMessageBox.information(self, "Success", f"Welcome, {username}!")
            self.open_main_window(user['role'])
        else:
            QMessageBox.critical(self, "Authentication Failed", "Invalid username or password.")

    def get_user(self, username):
        users = self.load_users()
        for user in users:
            if user['username'] == username:
                return user
        return None

    def load_users(self):
        users_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.json')
        if not os.path.exists(users_file):
            QMessageBox.critical(self, "Error", "Users file not found.")
            sys.exit(1)
        with open(users_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                QMessageBox.critical(self, "Error", "Users file is corrupted.")
                sys.exit(1)

    def verify_password(self, password, hashed_password):
        return hashlib.sha256(password.encode()).hexdigest() == hashed_password

    def open_main_window(self, role):
        self.close()
        if role == 'admin':
            try:
                inventory_service = setup_inventory_service()
                self.main_window = ModernSidebarUI(inventory_service)
                self.main_window.show()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open admin dashboard: {e}")
                sys.exit(1)
        else:
            try:
                from User.UI.user_window import UserMainWindow
            except ImportError:
                QMessageBox.critical(self, "Error", "Failed to import UserMainWindow. Please check the module path.")
                sys.exit(1)
            self.main_window = UserMainWindow()
            self.main_window.show()

    def open_signup_window(self):
        self.signup_window = SignupWindow()
        self.signup_window.show()


class SignupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Up")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)  # Ensure style is applied immediately
        self.init_ui()
        self.apply_styles()
        self.setFixedSize(400, 600)

        # Fade-in animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()

    def init_ui(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(20)

        title = QLabel("Create an Account")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Username")
        self.username_edit.setFixedHeight(40)
        main_layout.addWidget(self.username_edit)

        # Connect returnPressed signal to register_user
        self.username_edit.returnPressed.connect(self.register_user)

        password_layout = QHBoxLayout()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setFixedHeight(40)
        password_layout.addWidget(self.password_edit)

        # Connect returnPressed signal to register_user
        self.password_edit.returnPressed.connect(self.register_user)

        self.toggle_password_btn = QToolButton()
        self.toggle_password_btn.setIcon(QIcon(os.path.join(script_dir, "icons", "eye_closed.png")))
        self.toggle_password_btn.setCheckable(True)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.toggle_password_btn)

        main_layout.addLayout(password_layout)

        confirm_password_layout = QHBoxLayout()
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_edit.setPlaceholderText("Confirm Password")
        self.confirm_password_edit.setFixedHeight(40)
        confirm_password_layout.addWidget(self.confirm_password_edit)

        # Connect returnPressed signal to register_user
        self.confirm_password_edit.returnPressed.connect(self.register_user)

        self.toggle_confirm_password_btn = QToolButton()
        self.toggle_confirm_password_btn.setIcon(QIcon(os.path.join(script_dir, "icons", "eye_closed.png")))
        self.toggle_confirm_password_btn.setCheckable(True)
        self.toggle_confirm_password_btn.clicked.connect(self.toggle_confirm_password_visibility)
        confirm_password_layout.addWidget(self.toggle_confirm_password_btn)

        main_layout.addLayout(confirm_password_layout)

        signup_button = QPushButton("Sign Up")
        signup_button.setObjectName("primaryButton")
        signup_button.clicked.connect(self.register_user)
        signup_button.setFixedHeight(40)
        main_layout.addWidget(signup_button)

        # Set the Sign Up button as the default button
        signup_button.setDefault(True)

        self.setLayout(main_layout)

    def toggle_password_visibility(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if self.toggle_password_btn.isChecked():
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_btn.setIcon(QIcon(os.path.join(script_dir, "icons", "eye_open.png")))
        else:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_btn.setIcon(QIcon(os.path.join(script_dir, "icons", "eye_closed.png")))

    def toggle_confirm_password_visibility(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if self.toggle_confirm_password_btn.isChecked():
            self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_confirm_password_btn.setIcon(QIcon(os.path.join(script_dir, "icons", "eye_open.png")))
        else:
            self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_confirm_password_btn.setIcon(QIcon(os.path.join(script_dir, "icons", "eye_closed.png")))

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
            QToolButton {
                border: none;
                background: transparent;
            }
        """)

    def register_user(self):
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
        new_user = {'username': username, 'password': hashed_password, 'role': 'user'}
        users.append(new_user)
        self.save_users(users)

        QMessageBox.information(self, "Success", "Account created successfully. You can now log in.")
        self.close()

    def load_users(self):
        users_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.json')
        if not os.path.exists(users_file):
            return []
        with open(users_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                QMessageBox.critical(self, "Error", "Users file is corrupted.")
                return []

    def save_users(self, users):
        users_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.json')
        with open(users_file, 'w') as f:
            json.dump(users, f, indent=4)


# Run the application if needed
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())