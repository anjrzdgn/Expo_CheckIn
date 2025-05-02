import sys
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
)
from PySide6.QtGui import QFont, QPalette, QBrush, QPixmap

class PhoneCheckerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expo Check-in")
        self.setFixedSize(1270, 720)

        # Background image
        palette = QPalette()
        bg = QPixmap("C:\\Users\\Ali\\Downloads\\BG.jpg")
        palette.setBrush(QPalette.Window, QBrush(bg))
        self.setPalette(palette)

        layout = QVBoxLayout()

        title = QLabel("Please write your phone number")
        title.setFont(QFont("Arial", 16))
        layout.addWidget(title)

        # Dropdown to select time slot
        self.dropdown = QComboBox()
        self.dropdown.addItems(["15-17", "17-19"])
        self.dropdown.currentTextChanged.connect(self.load_data)
        layout.addWidget(self.dropdown)

        self.input = QLineEdit()
        layout.addWidget(self.input)

        self.button = QPushButton("OK")
        self.button.clicked.connect(self.check_number)
        layout.addWidget(self.button)

        self.result = QLabel("")
        layout.addWidget(self.result)

        self.setLayout(layout)

        # Load default data (based on default dropdown value)
        self.data = pd.DataFrame()
        self.load_data("15-17")

    def load_data(self, time_slot):
        if time_slot == "15-17":
            path = "C:\\Users\\Ali\\Desktop\\15.17.xlsx"
        elif time_slot == "17-19":
            path = "C:\\Users\\Ali\\Desktop\\17.19.xlsx"
        else:
            self.result.setText("⚠️ Unknown time slot selected.")
            return

        try:
            self.data = pd.read_excel(path)
            self.result.setText(f"✅ Loaded {time_slot} data.")
        except Exception as e:
            self.result.setText(f"❌ Error loading file: {e}")

    def check_number(self):
        number = self.input.text().strip()[1:]  # Remove the first character
        phone_list = self.data['Phone'].astype(str).str.strip()
        if number in phone_list.values:
            self.result.setText("✅ Welcome! Your registration is allowed.")
        else:
            self.result.setText("❌ Sorry, you can't be here.")

app = QApplication(sys.argv)
window = PhoneCheckerApp()
window.show()
app.exec()
