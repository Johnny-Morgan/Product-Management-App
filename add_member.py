from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3

con = sqlite3.connect("product.db")
cur = con.cursor()


class AddMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Add Member")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450, 150, 400, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ##### Widgets - Top Layout #####
        self.add_member_img = QLabel()
        self.img = QPixmap("icons/addmember.png")
        self.add_member_img.setPixmap(self.img)
        self.add_member_img.setAlignment(Qt.AlignCenter)
        self.title_text = QLabel("Add Member")
        self.title_text.setAlignment(Qt.AlignCenter)

        ##### Widgets - Bottom Layout #####
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("Enter name of member")
        self.surname_entry = QLineEdit()
        self.surname_entry.setPlaceholderText("Enter surname of member")
        self.phone_entry = QLineEdit()
        self.phone_entry.setPlaceholderText("Enter phone number")
        self.submit_btn = QPushButton("Submit")

    def layouts(self):
        self.main_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        self.bottom_layout = QFormLayout()
        self.top_frame = QFrame()
        self.bottom_frame = QFrame()

        ##### Add Widgets #####
        ##### Top Layout Widgets #####
        self.top_layout.addWidget(self.title_text)
        self.top_layout.addWidget(self.add_member_img)
        self.top_frame.setLayout(self.top_layout)

        ##### Bottom Layout Widgets #####
        self.bottom_layout.addRow(QLabel("Name: "), self.name_entry)
        self.bottom_layout.addRow(QLabel("Surname: "), self.surname_entry)
        self.bottom_layout.addRow(QLabel("Pjone: "), self.phone_entry)
        self.bottom_layout.addRow(QLabel(""), self.submit_btn)
        self.bottom_frame.setLayout(self.bottom_layout)

        self.main_layout.addWidget(self.top_frame)
        self.main_layout.addWidget(self.bottom_frame)

        self.setLayout(self.main_layout)
