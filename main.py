import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QFont, QPalette, QBrush, QPixmap

class PhoneCheckerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expo Check-in")
        self.setFixedSize(400, 300)

        palette = QPalette()
        bg = QPixmap("background.jpg")
        palette.setBrush(QPalette.Window, QBrush(bg))
        self.setPalette(palette)

        layout = QVBoxLayout()
        title = QLabel("Please write your phone number")
        title.setFont(QFont("Arial", 16))
        layout.addWidget(title)
        self.input = QLineEdit()
        layout.addWidget(self.input)

        self.button = QPushButton("OK")
        self.button.clicked.connect(self.check_number)
        layout.addWidget(self.button)

        self.result = QLabel("")
        layout.addWidget(self.result)

        self.setLayout(layout)

        self.data = pd.read_excel("registered.xlsx")

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
