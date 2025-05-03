import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker: Create account")
        uic.loadUi("views/registration_window.ui", self)
        self.backToLoginBtn.clicked.connect(self.returnToLoginWindow)
        # self.createAccountBtn.clicked.connect(self.handle register)

    def handle_register(self):
        # Initial registration data error handling
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        re_password = self.rePasswordInput.text()

        if not username or password or re_password:
            QMessageBox.warning(self, "Please fill in all fields to create your account.")
            return
        
        if password != re_password:
            QMessageBox.warning(self, "Your passwords do not match.")
            return
        
        # try:
    

    def returnToLoginWindow(self):
        from controllers.LoginApp import Login
        self.login_window = Login()
        self.login_window.show()
        self.close() # close the registration window