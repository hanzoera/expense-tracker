import sys
from PyQt6.QtWidgets import QApplication

from controllers.LoginApp import Login
#ello
if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(application.exec())