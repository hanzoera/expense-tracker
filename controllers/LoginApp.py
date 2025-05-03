import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem

# from models.user import user

class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("views/login_window.ui", self)
        self.loginBtn.clicked.connect(self.handle_login)
        self.registerBtn.clicked.connect(self.open_register_window) # to be created soon
        self.setWindowTitle("Expense Tracker: Login")
    
    # def handle_login(self):
        