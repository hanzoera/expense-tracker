import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem

from config.DatabaseConnection import DatabaseConnection
from datetime import datetime

class ExpenseTableApp(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        # assign the logged-in user's ID as an instance variable to be use for SQL queries
        self.user_id = user_id

        uic.loadUi("views/expense_tracker.ui", self)
        self.curDate.clicked.connect(self.toCurrentDate)
        self.saveEntry.clicked.connect(self.saveEntryFunc)
        self.clearEntry.clicked.connect(self.clearEntryFunc)

        self.itemCategory.addItems(["Utilities", "Transportation", "Food & Drinks", "Entertainment", "Shopping", "Others"])

        self.load_expenses()

    def toCurrentDate(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.datePurchase.setText(current_date)
    

    # It inserts the inputs that you typed sa database.
    def saveEntryFunc(self):
        item = self.itemName.text() 
        category = self.itemCategory.currentText()
        price = self.itemPrice.text()
        quantity = self.itemQuant.text()
        date = self.datePurchase.text()

        #Input Validation For Inputs or Smth.
        if not item or not price or not quantity or not date:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return
        
        try:
            db = DatabaseConnection()
            connection = db.connect()
            cursor = connection.cursor()

            insert_query = """
                INSERT INTO expenses (user_id, category, item, quantity, price, date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (self.user_id, category, item, quantity, price, date))
            connection.commit()
            cursor.close()
            db.close()

            QMessageBox.information(self, "Entry Saved", "Expense entry has been added to the database.")
            self.clearEntryFunc()
            self.load_expenses()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save entry to database.\n{e}")


    # Clears the inputs that you typed.
    def clearEntryFunc(self):
        self.itemName.clear()
        self.itemCategory.setCurrentIndex(0)
        self.itemPrice.clear()
        self.itemQuant.clear()
        self.datePurchase.clear()


    # Displays the records in the table.
    def load_expenses(self):
        try:
            db = DatabaseConnection()
            connection = db.connect()
            cursor = connection.cursor()
            select_query = "SELECT id, item, category, price, quantity, date FROM expenses WHERE user_id = %s ORDER BY id DESC"
            cursor.execute(select_query, self.user_id)
            records = cursor.fetchall()

            self.spendrecords.setRowCount(0)

            for row_number, row_data in enumerate(records):
                self.spendrecords.insertRow(row_number)
                self.spendrecords.setItem(row_number, 0, QTableWidgetItem(row_data[1]))  # item
                self.spendrecords.setItem(row_number, 1, QTableWidgetItem(row_data[2]))  # category
                self.spendrecords.setItem(row_number, 2, QTableWidgetItem("Php " + str(row_data[3])))  # price per
                self.spendrecords.setItem(row_number, 3, QTableWidgetItem(str(row_data[4])))  # quantity
                self.spendrecords.setItem(row_number, 4, QTableWidgetItem(str(row_data[5]))) # date
                self.spendrecords.setItem(row_number, 5, QTableWidgetItem("Php " + str(row_data[3] * row_data[4])))

            cursor.close()
            db.close()

        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Failed to load entries from database.\n{e}")