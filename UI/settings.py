import json
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QLabel
from PyQt6.QtCore import pyqtSignal, Qt

class Settings(QDialog):
    # Define a custom signal to emit the auto backup preference
    auto_backup_toggled = pyqtSignal(bool)

    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 300)

        # Apply styles
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2d; 
                border-radius: 10px;
                color: transparent;
                font-family: "Roboto", Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #ffffff;
                padding: 10px;
            }
            QCheckBox {
                font-size: 14px;
                color: #ffffff;
            }
        """)

        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Auto Backup Label
        auto_backup_label = QLabel("Automatically backup data every 5 minutes.")

        # Auto Backup Checkbox
        self.auto_backup_checkbox = QCheckBox("Enable Auto Backup")
        self.auto_backup_checkbox.setChecked(True)  # Default state; will be updated later
        self.auto_backup_checkbox.stateChanged.connect(self.on_auto_backup_toggled)

        # Add widgets to layout
        layout.addWidget(auto_backup_label)
        layout.addWidget(self.auto_backup_checkbox)

        # You can add more settings here as needed

        self.setLayout(layout)

    def on_auto_backup_toggled(self, state):
        """
        Emits a signal when the auto backup checkbox is toggled.
        
        :param state: Integer representing the state of the checkbox.
        """
        is_enabled = state == Qt.CheckState.Checked
        self.auto_backup_toggled.emit(is_enabled)

    def load_settings(self):
        """
        Loads settings from the config file and updates the UI accordingly.
        """
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
                auto_backup_enabled = config.get('auto_backup_enabled', True)
        except (FileNotFoundError, json.JSONDecodeError):
            auto_backup_enabled = True  # Default to enabled

        self.auto_backup_checkbox.setChecked(auto_backup_enabled)

    def save_settings(self):
        """
        Saves current settings to the config file.
        """
        config = {}
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Use default if config file doesn't exist or is corrupted

        config['auto_backup_enabled'] = self.auto_backup_checkbox.isChecked()

        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)

    def exec_(self):
        """
        Overrides the exec_ method to load settings before showing the dialog.
        """
        self.load_settings()
        return super().exec_()