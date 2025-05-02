import sys
import pandas as pd
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox)
from PySide6.QtGui import QFont, QPalette, QBrush, QPixmap, QIcon
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # This is set by PyInstaller when running the EXE
    except AttributeError:
        base_path = os.path.abspath(".")  # This is used during development

    return os.path.join(base_path, relative_path)

class PhoneCheckerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.success_sound = QSoundEffect()
        self.success_sound.setSource(QUrl.fromLocalFile(resource_path("Wellcome.wav")))
        self.success_sound.setVolume(0.8)

        self.error_sound = QSoundEffect()
        self.error_sound.setSource(QUrl.fromLocalFile(resource_path("Error.wav")))
        self.error_sound.setVolume(0.8)

        logo = QLabel()

        self.setWindowTitle("Expo Check-in")
        self.setFixedSize(426, 720)
        self.setWindowIcon(QIcon(resource_path("icon.ico")))

        palette = QPalette()
        bg = QPixmap(resource_path("BG2.jpg"))
        palette.setBrush(QPalette.Window, QBrush(bg))
        self.setPalette(palette)

        self.dropdown = QComboBox(self)
        self.dropdown.addItems(["15-17", "17-19"])
        self.dropdown.setGeometry(5, 690, 100, 30)
        self.dropdown.currentTextChanged.connect(self.load_data)

        self.input = QLineEdit(self)
        self.input.setGeometry(50, 240, 226, 40)

        self.button = QPushButton("Search", self)
        self.button.setGeometry(330, 235, 50, 45)
        self.button.clicked.connect(self.check_number)
        self.input.returnPressed.connect(self.button.click)

        self.result = QLabel("")
        font_id = QFontDatabase.addApplicationFont(resource_path("Vazir-Black.ttf"))
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        persian_font = QFont(family, 21)

        self.result.setFont(persian_font)
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setGeometry(20, 480, 400, 200)
        self.result.setStyleSheet("color: white;")
        self.result.setParent(self)

        self.data = pd.DataFrame()
        self.load_data("15-17")
        self.input.setFocus()

    def load_data(self, time_slot):
        if time_slot == "15-17":
            path = resource_path("15.17.xlsx")
        elif time_slot == "17-19":
            path = resource_path("17.19.xlsx")
        else:
            self.result.setText("⚠️ Unknown time slot selected.")
            return

        try:
            self.data = pd.read_excel(path)
        except Exception as e:
            self.result.setText(f"⚠️ Failed to load file: {e}")

    def check_number(self):
        number = self.input.text().strip()[1:]
        phone_list = self.data['Phone'].astype(str).str.strip()

        match = self.data[phone_list == number]

        if not match.empty:
            index = match.index[0]
            name = match.at[index, 'Name']

            self.result.setText(f"✅ {name} عزیز\nخوش اومدی!")
            self.success_sound.play()

        else:
            self.result.setText("❌ متأسفم! اسمتو پیدا نکردیم.")
            self.error_sound.play()

app = QApplication(sys.argv)
window = PhoneCheckerApp()
window.show()
app.exec()
