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
        # Apply modern UI design
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

            sales_by_product = {}  # Collect sales by product

            for sale in self.inventory_service.get_all_sales():
                if start_date <= sale.sale_date <= end_date:
                    product_name = sale.product.name if sale.product and sale.product.name else "Unnamed Product"
                    report_text += (
                        f"Sale ID: {sale.sale_id}, "
                        f"Product: {product_name}, "
                        f"Quantity: {sale.quantity_sold}, "
                        f"Date: {sale.sale_date}, "
                        f"Unit Price: {sale.unit_price_at_sale}\n"
                    )

                    # Accumulate sales amount by product
                    if product_name not in sales_by_product:
                        sales_by_product[product_name] = 0.0
                    sales_by_product[product_name] += sale.quantity_sold * sale.unit_price_at_sale

            self.report_display.setText(report_text)

            # Plot the bar chart with valid data
            if sales_by_product:
                self.plot_bar_chart(sales_by_product, "Sales by Product", "Product", "Sales Amount")
            else:
                QMessageBox.warning(self, "No Sales Data", "No sales data available for the selected dates.")

        elif report_type == "Inventory Status":
            inventory = self.inventory_service.get_inventory_status()
            report_text = f"Inventory Status as of {end_date}\n\n"
            report_text += "Products:\n"

            inventory_distribution = {}
            for product in inventory:
                product_name = product.name if product.name else "Unnamed Product"
                report_text += (
                    f"Product ID: {product.product_id}, "
                    f"SKU: {product.sku}, "
                    f"Name: {product_name}, "
                    f"Quantity: {product.total_quantity}, "
                    f"Reorder Level: {product.reorder_level}\n"
                )
                inventory_distribution[product_name] = product.total_quantity

            self.report_display.setText(report_text)
            self.plot_pie_chart(inventory_distribution, "Inventory Distribution")

    
    def plot_bar_chart(self, data: Dict[str, float], title: str, xlabel: str, ylabel: str):
        self.canvas.figure.clear()
        
        # Set a slightly larger figure size for readability
        self.canvas.figure.set_size_inches(6, 4)
        ax = self.canvas.figure.add_subplot(111)

        # Extract data
        products = list(data.keys())
        sales = list(data.values())

        # If product names are missing, replace them with placeholders
        products = [p if p else "Unknown Product" for p in products]

        # Plot the bar chart
        bars = ax.bar(products, sales, color='#00adb5', edgecolor='#323544')

        # Customize the appearance
        ax.set_facecolor('#1e1e2d')  
        ax.set_title(title, color='#00adb5', fontsize=18, pad=15, fontweight='bold')
        ax.set_xlabel(xlabel, color='#c4c4c4', fontsize=14, labelpad=10)
        ax.set_ylabel(ylabel, color='#c4c4c4', fontsize=14, labelpad=10)

        # Adjust X-axis ticks for better readability
        ax.set_xticks(range(len(products)))
        ax.set_xticklabels(products, rotation=45, ha="right", fontsize=12, color='#c4c4c4')

        # Use tick_params to set y-axis tick label colors and size
        ax.tick_params(axis='y', colors='#c4c4c4', labelsize=12)

        # Add grid lines on Y-axis for clarity
        ax.grid(axis='y', linestyle='--', linewidth=0.7, color='#5a5f66', alpha=0.7)

        # Annotate each bar with values
        if sales:
            max_val = max(sales)
        else:
            max_val = 0
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2, 
                height + (max_val * 0.01 if max_val > 0 else 0.1),
                f"{height:.0f}", 
                ha='center', 
                va='bottom', 
                color='#ffffff', 
                fontsize=10, 
                fontweight='bold'
            )

        # Use tight_layout to avoid label cutoff
        self.canvas.figure.tight_layout(pad=2.0)
        self.canvas.draw()

    
    def plot_pie_chart(self, data: Dict[str, float], title: str):
        self.canvas.figure.clear()

        # Set a larger figure size for readability
        self.canvas.figure.set_size_inches(6, 6)
        ax = self.canvas.figure.add_subplot(111)

        labels = list(data.keys())
        sizes = list(data.values())

        # Define colors for consistency
        colors = ['#00adb5', '#f8c471', '#e74c3c', '#5a5f66', '#c4c4c4']
        colors = (colors * ((len(sizes) // len(colors)) + 1))[:len(sizes)]

        # Create the pie chart
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            colors=colors,
            textprops={'color': '#ffffff', 'fontsize': 10, 'fontweight': 'bold'},
            wedgeprops={'edgecolor': '#323544'}
        )

        # Adjust the chart's title
        ax.set_title(title, color='#00adb5', fontsize=18, pad=20, fontweight='bold')
        ax.axis('equal')  # Equal aspect ratio ensures a perfect circle

        self.canvas.figure.tight_layout(pad=2.0)
        self.canvas.draw()
