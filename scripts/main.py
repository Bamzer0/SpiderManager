import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget
)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFontDatabase, QFont

from datetime import datetime
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget

from LogBook import LogBook
from Schedule import Schedule
from FileManager import resource_path

def load_custom_font():
    font_path = resource_path("assets/Yoster Island.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)

    if font_id == -1:
        print("Failed to load font at:", font_path)
        return

    families = QFontDatabase.applicationFontFamilies(font_id)
    if not families:
        print("Font loaded but no family found.")
        return

    font_family = families[0]
    QApplication.setFont(QFont(font_family, 20))
    print("Custom font loaded:", font_family)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TarantulaManager")
        self.setGeometry(100, 100, 1400, 800)

        tabs = QTabWidget()
        tabs.addTab(LogBook(), "Logbook")
        tabs.addTab(Schedule(), "Schedule")
        # tabs.addTab(FeedingSchedule(), "Feeding Schedule")
        self.setCentralWidget(tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_custom_font()
    #app.setFont(QFont("Yoster Island", 20)) # change this to qss file later 
    app.setStyleSheet(
        """
    QMainWindow {
        background: #322924;
        }
    QWidget {
        background: #322924
        }
    QTabWidget::pane {
        background: #322924
        }

    QTabBar::tab {
        background: #EAB22D; 
        padding: 6px 12px;
        border: 1px solid #444;
    }

    QTabBar::tab:selected {
        background-color: #FFCE56;
        
    }
    QTableWidget {
        background: #EAB22D;
        alternate-background-color: #FFCE56;
        font-size: 15px;
        font-family: Yoster Island;
        color: #322924;
        }
    
    QTableCornerButton::section {
        background-color: #322924;
        border: 1px solid #444;
    }
    QHeaderView::section {
        background: #322924;
        font-size: 15px;
        font-family: Yoster Island;
        color: #DDDEE0
        }
    
     QComboBox, QLineEdit, QDateEdit, QPushButton{
        color: #DDDEE0;
        background: #3E342F;
        font-family: "Yoster Island";
    }

        QComboBox QAbstractItemView {
        background: #3E342F;
        color: #DDDEE0;
    }

    QLabel {
        color: #DDDEE0;
    }
    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())