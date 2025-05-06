import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem

class ExpenseTableApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.load_ui("views/expense_tracker.ui", self)

