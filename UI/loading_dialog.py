# filepath: /c:/Users/ASUS/Desktop/Layered/UI/loading_dialog.py
import os
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMovie


class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Loading")
        self.setFixedSize(100, 100)  # Set the dialog size to 100x100
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)

        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setFixedSize(100, 100)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Initialize QMovie
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gif_path = os.path.join(script_dir, "icons", "loading.gif")
        if os.path.exists(gif_path):
            self.movie = QMovie(gif_path)
            self.movie.setScaledSize(self.label.size())
            self.label.setMovie(self.movie)
        else:
            self.label.setText("Loading...")

    def showEvent(self, event):
        if hasattr(self, 'movie'):
            self.movie.start()
        super().showEvent(event)