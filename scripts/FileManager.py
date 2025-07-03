import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QHBoxLayout, QHeaderView, QComboBox, QTextEdit, QLabel,QDateEdit, QTableWidgetItem
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont, QColor

from datetime import datetime
import os

LOGS_FILE = "data/logs.csv"
PROFILE_FILE = "data/profile info spiders.csv"

def resource_path(relative_path):
    # When bundled with PyInstaller, use the folder where the executable is located
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    return os.path.join(base_path, relative_path)

class FileManager():
    def __init__(self):
        self.logs_file = resource_path("data/logs.csv")
        self.profile_file = resource_path("data/profile info spiders.csv")
    
    def read_csv(self, file_path, delimiter=";"):
        if not os.path.exists(file_path):
            return []

        with open(file_path, newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=delimiter)
            return list(reader)
    
    def read_logs(self):
        data = self.read_csv(self.logs_file)
        if not data:
            return [], []

        header = data[0]
        rows = []

        for row in data[1:]:  # Skip header
            if len(row) < len(header):
                continue  # Skip malformed rows

            try:
                date_obj = datetime.strptime(row[1], "%d-%m-%Y")
            except ValueError:
                date_obj = None  # If the date is malformed, you can also skip or log this

            # Replace the original date string with datetime object
            row_with_date = row.copy()
            row_with_date[1] = date_obj
            rows.append(row_with_date)

        return header, rows

    def write_csv_row(self, file_path, row_data, delimiter=";"):
        with open(file_path, "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerow(row_data)
        
    def overwrite_csv(self, file_path, all_rows, delimiter=";"):
        with open(file_path, "w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=delimiter)
            for row in all_rows:
               writer.writerow(row)

    def get_logs_path(self):
        return self.logs_file
    
    def get_profile_path(self):
        return self.profile_file
