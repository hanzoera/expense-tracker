import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker: Login")
        uic.loadUi("views/login_window.ui", self)
        # print(hasattr(self, "createAccountBtn"))
        # print(dir(self))
        self.loginBtn.clicked.connect(self.handleLogin)
        self.createAccountBtn.clicked.connect(self.openRegisterWindow)
    
    def handleLogin(self):
        # Initial login credentials error handling
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        # Checks if the user provide username and password
        if not username or not password:
            QMessageBox.warning(self, "Login Failure", "Please enter both your username and password.")
            return
        
        # 
        # pass onto model.user
        
    def openRegisterWindow(self):
        from controllers.RegisterApp import Register
        self.register_window = Register()
        self.register_window.show()
        self.close() # close the login window