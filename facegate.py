import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCheckBox, QMainWindow
from PyQt6.QtGui import QIcon, QFont

class FaceGate(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Основа")
        self.setGeometry(50, 50, 500, 500)
        self.setWindowIcon(QIcon('icon.png')) # Замените icon.png на путь к вашему иконтеку
        self.setStyleSheet("background-color: #00c77b")

