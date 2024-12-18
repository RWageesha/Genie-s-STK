# ui/reports.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QDateEdit, QTextEdit, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime
from typing import Dict

from domain.domain_models import SalesReport

class Reports(QWidget):
    def __init__(self, inventory_service):
        super().__init__()
        self.inventory_service = inventory_service
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Report selection and parameters
        param_layout = QHBoxLayout()
        
        self.report_type_combo = QComboBox()
        self.report_type_combo.addItems(["Sales Report", "Inventory Status"])
        param_layout.addWidget(QLabel("Report Type:"))
        param_layout.addWidget(self.report_type_combo)
        
        self.start_date_edit = QDateEdit(datetime.today())
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDisplayFormat("yyyy-MM-dd")
        param_layout.addWidget(QLabel("Start Date:"))
        param_layout.addWidget(self.start_date_edit)
        
        self.end_date_edit = QDateEdit(datetime.today())
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat("yyyy-MM-dd")
        param_layout.addWidget(QLabel("End Date:"))
        param_layout.addWidget(self.end_date_edit)
        
        self.generate_btn = QPushButton("Generate Report")
        self.generate_btn.clicked.connect(self.generate_report)
        param_layout.addWidget(self.generate_btn)
        
        self.layout.addLayout(param_layout)
        
        # Report display area
        self.report_display = QTextEdit()
        self.report_display.setReadOnly(True)
        self.layout.addWidget(self.report_display)
        
        # Report visualization
        self.canvas = FigureCanvas(plt.Figure(figsize=(5, 3)))
        self.layout.addWidget(self.canvas)
        
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
                color: #00adb5;
                font-size: 16px;
                font-weight: 600;
            }

            QComboBox {
                background-color: #2b2b3c; 
                color: #ffffff; 
                border: 1px solid #5a5f66; 
                padding: 4px;
            }

            QComboBox:focus {
                border: 1px solid #00adb5;
            }

            QComboBox QAbstractItemView {
                background-color: #1e1e2d; 
                selection-background-color: #323544; 
                color: #ffffff;
            }

            QDateEdit {
                background-color: #2b2b3c; 
                color: #ffffff; 
                border: 1px solid #5a5f66;
                padding: 4px;
            }

            QDateEdit:focus {
                border: 1px solid #00adb5;
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

            QTextEdit {
                background-color: #2b2b3c; 
                color: #ffffff; 
                border: 1px solid #5a5f66;
                font-size: 14px;
            }

            QMessageBox {
                background-color: #1e1e2d;
                color: #c4c4c4;
            }
        """)

    def generate_report(self):
        report_type = self.report_type_combo.currentText()
        start_date = self.start_date_edit.date().toPyDate()
        end_date = self.end_date_edit.date().toPyDate()
        
        if start_date > end_date:
            QMessageBox.warning(self, "Invalid Dates", "Start date must be before end date.")
            return
        
        if report_type == "Sales Report":
            sales_report = self.inventory_service.get_sales_report(start_date, end_date)
            report_text = f"Sales Report from {sales_report.start_date} to {sales_report.end_date}\n"
            report_text += f"Total Sales: {sales_report.total_sales:.2f}\n\n"
            report_text += "Detailed Sales:\n"
            for sale in self.inventory_service.get_all_sales():
                if start_date <= sale.sale_date <= end_date:
                    report_text += f"Sale ID: {sale.sale_id}, Product: {sale.product.name if sale.product else ''}, Quantity: {sale.quantity_sold}, Date: {sale.sale_date}, Unit Price: {sale.unit_price_at_sale}\n"
            self.report_display.setText(report_text)
            
            # Plot sales by product
            self.plot_bar_chart(sales_report.sales_by_product, "Sales by Product", "Product", "Sales Amount")
        
        elif report_type == "Inventory Status":
            inventory = self.inventory_service.get_inventory_status()
            report_text = f"Inventory Status as of {end_date}\n\n"
            report_text += "Products:\n"
            for product in inventory:
                report_text += f"Product ID: {product.product_id}, SKU: {product.sku}, Name: {product.name}, Quantity: {product.total_quantity}, Reorder Level: {product.reorder_level}\n"
            self.report_display.setText(report_text)
            
            # Plot inventory distribution
            inventory_distribution = {product.name: product.total_quantity for product in inventory}
            self.plot_pie_chart(inventory_distribution, "Inventory Distribution")
    
    def plot_bar_chart(self, data: Dict[str, float], title: str, xlabel: str, ylabel: str):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        products = list(data.keys())
        sales = list(data.values())
        # Applying chart colors as per guidelines
        ax.bar(products, sales, color='#00adb5')
        ax.set_title(title, color='#00adb5')
        ax.set_xlabel(xlabel, color='#c4c4c4')
        ax.set_ylabel(ylabel, color='#c4c4c4')
        ax.spines['bottom'].set_color('#5a5f66')
        ax.spines['left'].set_color('#5a5f66')
        ax.xaxis.label.set_color('#c4c4c4')
        ax.yaxis.label.set_color('#c4c4c4')
        ax.tick_params(axis='x', colors='#c4c4c4', rotation=45)
        ax.tick_params(axis='y', colors='#c4c4c4')
        self.canvas.draw()
    
    def plot_pie_chart(self, data: Dict[str, float], title: str):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        labels = list(data.keys())
        sizes = list(data.values())
        # For pie chart, let's maintain consistency with the theme:
        # Using teal accent for slices
        colors = ['#00adb5', '#f8c471', '#e74c3c', '#5a5f66', '#c4c4c4']
        # Cycle colors if less than needed
        colors = (colors * ((len(sizes)//len(colors))+1))[:len(sizes)]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, textprops={'color':'#ffffff'})
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title(title, color='#00adb5')
        self.canvas.draw()
