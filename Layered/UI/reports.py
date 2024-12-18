# ui/reports.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QDateEdit, QTextEdit, QMessageBox
)
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
        ax.bar(products, sales, color='skyblue')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.tick_params(axis='x', rotation=45)
        self.canvas.draw()
    
    def plot_pie_chart(self, data: Dict[str, float], title: str):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        labels = list(data.keys())
        sizes = list(data.values())
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title(title)
        self.canvas.draw()
