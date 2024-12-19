import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFrame, QStackedWidget, QLabel, QDialog, QMessageBox, QButtonGroup,
    QLineEdit, QTableWidget, QTableWidgetItem, QComboBox, QInputDialog, QTextEdit, QSizePolicy, QScrollArea
)
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtSvg import QSvgRenderer

# Matplotlib Imports for Embedding Charts
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def load_white_icon(svg_path, size=QSize(20, 20)):
    """
    Loads an SVG icon, renders it to a pixmap, and recolors it to white.
    """
    renderer = QSvgRenderer(svg_path)
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    image = pixmap.toImage()
    width, height = image.width(), image.height()
    for x in range(width):
        for y in range(height):
            pixel = image.pixelColor(x, y)
            if pixel.alpha() > 0:
                image.setPixelColor(x, y, QColor("#ffffff"))

    pixmap = QPixmap.fromImage(image)
    return QIcon(pixmap)

# Define the Product class
class Product:
    def __init__(self, product_id, name, price, quantity, category):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

class UserMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Inventory Management")
        self.setGeometry(100, 100, 1200, 700)

        # Load inventory data
        self.inventory = Inventory()

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Apply global styles
        self.apply_styles()

        # Main Layout
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(5)

        # Initialize Navigational Buttons
        self.nav_buttons = {}
        self.init_sidebar_buttons(sidebar_layout)

        # Spacer to push items to the bottom
        sidebar_layout.addStretch()

        # Initialize Bottom Action Buttons
        self.init_bottom_buttons(sidebar_layout)

        # Add Sidebar to Main Layout
        main_layout.addWidget(sidebar)

        # Main Content Area
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Initialize Modules
        self.init_modules()

        # Connect Buttons to Slots
        self.connect_buttons()

        # Set Home as the default selected button
        self.nav_buttons["Home"].setChecked(True)
        self.switch_page(0)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2d;
                color: #c4c4c4;
                font-family: Arial, Helvetica, sans-serif;
                font-size: 14px;
            }
            QLabel {
                color: #c4c4c4;
            }
            QLabel#titleLabel {
                font-size: 18px;
                color: #00adb5;
                font-weight: bold;
            }
            QLabel#sectionLabel {
                font-size: 16px;
                color: #c4c4c4;
                font-weight: 600;
            }
            QPushButton {
                background-color: transparent;
                color: #ffffff;
                text-align: left;
                padding: 8px 12px;
                border: none;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #495057;
                color: #00adb5;
                border-left: 3px solid #00adb5;
            }
            QPushButton:checked {
                background-color: #495057;
                color: #00adb5;
                border-left: 3px solid #00adb5;
            }
            QFrame {
                background-color: #2b2b3c;
            }
            QStackedWidget {
                background-color: #1e1e2d;
            }
            QTableWidget {
                background-color: #1e1e2d;
                color: #c4c4c4;
                gridline-color: #5a5f66;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #2b2b3c;
                color: #ffffff;
                font-weight: bold;
                border: none;
                padding: 8px;
            }
            QTableWidget::item {
                background-color: #1e1e2d;
                padding: 5px;
            }
            QTableWidget::item:alternate {
                background-color: #242636;
            }
            QTableWidget::item:selected {
                background-color: #323544;
            }
            QLineEdit, QComboBox {
                background-color: #2b2b3c;
                color: #ffffff;
                border: 1px solid #5a5f66;
                padding: 5px;
                border-radius: 5px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #00adb5;
            }
            QPushButton#primaryButton {
                background-color: #00adb5;
                color: #ffffff;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton#primaryButton:hover {
                background-color: #007f8b;
            }
            QDialog {
                background-color: #1e1e2d;
                color: #c4c4c4;
            }
            QMessageBox {
                background-color: #1e1e2d;
                color: #c4c4c4;
            }
        """)

    def init_sidebar_buttons(self, layout):
        # Define button labels and corresponding icon paths
        button_info = [
            ("Home", "icons/home.svg"),
            ("View Products", "icons/view_products.svg"),
            ("Sort Products", "icons/sort.svg"),
            ("Search Products", "icons/search.svg"),
            ("Reports", "icons/reports.svg"),
        ]

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for label, icon_path in button_info:
            btn = QPushButton(f"  {label}")
            btn.setFixedHeight(45)
            btn.setIcon(load_white_icon(icon_path))
            btn.setIconSize(QSize(24, 24))
            btn.setCheckable(True)
            self.button_group.addButton(btn)
            btn.setStyleSheet("QPushButton { text-align: left; }")
            layout.addWidget(btn)
            self.nav_buttons[label] = btn

    def init_bottom_buttons(self, layout):
        # Define bottom button labels and icon paths
        bottom_button_info = [
            ("Contact", "icons/contact.svg"),
        ]

        for label, icon_path in bottom_button_info:
            btn = QPushButton(f"  {label}")
            btn.setFixedHeight(45)
            btn.setIcon(load_white_icon(icon_path))
            btn.setIconSize(QSize(24, 24))
            btn.setCheckable(False)
            btn.setStyleSheet("QPushButton { text-align: left; }")
            layout.addWidget(btn)
            if label == "Contact":
                btn.clicked.connect(self.open_contact)

    def init_modules(self):
        # Initialize each module and add to the stacked widget
        self.home_page = HomePage()
        self.view_products_page = ViewProductsPage(self.inventory)
        self.sort_products_page = SortProductsPage(self.inventory)
        self.search_products_page = SearchProductsPage(self.inventory)
        self.reports_page = ReportsPage(self.inventory)

        # Add widgets to the stack in the same order as buttons
        self.stack.addWidget(self.home_page)              # Index 0 (Home)
        self.stack.addWidget(self.view_products_page)     # Index 1
        self.stack.addWidget(self.sort_products_page)     # Index 2
        self.stack.addWidget(self.search_products_page)   # Index 3
        self.stack.addWidget(self.reports_page)           # Index 4

    def connect_buttons(self):
        # Connect navigational buttons to switch pages
        self.nav_buttons["Home"].clicked.connect(lambda: self.switch_page(0))
        self.nav_buttons["View Products"].clicked.connect(lambda: self.switch_page(1))
        self.nav_buttons["Sort Products"].clicked.connect(lambda: self.switch_page(2))
        self.nav_buttons["Search Products"].clicked.connect(lambda: self.switch_page(3))
        self.nav_buttons["Reports"].clicked.connect(lambda: self.switch_page(4))

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)

    def open_contact(self):
        # Open the Contact Dialog
        contact_dialog = ContactDialog()
        contact_dialog.exec()

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        message = QLabel("Welcome to the User Inventory Management System")
        message.setObjectName("titleLabel")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        layout.addWidget(message)
        layout.addStretch()
        self.setLayout(layout)

class ViewProductsPage(QWidget):
    def __init__(self, inventory):
        super().__init__()
        self.inventory = inventory
        layout = QVBoxLayout()
        title = QLabel("All Products")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Product ID", "Name", "Price", "Quantity", "Category"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_products()

    def load_products(self):
        products = self.inventory.get_products()
        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(str(product.product_id)))
            self.table.setItem(row, 1, QTableWidgetItem(product.name))
            self.table.setItem(row, 2, QTableWidgetItem(f"{product.price:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(str(product.quantity)))
            self.table.setItem(row, 4, QTableWidgetItem(product.category))

class SortProductsPage(QWidget):
    def __init__(self, inventory):
        super().__init__()
        self.inventory = inventory
        layout = QVBoxLayout()

        title = QLabel("Sort Products")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Sorting Options Layout
        sorting_options_layout = QHBoxLayout()

        # Algorithm Selection
        algo_layout = QVBoxLayout()
        algo_label = QLabel("Select Sorting Algorithm:")
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["Quick Sort", "Merge Sort", "Shell Sort"])
        algo_layout.addWidget(algo_label)
        algo_layout.addWidget(self.algo_combo)
        sorting_options_layout.addLayout(algo_layout)

        # Primary Sort Criteria Selection
        primary_layout = QVBoxLayout()
        primary_label = QLabel("Select Primary Sort Criteria:")
        self.primary_combo = QComboBox()
        self.primary_combo.addItems(["Category", "Price", "Name", "Quantity", "Product ID"])
        primary_layout.addWidget(primary_label)
        primary_layout.addWidget(self.primary_combo)
        sorting_options_layout.addLayout(primary_layout)

        # Secondary Sort Criteria Selection
        secondary_layout = QVBoxLayout()
        secondary_label = QLabel("Select Secondary Sort Criteria:")
        self.secondary_combo = QComboBox()
        self.secondary_combo.addItems(["None", "Category", "Price", "Name", "Quantity", "Product ID"])
        secondary_layout.addWidget(secondary_label)
        secondary_layout.addWidget(self.secondary_combo)
        sorting_options_layout.addLayout(secondary_layout)

        layout.addLayout(sorting_options_layout)

        self.sort_button = QPushButton("Sort")
        self.sort_button.setObjectName("primaryButton")
        self.sort_button.clicked.connect(self.sort_products)
        layout.addWidget(self.sort_button)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Product ID", "Name", "Price", "Quantity", "Category"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_products()

    def load_products(self):
        products = self.inventory.get_products()
        self.display_products(products)

    def sort_products(self):
        algorithm = self.algo_combo.currentText()
        primary_key = self.primary_combo.currentText().lower().replace(" ", "_")
        secondary_key = self.secondary_combo.currentText().lower().replace(" ", "_")
        products = self.inventory.get_products()

        sort_keys = [primary_key]
        if secondary_key != "none":
            sort_keys.append(secondary_key)

        # Decide sorting function
        if algorithm == "Quick Sort":
            sorted_products = self.inventory.quick_sort(products.copy(), sort_keys)
        elif algorithm == "Merge Sort":
            sorted_products = self.inventory.merge_sort(products.copy(), sort_keys)
        elif algorithm == "Shell Sort":
            sorted_products = self.inventory.shell_sort(products.copy(), sort_keys)
        else:
            sorted_products = products

        self.display_products(sorted_products)

    def display_products(self, products):
        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(str(product.product_id)))
            self.table.setItem(row, 1, QTableWidgetItem(product.name))
            self.table.setItem(row, 2, QTableWidgetItem(f"{product.price:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(str(product.quantity)))
            self.table.setItem(row, 4, QTableWidgetItem(product.category))

class SearchProductsPage(QWidget):
    def __init__(self, inventory):
        super().__init__()
        self.inventory = inventory

        layout = QVBoxLayout()

        title = QLabel("Search Products")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        algo_layout = QHBoxLayout()
        algo_layout.addWidget(QLabel("Select Search Algorithm:"))

        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["Linear Search", "Binary Search"])
        algo_layout.addWidget(self.algo_combo)
        layout.addLayout(algo_layout)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter Product ID to search")
        self.search_button = QPushButton("Search")
        self.search_button.setObjectName("primaryButton")
        self.search_button.clicked.connect(self.search_product)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        layout.addLayout(search_layout)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels(["Product ID", "Name", "Price", "Quantity", "Category"])
        self.result_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.result_table)

        self.setLayout(layout)

    def search_product(self):
        try:
            product_id = int(self.search_input.text())
            algorithm = self.algo_combo.currentText()
            products = self.inventory.get_products()
            if algorithm == "Binary Search":
                # Ensure the list is sorted by product_id
                sorted_products = sorted(products, key=lambda x: x.product_id)
                product = self.inventory.recursive_binary_search(sorted_products, product_id, 0, len(sorted_products) - 1)
            elif algorithm == "Linear Search":
                product = self.inventory.linear_search(products, product_id)
            else:
                product = None

            if product:
                self.display_product(product)
            else:
                QMessageBox.information(self, "Not Found", "Product not found.")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid Product ID.")

    def display_product(self, product):
        self.result_table.setRowCount(1)
        self.result_table.setItem(0, 0, QTableWidgetItem(str(product.product_id)))
        self.result_table.setItem(0, 1, QTableWidgetItem(product.name))
        self.result_table.setItem(0, 2, QTableWidgetItem(f"{product.price:.2f}"))
        self.result_table.setItem(0, 3, QTableWidgetItem(str(product.quantity)))
        self.result_table.setItem(0, 4, QTableWidgetItem(product.category))

class ReportsPage(QWidget):
    def __init__(self, inventory):
        super().__init__()
        self.inventory = inventory
        layout = QVBoxLayout()

        title = QLabel("Reports")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Count Products by Category
        count_layout = QHBoxLayout()
        self.count_button = QPushButton("Count Products in Category")
        self.count_button.setObjectName("primaryButton")
        self.count_button.clicked.connect(self.count_category)
        count_layout.addWidget(self.count_button)
        layout.addLayout(count_layout)

        self.count_result = QLabel("")
        self.count_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.count_result)

        # Calculate Total Inventory Value
        value_layout = QHBoxLayout()
        self.value_button = QPushButton("Calculate Total Inventory Value")
        self.value_button.setObjectName("primaryButton")
        self.value_button.clicked.connect(self.calculate_value)
        value_layout.addWidget(self.value_button)
        layout.addLayout(value_layout)

        self.value_result = QLabel("")
        self.value_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_result)

        # Visualization Buttons
        viz_layout = QHBoxLayout()
        self.category_chart_button = QPushButton("Show Category Distribution")
        self.category_chart_button.setObjectName("primaryButton")
        self.category_chart_button.clicked.connect(self.show_category_chart)
        viz_layout.addWidget(self.category_chart_button)

        self.quantity_chart_button = QPushButton("Show Quantity Distribution")
        self.quantity_chart_button.setObjectName("primaryButton")
        self.quantity_chart_button.clicked.connect(self.show_quantity_chart)
        viz_layout.addWidget(self.quantity_chart_button)

        layout.addLayout(viz_layout)

        # Canvas for Charts
        self.chart_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.chart_canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.chart_canvas.updateGeometry()
        layout.addWidget(self.chart_canvas)

        self.setLayout(layout)

    def count_category(self):
        category, ok = QInputDialog.getText(self, "Category Input", "Enter the category name:")
        if ok and category:
            count = self.inventory.count_products_in_category(self.inventory.products, category)
            self.count_result.setText(f"Total products in '{category}': {count}")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid category name.")

    def calculate_value(self):
        total = self.inventory.calculate_total_value(self.inventory.products)
        self.value_result.setText(f"Total Inventory Value: Rs.{total:.2f}")

    def show_category_chart(self):
        category_counts = self.inventory.get_category_counts()
        categories = list(category_counts.keys())
        counts = list(category_counts.values())

        self.chart_canvas.figure.clear()
        ax = self.chart_canvas.figure.add_subplot(111)
        ax.bar(categories, counts, color='#00adb5')
        ax.set_title('Number of Products per Category')
        ax.set_xlabel('Category')
        ax.set_ylabel('Number of Products')
        ax.tick_params(axis='x', rotation=45)
        self.chart_canvas.draw()

    def show_quantity_chart(self):
        category_quantities = self.inventory.get_category_quantities()
        categories = list(category_quantities.keys())
        quantities = list(category_quantities.values())

        self.chart_canvas.figure.clear()
        ax = self.chart_canvas.figure.add_subplot(111)
        ax.bar(categories, quantities, color='#00adb5')
        ax.set_title('Total Quantity per Category')
        ax.set_xlabel('Category')
        ax.set_ylabel('Total Quantity')
        ax.tick_params(axis='x', rotation=45)
        self.chart_canvas.draw()

class ContactDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contact Us")
        self.setFixedSize(450, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #343a40; 
                border-radius: 10px;
                color: #f8f9fa;
                font-family: "Arial", sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #f8f9fa;
                padding: 10px;
            }
            QLabel#title {
                font-size: 22px;
                font-weight: bold;
                color: #17a2b8;
            }
            QLabel#footer {
                font-size: 12px;
                color: #adb5bd;
                padding: 10px;
            }
        """)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel("Contact Us")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))

        contact_info = QLabel(
            "For support, reach out to us:\n\n"
            "📧 Email: support@example.com\n"
            "📞 Phone: +1 234 567 8900\n"
            "🏢 Address: 123 Main Street\n"
            "City, Country"
        )
        contact_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contact_info.setWordWrap(True)

        footer_label = QLabel("We are here to help you 24/7.")
        footer_label.setObjectName("footer")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_label)
        layout.addWidget(contact_info)
        layout.addStretch()
        layout.addWidget(footer_label)

        self.setLayout(layout)

class Inventory:
    def __init__(self):
        self.products = self.load_data()

    def load_data(self):
        import json
        import os
        products = []
        try:
            # Get the directory two levels up from the current file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            BASE_DIR = os.path.abspath(os.path.join(script_dir, '..', '..'))
            backup_file = os.path.join(BASE_DIR, 'backup.json')

            print(f"Looking for backup.json at: {backup_file}")

            if not os.path.exists(backup_file):
                print(f"backup.json not found at {backup_file}")
                return []

            with open(backup_file, 'r') as f:
                data = json.load(f)

                # Load products
                products_data = data.get('products', [])
                print(f"Found {len(products_data)} products.")

                # Load batches
                batches_data = data.get('batches', [])
                print(f"Found {len(batches_data)} batches.")

                # Calculate total quantity per product_id from batches
                quantity_map = {}
                for batch in batches_data:
                    pid = batch.get('product_id')
                    qty = batch.get('quantity', 0)
                    if pid in quantity_map:
                        quantity_map[pid] += qty
                    else:
                        quantity_map[pid] = qty

                # Process each product
                for item in products_data:
                    product_id = item.get('product_id')
                    unit_price = item.get('unit_price')
                    quantity = quantity_map.get(product_id, 0)  # Get total quantity from batches

                    print(f"Loading Product ID: {product_id}, Price: {unit_price}, Quantity: {quantity}")

                    # Handle missing or null 'unit_price'
                    if unit_price is None:
                        print(f"Unit price is missing for Product ID {product_id}. Setting default price to 0.0.")
                        unit_price = 0.0

                    # Ensure correct data types
                    try:
                        product_id = int(product_id) if product_id is not None else 0
                        name = item.get('name', '')
                        price = float(unit_price)
                        quantity = int(quantity)
                        category = item.get('category', '')
                    except (ValueError, TypeError) as e:
                        print(f"Data type conversion error for Product ID {product_id}: {e}")
                        continue  # Skip this product

                    product = Product(
                        product_id=product_id,
                        name=name,
                        price=price,
                        quantity=quantity,
                        category=category
                    )
                    products.append(product)

        except FileNotFoundError:
            print("backup.json file not found.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return products

    def get_products(self):
        return self.products

    def quick_sort(self, arr, keys):
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0]
            less = []
            greater = []
            for item in arr[1:]:
                if self.compare_products(item, pivot, keys) < 0:
                    less.append(item)
                else:
                    greater.append(item)
            return self.quick_sort(less, keys) + [pivot] + self.quick_sort(greater, keys)

    def merge_sort(self, arr, keys):
        if len(arr) > 1:
            mid = len(arr) // 2
            left_half = self.merge_sort(arr[:mid], keys)
            right_half = self.merge_sort(arr[mid:], keys)
            return self.merge(left_half, right_half, keys)
        else:
            return arr

    def shell_sort(self, arr, keys):
        n = len(arr)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and self.compare_products(arr[j - gap], temp, keys) > 0:
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2
        return arr

    def merge(self, left, right, keys):
        result = []
        while left and right:
            if self.compare_products(left[0], right[0], keys) <= 0:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result.extend(left or right)
        return result

    def compare_products(self, a, b, keys):
        for key in keys:
            a_value = getattr(a, key)
            b_value = getattr(b, key)
            if isinstance(a_value, str) and isinstance(b_value, str):
                a_value = a_value.lower()
                b_value = b_value.lower()
            if a_value < b_value:
                return -1
            elif a_value > b_value:
                return 1
        return 0

    def recursive_binary_search(self, arr, target_id, low, high):
        if high >= low:
            mid = (high + low) // 2
            if arr[mid].product_id == target_id:
                return arr[mid]
            elif arr[mid].product_id > target_id:
                return self.recursive_binary_search(arr, target_id, low, mid - 1)
            else:
                return self.recursive_binary_search(arr, target_id, mid + 1, high)
        else:
            return None

    def linear_search(self, arr, target_id):
        for item in arr:
            if item.product_id == target_id:
                return item
        return None

    def count_products_in_category(self, products, category):
        if not products:
            return 0
        count = self.count_products_in_category(products[1:], category)
        if products[0].category.lower() == category.lower():
            return 1 + count
        else:
            return count

    def calculate_total_value(self, products):
        if not products:
            return 0.0
        total = self.calculate_total_value(products[1:])
        return (products[0].price * products[0].quantity) + total

    def get_category_counts(self):
        category_counts = {}
        for product in self.products:
            cat = product.category
            category_counts[cat] = category_counts.get(cat, 0) + 1
        return category_counts

    def get_category_quantities(self):
        category_quantities = {}
        for product in self.products:
            cat = product.category
            category_quantities[cat] = category_quantities.get(cat, 0) + product.quantity
        return category_quantities

def run_user_app():
    app = QApplication(sys.argv)
    window = UserMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_user_app()