import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView

from config.DatabaseConnection import DatabaseConnection
from controllers.ExpenseTableApp import ExpenseTableApp
from utils.date_helper import *


class Edit(QMainWindow):
    def __init__(self, parent_app, user_id, row_data):
        super().__init__()
        uic.loadUi("views/edit_window.ui", self)

        # assign the logged-in user's ID as an instance variable to be use for SQL queries
        self.user_id = user_id
        self.parent_app = parent_app
        self.old_item_name = row_data[0]

        self.itemCategory.addItems(["Utilities", "Transportation", "Food & Drinks", "Entertainment", "Shopping", "Others"])

        self.itemName.setText(row_data[0])        # item
        self.itemCategory.setCurrentText(row_data[1])  # category
        self.itemPrice.setText(row_data[2])       # price (no Php prefix now)
        self.itemQuant.setText(row_data[3])       # quantity
        self.datePurchase.setDate(stringToQDate(row_data[4]))    # date
        self.cancelChanges.clicked.connect(self.closeCancelWindow)
        self.saveChanges.clicked.connect(self.saveExpenses)
        
        self.curDate.clicked.connect(self.toCurrentDate)
        # self.saveChanges.clicked.connect(self.saveChanges)
        # self.cancelChanges.clicked.connect(self.cancelChanges)
    
    def saveExpenses(self):
        # get the text from the QWidgets
        item = self.itemName.text() 
        category = self.itemCategory.currentText()
        price = self.itemPrice.text()
        quantity = self.itemQuant.text()
        date = self.datePurchase.date().toString("yyyy-MM-dd")  # Format the date as a string

        try:
            db = DatabaseConnection()
            connection = db.connect()
            cursor = connection.cursor()
            update_query = """
                UPDATE expenses
                SET item = %s, category = %s, price = %s, quantity = %s, date = %s
                where user_id = %s AND item = %s
            """
            values = (item, category, price, quantity, date, self.user_id, self.old_item_name)
            cursor.execute(update_query, values)
            connection.commit()

            # Check how many rows were affected
            rows_affected = cursor.rowcount
            print(f"Rows affected: {rows_affected}")

            if rows_affected > 0:
                QMessageBox.information(self, "Success", "Expense updated successfully.")
                self.parent_app.load_expenses()  # reload the table from ExpenseTableApp
                self.close()  # Close the edit window
            else:
                QMessageBox.warning(self, "No Changes", "No changes were made.")

        except Exception as e:
            QMessageBox.critical(self, "Update Error", f"Failed to update entry.\n{e}")
        
        finally:
            cursor.close()
            connection.close()

    def toCurrentDate(self):
        self.datePurchase.setDate(getCurrentQDate())

    def closeCancelWindow(self):
        self.close()