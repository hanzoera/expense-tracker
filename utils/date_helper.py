from PyQt6.QtCore import QDate
from datetime import datetime

def getCurrentQDate():
    current_date = datetime.now().strftime("%Y-%m-%d")
    year, month, day = map(int, current_date.split('-'))
    return QDate(year, month, day)

def stringToQDate(date_string):
    year, month, day = map(int, date_string.split('-'))
    return QDate(year, month, day)