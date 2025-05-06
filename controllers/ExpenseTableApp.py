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

        self.itemCategory.addItems(["Utilities", "Transportion", "Food", "Entertainment", "Others"])

        self.rowCount = 0

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
        
        table = self.spendrecords
        table.insertRow(self.rowCount)
        table.setItem(self.rowCount, 0, QTableWidgetItem(str(self.rowCount + 1)))
        table.setItem(self.rowCount, 1, QTableWidgetItem(category))
        table.setItem(self.rowCount, 2, QTableWidgetItem(item))
        table.setItem(self.rowCount, 3, QTableWidgetItem(quantity))
        table.setItem(self.rowCount, 4, QTableWidgetItem(date))
        self.rowCount += 1

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
            self.clearEntry()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save entry to database.\n{e}")

    def clearEntryFunc(self):
        self.itemName.clear()
        self.itemCategory.setCurrentIndex(0)
        self.itemPrice.clear()
        self.itemQuant.clear()
        self.datePurchase.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTableApp()
    window.show()
    sys.exit(app.exec())