import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

from models.User import InnerUser

class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker: Create account")
        uic.loadUi("views/registration_window.ui", self)
        self.backToLoginBtn.clicked.connect(self.returnToLoginWindow)
        self.createAccountBtn.clicked.connect(self.handleRegister)

    # Mainly Handles the create account button click event.
    # Subsequently triggers the inner user registration logic when the button is pressed.
    def handleRegister(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        re_password = self.rePasswordInput.text()

        # Initial registration data error handling
        if not username or not password or not re_password:
            QMessageBox.warning(self, "Account Creation Failed!", "Please fill in all fields to create your account.")
            return
        
        if password != re_password:
            QMessageBox.warning(self, "Account Creation Failed!", "Your passwords do not match.")
            return
        
        try:
            # Create an instance of the user query handler class
            user = InnerUser()
            # Pass onto the method that mainly manages the logic for registering new user
            is_registration_successful = user.registerUser(username, password) 

            # Indicates whether the registration was successful or not
            if is_registration_successful:
                QMessageBox.information(self, "Account Created!", "Your account has been successfully created.")
                self.usernameInput.clear()
                self.passwordInput.clear()
                self.rePasswordInput.clear()
            else:
                QMessageBox.warning(self, "Account Creation Failed!", "User account creation failed. Please try again.")
        
        except Exception as error:
            print(f"Error Message: {error}")

    def returnToLoginWindow(self):
        from controllers.LoginApp import Login
        self.login_window = Login()
        self.login_window.show()
        self.close() # Close the registration window