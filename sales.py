from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3

con = sqlite3.connect("product.db")
cur = con.cursor()

class SellProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Sell Products")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(500, 200, 350, 600)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ##### Widgets - Top Layout #####
        self.sell_product_img = QLabel()
        self.img = QPixmap("icons/shop.png")
        self.sell_product_img.setPixmap(self.img)
        self.sell_product_img.setAlignment(Qt.AlignCenter)
        self.title_text = QLabel("Sell Products")
        self.title_text.setAlignment(Qt.AlignCenter)

        ##### Widgets - Bottom Layout #####
        self.product_combo = QComboBox()
        self.product_combo.currentIndexChanged.connect(self.change_combo_value)
        self.member_combo = QComboBox()
        self.quantity_combo = QComboBox()
        self.submit_btn = QPushButton("Submit")
        #self.submit_btn.clicked.connect(self.sell_product)

        query1 = "SELECT * FROM product WHERE product_availability = ?"
        products = cur.execute(query1, ("Available",)).fetchall()
        query2 = "SELECT member_id, member_name FROM member"
        members = cur.execute(query2).fetchall()
        quantity = products[0][4]

        for product in products:
            self.product_combo.addItem(product[1], product[0])  # product_id as hidden value

        for member in members:
            self.member_combo.addItem(member[1], member[0])

        for i in range(1, quantity + 1):
            self.quantity_combo.addItem(str(i))

    def layouts(self):
        self.main_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        self.bottom_layout = QFormLayout()
        self.top_frame = QFrame()
        self.bottom_frame = QFrame()

        ##### Add Widgets #####
        ##### Top Layout Widgets #####
        self.top_layout.addWidget(self.title_text)
        self.top_layout.addWidget(self.sell_product_img)
        self.top_frame.setLayout(self.top_layout)

        ##### Bottom Layout Widgets #####
        self.bottom_layout.addRow(QLabel("Product: "), self.product_combo)
        self.bottom_layout.addRow(QLabel("Member: "), self.member_combo)
        self.bottom_layout.addRow(QLabel("Quantity: "), self.quantity_combo)
        self.bottom_layout.addRow(QLabel(""), self.submit_btn)
        self.bottom_frame.setLayout(self.bottom_layout)

        self.main_layout.addWidget(self.top_frame)
        self.main_layout.addWidget(self.bottom_frame)

        self.setLayout(self.main_layout)

    def change_combo_value(self):
        self.quantity_combo.clear()
        product_id = self.product_combo.currentData()
        query = "SELECT product_quota FROM product WHERE product_id = ?"
        quota = cur.execute(query, (product_id, )).fetchone()

        for i in range(1, quota[0] + 1):
            self.quantity_combo.addItem(str(i))

