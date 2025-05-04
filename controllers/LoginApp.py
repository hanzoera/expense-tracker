import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

from models.User import InnerUser

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
        
        # Create an instance of the user query handler class
        user = InnerUser()
        # Pass onto the method that mainly manages the logic for logging user account
        is_login_successful = user.validateUserLogin(username, password)

        # Indicates whether the login process was successful or not
        if is_login_successful:
            QMessageBox.information(self, "Login Successful!", "Welcome! Your account was successfully opened.")
            self.usernameInput.clear()
            self.passwordInput.clear()

            # from controllers.ExpenseTableApp import 
            # create expense app window object
            # show the expense app window
            # close the login window
        
    def openRegisterWindow(self):
        from controllers.RegisterApp import Register
        self.register_window = Register()
        self.register_window.show()
        self.close() # Close the login window