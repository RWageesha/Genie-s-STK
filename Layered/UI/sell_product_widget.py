from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QDialogButtonBox, QTextEdit, QHeaderView
)
from PyQt6.QtGui import QIntValidator, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter

from domain.domain_models import Product, SaleRecord
from typing import List
from datetime import date

import win32print
import win32ui

from PyQt6.QtGui import QKeySequence, QShortcut  # Add QShortcut import

class BillDialog(QDialog):
    def __init__(self, bill_text: str, send_to_printer_callback):
        super().__init__()
        self.send_to_printer_callback = send_to_printer_callback
        self.setWindowTitle("Sale Bill")
        self.setMinimumSize(400, 500)

        layout = QVBoxLayout()

        # Text area to display the bill
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(bill_text)
        layout.addWidget(self.text_edit)

        # Dialog buttons
        button_box = QDialogButtonBox()
        print_button = button_box.addButton("Print", QDialogButtonBox.ButtonRole.ActionRole)
        close_button = button_box.addButton(QDialogButtonBox.StandardButton.Close)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        close_button.clicked.connect(self.reject)
        print_button.clicked.connect(self.print_bill)

        layout.addWidget(button_box)
        self.setLayout(layout)

        self.apply_dialog_styles()

    def apply_dialog_styles(self):
        # Apply modern UI design based on the guidelines
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2d; 
                color: #c4c4c4; 
                font-family: "Roboto"; 
                font-size: 14px;
            }

            QTextEdit {
                background-color: #2b2b3c; 
                color: #ffffff;
                border: 1px solid #5a5f66; 
            }

            QDialogButtonBox QPushButton {
                background-color: #00adb5; 
                color: #ffffff; 
                border-radius: 5px; 
                padding: 8px 12px; 
                font-weight: bold;
            }

            QDialogButtonBox QPushButton:hover {
                background-color: #007f8b;
            }
        """)

    def print_bill(self):
        """
        Sends the bill_text directly to the thermal printer without showing the print dialog.
        """
        bill_text = self.text_edit.toPlainText()
        try:
            self.send_to_printer_callback(bill_text)
            QMessageBox.information(self, "Print Success", "Bill sent to the thermal printer successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Print Error", f"Failed to print bill: {str(e)}")


class SellProductWidget(QWidget):
    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service
        self.cart = []  # List to store cart items
        self.init_ui()
        self.add_shortcuts()  # Add shortcut bindings

    def add_shortcuts(self):
        """
        Add keyboard shortcuts for common actions.
        """
        # Shortcut for Add to Cart button (Enter key)
        self.add_to_cart_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        self.add_to_cart_shortcut.activated.connect(self.add_to_cart)

        # Optionally, also bind the Enter key (numpad) for consistency
        self.add_to_cart_shortcut_numpad = QShortcut(QKeySequence(Qt.Key.Key_Enter), self)
        self.add_to_cart_shortcut_numpad.activated.connect(self.add_to_cart)

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Product Selection Layout
        product_layout = QHBoxLayout()

        product_label = QLabel("Select Product:")
        self.product_combo = QComboBox()
        self.load_products()

        quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter quantity")
        self.quantity_input.setValidator(QIntValidator(1, 1000000, self))

        add_button = QPushButton("Add to Cart")
        add_button.clicked.connect(self.add_to_cart)

        product_layout.addWidget(product_label)
        product_layout.addWidget(self.product_combo)
        product_layout.addWidget(quantity_label)
        product_layout.addWidget(self.quantity_input)
        product_layout.addWidget(add_button)

        main_layout.addLayout(product_layout)

        # Cart Table
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(4)
        self.cart_table.setHorizontalHeaderLabels([
            "Product ID", "Product Name", "Quantity", "Unit Price"
        ])
        self.cart_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.cart_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.cart_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.cart_table.setAlternatingRowColors(True)  # For even/odd row color styling

        # Configure header to make columns equal width
        header = self.cart_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        main_layout.addWidget(self.cart_table)

        # Total and Finalize Sale Layout
        finalize_layout = QHBoxLayout()

        self.total_label = QLabel("Total: Rs 0.00")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        finalize_button = QPushButton("Finalize Sale")
        finalize_button.clicked.connect(self.finalize_sale)

        finalize_layout.addStretch()
        finalize_layout.addWidget(self.total_label)
        finalize_layout.addWidget(finalize_button)

        main_layout.addLayout(finalize_layout)

        self.setLayout(main_layout)
        self.apply_styles()

    def apply_styles(self):
        # Apply modern UI design based on the provided guidelines
        self.setFont(QFont("Roboto", 14))

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2d;
                color: #c4c4c4;
                font-family: "Roboto";
                font-size: 14px;
            }

            QLabel {
                color: #ffffff;
                font-size: 14px;
            }

            QLineEdit, QTextEdit {
                background-color: #2b2b3c;
                color: #ffffff;
                border: 1px solid #5a5f66;
                border-radius: 5px;
                padding: 4px;
            }

            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #00adb5;
                outline: none;
            }

            QComboBox {
                background-color: #2b2b3c;
                color: #ffffff;
                border: 1px solid #5a5f66;
                border-radius: 5px;
                padding: 4px;
            }

            QComboBox QAbstractItemView {
                background-color: #1e1e2d;
                selection-background-color: #323544;
                color: #ffffff;
            }

            QPushButton {
                background-color: #00adb5;
                color: #ffffff;
                border-radius: 5px;
                padding: 8px 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #007f8b;
            }

            QTableWidget {
                gridline-color: #5a5f66;
                border: 1px solid #5a5f66;
                font-size: 14px;
            }

            QTableWidget::item:alternate {
                background-color: #2b2b3c;
            }

            QTableWidget::item:selected {
                background-color: #323544;
            }

            QHeaderView::section {
                background-color: #2b2b3c;
                color: #ffffff;
                font-weight: bold;
                border: none;
                padding: 4px;
            }

            QDialog {
                background-color: #1e1e2d;
                color: #c4c4c4;
                border-radius: 10px;
            }

            QMessageBox {
                background-color: #1e1e2d;
                color: #c4c4c4;
            }

            QDialogButtonBox QPushButton {
                background-color: #00adb5;
                color: #ffffff;
                border-radius: 5px;
                padding: 8px 12px;
            }

            QDialogButtonBox QPushButton:hover {
                background-color: #007f8b;
            }

        """)

        self.total_label.setStyleSheet("color: #ffffff; font-size: 16px; font-weight:bold;")
    
    def load_products(self):
        """
        Loads all products into the product_combo dropdown.
        """
        try:
            products: List[Product] = self.inventory_service.get_all_products()
            self.product_combo.clear()
            for product in products:
                display_text = f"{product.name} (SKU: {product.sku})"
                self.product_combo.addItem(display_text, userData=product.product_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load products: {str(e)}")

    def add_to_cart(self):
        """
        Adds the selected product and quantity to the cart.
        """
        product_id = self.product_combo.currentData()
        quantity_text = self.quantity_input.text()

        if not quantity_text.isdigit():
            QMessageBox.warning(self, "Input Error", "Please enter a valid quantity.")
            return

        quantity = int(quantity_text)
        if quantity <= 0:
            QMessageBox.warning(self, "Input Error", "Quantity must be greater than zero.")
            return

        try:
            product = self.inventory_service.get_product_by_id(product_id)
            if not product:
                QMessageBox.warning(self, "Error", "Selected product not found.")
                return

            available_quantity = self.inventory_service.get_available_quantity(product_id)
            if quantity > available_quantity:
                QMessageBox.warning(
                    self, "Insufficient Stock",
                    f"Only {available_quantity} units of '{product.name}' are available."
                )
                return

            # Add to cart
            self.cart.append({
                "product_id": product.product_id,
                "product_name": product.name,
                "quantity": quantity,
                "unit_price": product.unit_price
            })

            self.update_cart_table()
            self.quantity_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add to cart: {str(e)}")

    def update_cart_table(self):
        """
        Updates the cart_table to display current cart items and calculates the total.
        """
        self.cart_table.setRowCount(len(self.cart))
        total = 0.0
        for row, item in enumerate(self.cart):
            self.cart_table.setItem(row, 0, QTableWidgetItem(str(item["product_id"])))
            self.cart_table.setItem(row, 1, QTableWidgetItem(item["product_name"]))
            self.cart_table.setItem(row, 2, QTableWidgetItem(str(item["quantity"])))
            self.cart_table.setItem(row, 3, QTableWidgetItem(f"Rs{item['unit_price']:.2f}"))
            total += item["quantity"] * item["unit_price"]

        self.total_label.setText(f"Total: Rs{total:.2f}")

    def _send_to_printer(self, bill_text: str):
        """
        Sends the given text directly to the thermal printer.
        """
        CUT_COMMAND = "\x1D\x56\x42\x00"
        FEED_LINES = "\n" * 2
        bill_text += FEED_LINES + CUT_COMMAND

        printer_name = win32print.GetDefaultPrinter()
        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Bill Print", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, bill_text.encode('cp437'))
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)

    def finalize_sale(self):
        """
        Processes the sale by recording each item in the cart and then prints a bill.
        """
        if not self.cart:
            QMessageBox.warning(self, "Empty Cart", "No items in the cart to sell.")
            return

        try:
            total = 0.0
            bill_lines = []
            bill_lines.append("\n      ***** PHARMACY INVOICE *****\n\n")
            bill_lines.append(f"Date: {date.today().strftime('%Y-%m-%d')}\n")
            bill_lines.append("------------------------------------------------\n")
            bill_lines.append(f"{'Product':<20}{'Qty':>6}{'Price':>10}{'Total':>12}\n")
            bill_lines.append("------------------------------------------------\n")

            for item in self.cart:
                sale_record = SaleRecord(
                    sale_id=None,
                    product_id=item["product_id"],
                    quantity_sold=item["quantity"],
                    sale_date=date.today(),
                    unit_price_at_sale=item["unit_price"]
                )
                self.inventory_service.record_sale(sale_record)

                line_total = item["quantity"] * item["unit_price"]
                total += line_total

                # Truncate product name if too long
                product_name = (item['product_name'][:18] + '..') if len(item['product_name']) > 18 else item['product_name']

                # Format prices with two decimal places
                unit_price_str = f"Rs{item['unit_price']:.2f}"
                line_total_str = f"Rs{line_total:.2f}"

                bill_lines.append(
                    f"{product_name:<20}{item['quantity']:>6}{unit_price_str:>10}{line_total_str:>12}\n"
                )

            bill_lines.append("------------------------------------------------\n")
            bill_lines.append(f"{'TOTAL':>38}{f'Rs{total:.2f}':>10}\n")
            bill_lines.append("------------------------------------------------\n")
            bill_lines.append("\n          Thank you for your purchase!\n")
            bill_lines.append("              Visit again!\n")
            bill_lines.append("------------------------------------------------\n")

            bill_text = "".join(bill_lines)

            # Send bill_text to the thermal printer
            self._send_to_printer(bill_text)

            QMessageBox.information(self, "Success", "Sale completed successfully.")
            self.cart.clear()
            self.update_cart_table()

            # Show the bill dialog
            bill_dialog = BillDialog(bill_text, self._send_to_printer)
            bill_dialog.exec()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to finalize sale: {str(e)}")
