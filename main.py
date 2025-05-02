import sys
import pandas as pd
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
)
from PySide6.QtGui import QFont, QPalette, QBrush, QPixmap

class PhoneCheckerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.success_sound = QSoundEffect()
        self.success_sound.setSource(QUrl.fromLocalFile("C:/Users/Ali/Desktop/welcome.wav"))
        self.success_sound.setVolume(0.8)

        self.error_sound = QSoundEffect()
        self.error_sound.setSource(QUrl.fromLocalFile("C:/Users/Ali/Desktop/error.wav"))
        self.error_sound.setVolume(0.8)

        self.setWindowTitle("Expo Check-in")
        self.setFixedSize(1270, 720)

        palette = QPalette()
        bg = QPixmap("C:\\Users\\Ali\\Downloads\\BG.jpg")
        palette.setBrush(QPalette.Window, QBrush(bg))
        self.setPalette(palette)

        layout = QVBoxLayout()

        title = QLabel("Please write your phone number")
        title.setFont(QFont("Arial", 16))
        layout.addWidget(title)

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


        # Load custom Persian font
        font_id = QFontDatabase.addApplicationFont("C:\\Users\\Ali\\Downloads\\myfont.ttf")  # Path to your .ttf file
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        persian_font = QFont(family, 24)  # 24 is font size, change it if needed

        self.result.setFont(persian_font)
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setStyleSheet("color: white;")  # optional: change text color

        layout.addWidget(self.result)

        self.setLayout(layout)

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

        match = self.data[phone_list == number]

        if not match.empty:
            name = match.iloc[0]['Name']
            self.result.setText(f"✅ {name} عزیز، خوش اومدی!")
            self.success_sound.play()
        else:
            self.result.setText("❌ متأسفم! اسمتو پیدا نکردیم.")
            self.error_sound.play()


app = QApplication(sys.argv)
window = PhoneCheckerApp()
window.show()
app.exec()
