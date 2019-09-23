import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import add_product, add_member
from PIL import Image

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
        self.display_members()

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
        self.products_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.products_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)  # Prevents user resizing columns
        self.products_table.doubleClicked.connect(self.selected_product)

        ##### Right Top Layout Widgets #####
        self.search_text = QLabel("Search")
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Search For Products")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_products)

        ##### Right Middle Layout Widgets #####
        self.all_products = QRadioButton("All Products")
        self.available_products = QRadioButton("Available")
        self.not_available_products = QRadioButton("Not Available")
        self.list_button = QPushButton("List")
        self.list_button.clicked.connect(self.list_products)

        ########################
        ##### Tab2 Widgets #####
        ########################

        self.members_table = QTableWidget()
        self.members_table.setColumnCount(4)
        self.members_table.setHorizontalHeaderItem(0, QTableWidgetItem("Member ID"))
        self.members_table.setHorizontalHeaderItem(1, QTableWidgetItem("Member Name"))
        self.members_table.setHorizontalHeaderItem(2, QTableWidgetItem("Member Surname"))
        self.members_table.setHorizontalHeaderItem(3, QTableWidgetItem("Phone"))
        self.members_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.members_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.members_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.members_table.doubleClicked.connect(self.selected_member)
        self.member_search_text = QLabel("Search Members")
        self.member_search_entry = QLineEdit()
        self.member_search_button = QPushButton("Search")
        self.member_search_button.clicked.connect(self.search_members)

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

        self.member_left_layout.addWidget(self.members_table)
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

    def display_members(self):
        self.members_table.setFont(QFont("Arial", 12))
        for i in reversed(range(self.members_table.rowCount())):
            self.members_table.removeRow(i)

        query = cur.execute("SELECT * FROM member")
        for row_data in query:
            row_number = self.members_table.rowCount()
            self.members_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.members_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.members_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def selected_product(self):
        global product_id
        product_list = []
        for i in range(0, 6):
            product_list.append(self.products_table.item(self.products_table.currentRow(), i).text())

        product_id = product_list[0]
        self.display = DisplayProduct()
        self.display.show()

    def selected_member(self):
        global member_id
        member_list = []
        for i in range(0, 4):
            member_list.append(self.members_table.item(self.members_table.currentRow(), i).text())

        member_id = member_list[0]
        self.display_member = DisplayMember()
        self.display_member.show()

    def search_products(self):
        value = self.search_entry.text()
        if value == "":
            QMessageBox.information(self, "Warning", "Search query cannot be empty!")
        else:
            self.search_entry.setText("")

            query = "SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_availability " \
                    "FROM product WHERE product_name LIKE ? OR product_manufacturer LIKE ?"
            results = cur.execute(query, ("%" + value + "%", "%" + value + "%")).fetchall()

            if results == []:
                QMessageBox.information(self, "Warning", "There is no such product or manufacturer")
            else:
                for i in reversed(range(self.products_table.rowCount())):
                    self.products_table.removeRow(i)  # clear table
                for row_data in results:
                    row_number = self.products_table.rowCount()
                    self.products_table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.products_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def search_members(self):
        value = self.member_search_entry.text()
        if value == "":
            QMessageBox.information(self, "Warning", "Search query cannot be empty!")
        else:
            self.member_search_entry.setText("")

            query = "SELECT * FROM member WHERE member_name LIKE ? OR member_surname LIKE ? OR member_phone LIKE ?"
            results = cur.execute(query, ("%" + value + "%", "%" + value + "%", "%" + value + "%")).fetchall()

            if results == []:
                QMessageBox.information(self, "Warning", "There is no such member")
            else:
                for i in reversed(range(self.members_table.rowCount())):
                    self.members_table.removeRow(i)  # clear table
                for row_data in results:
                    row_number = self.members_table.rowCount()
                    self.members_table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.members_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def list_products(self):
        if self.all_products.isChecked():
            self.display_products()
        elif self.available_products.isChecked():
            query = "SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_availability " \
                    "FROM product WHERE product_availability = 'Available' "
            products = cur.execute(query).fetchall()
            for i in reversed(range(self.products_table.rowCount())):
                self.products_table.removeRow(i)  # clear table
            for row_data in products:
                row_number = self.products_table.rowCount()
                self.products_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.products_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        elif self.not_available_products.isChecked():
            query = "SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_availability " \
                    "FROM product WHERE product_availability = 'Unavailable' "
            products = cur.execute(query).fetchall()
            for i in reversed(range(self.products_table.rowCount())):
                self.products_table.removeRow(i)  # clear table
            for row_data in products:
                row_number = self.products_table.rowCount()
                self.products_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.products_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


class DisplayMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Member Details")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(500, 200, 350, 600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.member_details()
        self.widgets()
        self.layouts()

    def member_details(self):
        global member_id
        query = "SELECT * FROM member WHERE member_id = ?"
        member = cur.execute(query, (member_id, )).fetchone()
        self.member_name = member[1]
        self.member_surname = member[2]
        self.member_phone = member[3]

    def widgets(self):
        ##### Top Layout Widgets #####
        self.member_img = QLabel()
        self.img = QPixmap("icons/members.png")
        self.member_img.setPixmap(self.img)
        self.member_img.setAlignment(Qt.AlignCenter)
        self.title_text = QLabel("Display Member")
        self.title_text.setAlignment(Qt.AlignCenter)

        ##### Bottom Layout Widgets #####
        self.name_entry = QLineEdit()
        self.name_entry.setText(self.member_name)
        self.surname_entry = QLineEdit()
        self.surname_entry.setText(self.member_surname)
        self.phone_entry = QLineEdit()
        self.phone_entry.setText(self.member_phone)
        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self.update_member)
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_member)

    def layouts(self):
        self.main_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        self.bottom_layout = QFormLayout()
        self.top_frame = QFrame()
        self.bottom_frame = QFrame()

        ##### Add Widgets #####
        self.top_layout.addWidget(self.title_text)
        self.top_layout.addWidget(self.member_img)
        self.top_frame.setLayout(self.top_layout)
        self.bottom_layout.addRow(QLabel("Name:"), self.name_entry)
        self.bottom_layout.addRow(QLabel("Surname:"), self.surname_entry)
        self.bottom_layout.addRow(QLabel("Phone:"), self.phone_entry)
        self.bottom_layout.addRow(QLabel(""), self.update_btn)
        self.bottom_layout.addRow(QLabel(""), self.delete_btn)
        self.bottom_frame.setLayout(self.bottom_layout)
        self.main_layout.addWidget(self.top_frame)
        self.main_layout.addWidget(self.bottom_frame)

        self.setLayout(self.main_layout)

    def update_member(self):
        global member_id
        name = self.name_entry.text()
        surname = self.surname_entry.text()
        phone = self.phone_entry.text()

        if name and surname and phone != "":
            try:
                query = "UPDATE member SET member_name = ?, member_surname = ?, member_phone = ? WHERE member_id = ?"
                cur.execute(query, (name, surname, phone, member_id))
                con.commit()
                QMessageBox.information(self, "Info", "Member has been updated")
                con.close()
                self.close()
            except:
                QMessageBox.information(self, "Warning", "Member has not been updated")
        else:
            QMessageBox.information(self, "Warning", "Fields cannot be empty")

    def delete_member(self):
        global member_id
        mbox = QMessageBox.question(self, "Warning", "Are you sure you want to delete this member?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if mbox == QMessageBox.Yes:
            try:
                query = "DELETE FROM member WHERE member_id = ?"
                cur.execute(query, (member_id,))
                con.commit()
                QMessageBox.information(self, "Info", "Member has been deleted")
                self.close()
            except:
                QMessageBox.information(self, "Info", "Member has not been deleted")


class DisplayProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Product Details")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(500, 200, 350, 600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.product_details()
        self.widgets()
        self.layouts()

    def product_details(self):
        global product_id
        query = "SELECT * FROM product WHERE product_id = ?"
        product = cur.execute(query, (product_id, )).fetchone()  # single item tuple = (1, )
        self.product_name = product[1]
        self.product_manufacturer = product[2]
        self.product_price = product[3]
        self.product_quota = product[4]
        self.product_img = product[5]
        self.product_status = product[6]

    def widgets(self):
        ##### Top Layout Widgets #####
        self.product_image = QLabel()
        self.img = QPixmap("images/{}".format(self.product_img))
        self.product_image.setPixmap(self.img)
        self.product_image.setAlignment(Qt.AlignCenter)
        self.title_text = QLabel("Update Product")
        self.title_text.setAlignment(Qt.AlignCenter)

        ##### Bottom Layout Widgets #####
        self.name_entry = QLineEdit()
        self.name_entry.setText(self.product_name)
        self.manufacturer_entry = QLineEdit()
        self.manufacturer_entry.setText(self.product_manufacturer)
        self.price_entry = QLineEdit()
        self.price_entry.setText(str(self.product_price))  # cast to string
        self.quota_entry = QLineEdit()
        self.quota_entry.setText(str(self.product_quota))  # cast to string
        self.availability_combo = QComboBox()
        self.availability_combo.addItems(["Available", "Unavailable"])
        self.upload_btn = QPushButton("Upload")
        self.upload_btn.clicked.connect(self.upload_img)
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_product)
        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self.update_product)

    def layouts(self):
        self.main_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        self.bottom_layout = QFormLayout()
        self.top_frame = QFrame()
        self.bottom_frame = QFrame()

        ##### Add Widgets #####
        self.top_layout.addWidget(self.title_text)
        self.top_layout.addWidget(self.product_image)
        self.top_frame.setLayout(self.top_layout)
        self.bottom_layout.addRow(QLabel("Name:"), self.name_entry)
        self.bottom_layout.addRow(QLabel("Manufacturer:"), self.manufacturer_entry)
        self.bottom_layout.addRow(QLabel("Price:"), self.price_entry)
        self.bottom_layout.addRow(QLabel("Quota:"), self.quota_entry)
        self.bottom_layout.addRow(QLabel("Status:"), self.availability_combo)
        self.bottom_layout.addRow(QLabel("Image:"), self.upload_btn)
        self.bottom_layout.addRow(QLabel(""), self.delete_btn)
        self.bottom_layout.addRow(QLabel(""), self.update_btn)
        self.bottom_frame.setLayout(self.bottom_layout)
        self.main_layout.addWidget(self.top_frame)
        self.main_layout.addWidget(self.bottom_frame)

        self.setLayout(self.main_layout)

    def upload_img(self):
        size = (256, 256)
        self.file_name, ok = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.jpg *.png)")
        if ok:
            self.product_image = os.path.basename(self.file_name)
            img = Image.open(self.file_name)
            img = img.resize(size)
            img.save("images/{}".format(self.product_image))

    def update_product(self):
        global product_id
        name = self.name_entry.text()
        manufacturer = self.manufacturer_entry.text()
        price = int(self.price_entry.text())  # cast to int
        quota = int(self.quota_entry.text())  # cast to int
        status = self.availability_combo.currentText()
        default_image = self.product_image

        if name and manufacturer and price and quota != "":
            try:
                query = "UPDATE product SET product_name = ?, product_manufacturer = ?, product_price = ?, " \
                        "product_quota = ?, product_img = ?, product_availability = ? WHERE product_id = ?"
                cur.execute(query, (name, manufacturer, price, quota, default_image, status, product_id))
                con.commit()
                QMessageBox.information(self, "Info", "Product has been updated")
                con.close()
                self.close()
            except:
                QMessageBox.information(self, "Warning", "Product has not been updated")
        else:
            QMessageBox.information(self, "Warning", "Fields cannot be empty")

    def delete_product(self):
        global product_id
        mbox = QMessageBox.question(self, "Warning", "Are you sure you want to delete this product?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if mbox == QMessageBox.Yes:
            try:
                query = "DELETE FROM product WHERE product_id = ?"
                cur.execute(query, (product_id,))
                con.commit()
                QMessageBox.information(self, "Info", "Product has been deleted")
                self.close()
            except:
                QMessageBox.information(self, "Warning", "Product has not been deleted")


def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()