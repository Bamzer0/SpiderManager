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

from FileManager import FileManager

class LogBook(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.filemanager = FileManager()
        self.fields = [
        "name", "date", "fed", "food", "pre-molt", "temp",
        "threat", "rehouse", "molt", "notes"
        ]

        self.create_table()
        self.create_form()
        self.load_data()

    def create_table(self):
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        self.layout.addWidget(self.table)
    
    def create_form(self):
        self.inputs={}

        form_row1 = QHBoxLayout()
        for field in self.fields:
            field_container = QVBoxLayout()
            label = QLabel(field.capitalize())

            if field in ["fed"]:
                input_widget = QComboBox()
                input_widget.addItems(["", "yes", "no", "maybe"])
            elif field in ["threat", "rehouse", "molt", "pre-molt"]:
                input_widget = QComboBox()
                input_widget.addItems(["no", "yes", "maybe"])
            elif field == "food":
                input_widget = QComboBox()
                input_widget.addItems(["","Cricket S","Cricket M","Cricket L","Dubia","Mealworm"])
            elif field == "date":
                input_widget = QDateEdit()
                input_widget.setDate(QDate.currentDate())  # Sets today's date
                input_widget.setDisplayFormat("dd-MM-yyyy")  # Your desired format
                input_widget.setCalendarPopup(True)  # Optional: lets user pick from calendar
                
            elif field == "name":
                input_widget = QComboBox()
                input_widget.addItems(['', 'Bibii', 'Bikki', 'Billie', 'Blaze', 'Blitz', 'Bobby', 'Bober', 'Bobo', 'Bojo', 'Bumi'])
            elif field == "temp":
                input_widget = QComboBox()
                for t in range(15, 36):
                    input_widget.addItem(f"{t}")
                input_widget.setCurrentIndex(10)
            else:
                input_widget = QLineEdit()
            self.inputs[field] = input_widget

            field_container.addWidget(label)
            field_container.addWidget(input_widget)

            # Skip 'notes' field from first row
            if field != "notes":
                form_row1.addLayout(field_container)

        self.layout.addLayout(form_row1)

        # Second row layout (notes field + button)
        form_row2 = QHBoxLayout()

        notes_container = QVBoxLayout()
        notes_label = QLabel("Notes")
        notes_input = QLineEdit()
        notes_container.addWidget(notes_label)
        notes_container.addWidget(notes_input)
        
        self.inputs["notes"] = notes_input

        Button_container = QVBoxLayout()
        Button_label = QLabel("")
        self.add_button = QPushButton("Add Entry")
        self.add_button.clicked.connect(self.add_entry)
        Button_container.addWidget(Button_label)
        Button_container.addWidget(self.add_button)

        form_row2.addLayout(notes_container)
        form_row2.addLayout(Button_container)

        self.layout.addLayout(form_row2)

        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_to_csv)
        self.layout.addWidget(self.save_button)

    def load_data(self):
        header, rows = self.filemanager.read_logs()
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)
        

        self.table.setRowCount(0)
        for row in rows:
            self.add_table_row(row)
        
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)


    def add_table_row(self, row_data):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for i, value in enumerate(row_data):
            if isinstance(value, datetime):
                display_value = value.strftime("%d-%m-%Y")
            else:
                display_value = str(value)
            self.table.setItem(row, i, QTableWidgetItem(display_value))

    def add_entry(self):
        row_data = []
        for field in self.fields:
            widget = self.inputs[field]
            if isinstance(widget, QComboBox):
                value = widget.currentText()
            elif isinstance(widget, QDateEdit):
                value = widget.date().toString("dd-MM-yyyy")
            else:
                value = widget.text().strip()
            row_data.append(value)

        # Validation: Require at least name + date
        if not all([row_data[0], row_data[1],row_data[2]]):  # Require at least name + date + fed
            return

        self.filemanager.write_csv_row(self.filemanager.get_logs_path(), row_data)
        self.add_table_row(row_data)

        # Clear form inputs
        for field, widget in self.inputs.items():
            if field == "temp":
                continue
            if isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            elif isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())
            else:
                widget.clear()

    def save_to_csv(self):
        all_rows = []
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        all_rows.append(headers)

        for row in range(self.table.rowCount()):
            row_data = []
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                value = item.text() if item else ""
                row_data.append(value)
            all_rows.append(row_data)

        self.filemanager.overwrite_csv(self.filemanager.get_logs_path(), all_rows)