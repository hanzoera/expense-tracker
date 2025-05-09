import sys
from PyQt6 import uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView, QDateEdit

from config.DatabaseConnection import DatabaseConnection

class ExpenseTableApp(QMainWindow):
    def __init__(self, user_id):
        super().__init__()

        # assign the logged-in user's ID as an instance variable to be use for SQL queries
        self.user_id = user_id

        uic.loadUi("views/expense_tracker.ui", self)
        self.curDate.clicked.connect(self.toCurrentDate)
        self.saveEntry.clicked.connect(self.saveEntryFunc)
        self.clearEntry.clicked.connect(self.clearEntryFunc)
        self.editEntry.clicked.connect(self.openEditWindow)
        self.delEntry.clicked.connect(self.delEntryFunc)
        self.editEntry.setEnabled(False)
        self.delEntry.setEnabled(False)


        self.itemCategory.addItems(["Utilities", "Transportation", "Food & Drinks", "Entertainment", "Shopping", "Others"])
        self.spendrecords.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.spendrecords.itemSelectionChanged.connect(self.on_row_selected)
        self.load_expenses()

    def toCurrentDate(self):
        from utils.date_helper import getCurrentQDate
        self.datePurchase.setDate(getCurrentQDate())
    

    # It inserts the inputs that you typed sa database.
    def saveEntryFunc(self):
        item = self.itemName.text() 
        category = self.itemCategory.currentText()
        price = self.itemPrice.text()
        quantity = self.itemQuant.text()
        date = self.datePurchase.date()

        # Convert the QDate object to a string in the format "YYYY-MM-DD"
        date_str = date.toString("yyyy-MM-dd")

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
            cursor.execute(insert_query, (self.user_id, category, item, quantity, price, date_str))
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


    def on_row_selected(self):
        selected_items = self.spendrecords.selectedItems()
        if selected_items:
            self.editEntry.setEnabled(True)
            self.delEntry.setEnabled(True)
        else:
            self.editEntry.setEnabled(False)
            self.delEntry.setEnabled(False)


    # Displays the records in the table.
    def load_expenses(self):
        try:
            db = DatabaseConnection()
            connection = db.connect()
            cursor = connection.cursor()
            select_query = "SELECT id, item, category, price, quantity, date FROM expenses WHERE user_id = %s ORDER BY id DESC"
            cursor.execute(select_query, self.user_id)
            records = cursor.fetchall()

            if not records:
                QMessageBox.information(self, "No Entries", "No expense records found.")
                cursor.close()
                db.close()
                return
            
            self.spendrecords.setRowCount(0)

            for row_number, row_data in enumerate(records):
                self.spendrecords.insertRow(row_number)

                item = QTableWidgetItem(row_data[1])  # item name
                item.setData(256, row_data[0])  # store expense ID in Qt.UserRole (256)

                self.spendrecords.setItem(row_number, 0, item)
                self.spendrecords.setItem(row_number, 1, QTableWidgetItem(row_data[2]))  # category
                self.spendrecords.setItem(row_number, 2, QTableWidgetItem("Php " + str(row_data[3])))  # price per
                self.spendrecords.setItem(row_number, 3, QTableWidgetItem(str(row_data[4])))  # quantity
                self.spendrecords.setItem(row_number, 4, QTableWidgetItem(str(row_data[5])))  # date
                self.spendrecords.setItem(row_number, 5, QTableWidgetItem("Php " + str(row_data[3] * row_data[4])))

            cursor.close()
            db.close()
        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Failed to load entries from database.\n{e}")

    def openEditWindow(self):
        selected_items = self.spendrecords.selectedItems()
        
        if selected_items:
            row_data = [item.text().replace("Php ", "") for item in selected_items]
            from controllers.EditApp import Edit
            self.edit_window = Edit(self.user_id, row_data)
            self.edit_window.show()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a row to edit.")

    def delEntryFunc(self):
        selected_items = self.spendrecords.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "Please select a row to delete.")
            return

        reply = QMessageBox.question(self, "Confirm Deletion", "Are you sure you want to delete this record?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                item_with_id = selected_items[0]  # Any cell in the row is fine
                expense_id = item_with_id.data(256)  # Get the ID we stored earlier

                db = DatabaseConnection()
                connection = db.connect()
                cursor = connection.cursor()
                delete_query = "DELETE FROM expenses WHERE id = %s AND user_id = %s"
                cursor.execute(delete_query, (expense_id, self.user_id))
                connection.commit()
                cursor.close()
                db.close()

                self.load_expenses()
                QMessageBox.information(self, "Deleted", "Expense entry deleted successfully.")
                self.editEntry.setEnabled(False)
                self.delEntry.setEnabled(False)

            except Exception as e:
                QMessageBox.critical(self, "Deletion Error", f"Failed to delete entry.\n{e}")
