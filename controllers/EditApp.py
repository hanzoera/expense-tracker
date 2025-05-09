import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView

from datetime import datetime
from config.DatabaseConnection import DatabaseConnection
from utils.date_helper import *


class Edit(QMainWindow):
    def __init__(self, user_id, row_data):
        super().__init__()
        uic.loadUi("views/edit_window.ui", self)

        # assign the logged-in user's ID as an instance variable to be use for SQL queries
        self.user_id = user_id

        self.itemCategory.addItems(["Utilities", "Transportation", "Food & Drinks", "Entertainment", "Shopping", "Others"])

        self.itemName.setText(row_data[0])        # item
        self.itemCategory.setCurrentText(row_data[1])  # category
        self.itemPrice.setText(row_data[2])       # price (no Php prefix now)
        self.itemQuant.setText(row_data[3])       # quantity
        self.datePurchase.setDate(stringToQDate(row_data[4]))    # date
        self.cancelChanges.clicked.connect(self.closeCancelWindow)
        self.saveChanges.clicked.connect(self.saveChangeFunc)
        
        self.curDate.clicked.connect(self.toCurrentDate)
        # self.saveChanges.clicked.connect(self.saveChanges)
        # self.cancelChanges.clicked.connect(self.cancelChanges)
    
    def toCurrentDate(self):
        self.datePurchase.setDate(getCurrentQDate())

    def closeCancelWindow(self):
        self.close()
    
    def saveChangeFunc(self):
        print("Test")
        # KULANG PA HERE, LOVE YOU