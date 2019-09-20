import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import add_product, add_member

con = sqlite3.connect("product.db")
cur = con.cursor()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Product Manager")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450, 150, 1350, 750)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.tool_bar()
        self.tab_widget()
        self.widgets()
        self.layouts()
        self.display_products()

    def tool_bar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        ##### Toolbar Buttons #####

        ##### Add Product #########
        self.add_product = QAction(QIcon("icons/add.png"), "Add Product", self)
        self.tb.addAction(self.add_product)
        self.add_product.triggered.connect(self.func_add_product)
        self.tb.addSeparator()

        ##### Add Member ##########
        self.add_member = QAction(QIcon("icons/addmember.png"), "Add Member", self)
        self.tb.addAction(self.add_member)
        self.add_member.triggered.connect(self.func_add_member)
        self.tb.addSeparator()

        ##### Add Member ##########
        self.sell_product = QAction(QIcon("icons/sell.png"), "Sell Product", self)
        self.tb.addAction(self.sell_product)
        self.tb.addSeparator()

    def tab_widget(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab1, "Products")
        self.tabs.addTab(self.tab2, "Members")
        self.tabs.addTab(self.tab3, "Statistics")

    def widgets(self):
        ########################
        ##### Tab1 Widgets #####
        ########################

        ##### Main Left Layout Widget #####
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(6)
        self.products_table.setColumnHidden(0, True)
        self.products_table.setHorizontalHeaderItem(0, QTableWidgetItem("Product Id"))
        self.products_table.setHorizontalHeaderItem(1, QTableWidgetItem("Product Name"))
        self.products_table.setHorizontalHeaderItem(2, QTableWidgetItem("Manufacturer"))
        self.products_table.setHorizontalHeaderItem(3, QTableWidgetItem("Price"))
        self.products_table.setHorizontalHeaderItem(4, QTableWidgetItem("Quota"))
        self.products_table.setHorizontalHeaderItem(5, QTableWidgetItem("Availability"))

        ##### Right Top Layout Widgets #####
        self.search_text = QLabel("Search")
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Search For Products")
        self.search_button = QPushButton("Search")

        ##### Right Middle Layout Widgets #####
        self.all_products = QRadioButton("All Products")
        self.available_products = QRadioButton("Available")
        self.not_available_products = QRadioButton("Not Available")
        self.list_button = QPushButton("List")

        ########################
        ##### Tab2 Widgets #####
        ########################

        self.members_table_widget = QTableWidget()
        self.members_table_widget.setColumnCount(4)
        self.members_table_widget.setHorizontalHeaderItem(0, QTableWidgetItem("Member ID"))
        self.members_table_widget.setHorizontalHeaderItem(1, QTableWidgetItem("Member Name"))
        self.members_table_widget.setHorizontalHeaderItem(2, QTableWidgetItem("Member Surname"))
        self.members_table_widget.setHorizontalHeaderItem(3, QTableWidgetItem("Phone"))
        self.member_search_text = QLabel("Search Members")
        self.member_search_entry = QLineEdit()
        self.member_search_button = QPushButton("Search")

    def layouts(self):
        ########################
        ##### Tab1 layouts #####
        ########################

        self.main_layout = QHBoxLayout()
        self.main_left_layout = QVBoxLayout()
        self.main_right_layout = QVBoxLayout()
        self.right_top_layout = QHBoxLayout()
        self.right_middle_layout = QHBoxLayout()
        self.top_group_box = QGroupBox("Search box")
        self.middle_group_box = QGroupBox("List Box")

        ##### Add Widgets #####
        ##### Add Left Main Layout Widgets #####
        self.main_left_layout.addWidget(self.products_table)

        ##### Right Top Layout Widgets #####
        self.right_top_layout.addWidget(self.search_text)
        self.right_top_layout.addWidget(self.search_entry)
        self.right_top_layout.addWidget(self.search_button)
        self.top_group_box.setLayout(self.right_top_layout)

        ##### Right Middle Layout Widgets #####
        self.right_middle_layout.addWidget(self.all_products)
        self.right_middle_layout.addWidget(self.available_products)
        self.right_middle_layout.addWidget(self.not_available_products)
        self.right_middle_layout.addWidget(self.list_button)
        self.middle_group_box.setLayout(self.right_middle_layout)

        self.main_right_layout.addWidget(self.top_group_box)
        self.main_right_layout.addWidget(self.middle_group_box)
        self.main_layout.addLayout(self.main_left_layout, 70)
        self.main_layout.addLayout(self.main_right_layout, 30)
        self.tab1.setLayout(self.main_layout)

        ########################
        ##### Tab2 layouts #####
        ########################

        self.member_main_layout = QHBoxLayout()
        self.member_left_layout = QHBoxLayout()
        self.member_right_layout = QHBoxLayout()
        self.member_right_group_box = QGroupBox("Search For Members")
        self.member_right_group_box.setContentsMargins(10, 10, 10, 550)
        self.member_right_layout.addWidget(self.member_search_text)
        self.member_right_layout.addWidget(self.member_search_entry)
        self.member_right_layout.addWidget(self.member_search_button)
        self.member_right_group_box.setLayout(self.member_right_layout)

        self.member_left_layout.addWidget(self.members_table_widget)
        self.member_main_layout.addLayout(self.member_left_layout, 70)
        self.member_main_layout.addWidget(self.member_right_group_box, 30)
        self.tab2.setLayout(self.member_main_layout)

    def func_add_product(self):
        self.new_product = add_product.AddProduct()

    def func_add_member(self):
        self.new_member = add_member.AddMember()

    def display_products(self):
        self.products_table.setFont(QFont("Arial", 12))
        for i in reversed(range(self.products_table.rowCount())):
            self.products_table.removeRow(i)

        query = cur.execute("SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_availability FROM product")
        for row_data in query:
            row_number = self.products_table.rowCount()
            self.products_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.products_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.products_table.setEditTriggers(QAbstractItemView.NoEditTriggers) # prevents user editing table

def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()