import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QGridLayout,
    QTableWidgetItem, QPushButton, QLineEdit, QHBoxLayout, QHeaderView, QComboBox, QTextEdit, QLabel,QDateEdit, QTableWidgetItem
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont, QColor

from datetime import datetime
import os

from FileManager import FileManager

class Schedule(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout()

        self.schedule_layout = QVBoxLayout()
        self.schedule_layout.addWidget(QLabel("Left: Main Content"))

        self.profile_layout = QVBoxLayout()
        self.profile_layout.addWidget(QLabel("Right: Sidebar"))

        self.setLayout(main_layout)