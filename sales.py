from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


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
        self.member_combo = QComboBox()
        self.quantity_combo = QComboBox()
        self.submit_btn = QPushButton("Submit")
        #self.submit_btn.clicked.connect(self.sell_product)

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

