import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem

from config.DatabaseConnection import DatabaseConnection
from datetime import datetime

class ExpenseTableApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.load_ui("views/expense_tracker.ui", self)

        self.curDate.clicked.connect(self.toCurrentDate)
        self.saveEntry.clicked.connect(self.saveEntryFunc)
        self.clearEntry.clicked.connect(self.clearEntryFunc)

        self.itemCategory.addItems(["Utilities", "Transportation", "Food", "Entertainment", "Others"])

        self.load_expenses()

    def toCurrentDate(self):
        current_date = datetime.now().strftime("%d-%m-%Y")
        self.datePurchase.setText(current_date)
    
    def saveEntryFunc(self):
        item = self.itemName.text() 
        category = self.itemCategory.currentText()
        price = self.itemPrice.text()
        quantity = self.itemQuant.text()
        date = self.datePurchase.text()

        #Input Validation For Inputs or Smth
        if not item or not price or not quantity or not date:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return
        
        try:
            db = DatabaseConnection()
            connection = db.connect()
            cursor = connection.cursor()

            insert_query = """
                INSERT INTO expenses (category, item, quantity, date)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (category, item, quantity, date))
            connection.commit()
            cursor.close()
            db.close()

            QMessageBox.information(self, "Entry Saved", "Expense entry has been added to the database.")
            self.clearEntryFunc()
            self.load_expenses()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save entry to database.\n{e}")

    def clearEntryFunc(self):
        self.itemName.clear()
        self.itemCategory.setCurrentIndex(0)
        self.itemPrice.clear()
        self.itemQuant.clear()
        self.datePurchase.clear()

    def load_expenses(self):
        try:
            db = DatabaseConnection()
            connection = db.connect()
            cursor = connection.cursor()

            select_query = "SELECT id, category, item, quantity, date FROM expenses ORDER BY id DESC"
            cursor.execute(select_query)
            records = cursor.fetchall()

            self.spendrecords.setRowCount(0)

            for row_number, row_data in enumerate(records):
                self.spendrecords.insertRow(row_number)
                self.spendrecords.setItem(row_number, 0, QTableWidgetItem(str(row_number + 1)))  # Row number
                self.spendrecords.setItem(row_number, 1, QTableWidgetItem(row_data[1]))  # category
                self.spendrecords.setItem(row_number, 2, QTableWidgetItem(row_data[2]))  # item
                self.spendrecords.setItem(row_number, 3, QTableWidgetItem(str(row_data[3])))  # quantity
                self.spendrecords.setItem(row_number, 4, QTableWidgetItem(str(row_data[4])))  # date

            cursor.close()
            db.close()

        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Failed to load entries from database.\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTableApp()
    window.show()
    sys.exit(app.exec())