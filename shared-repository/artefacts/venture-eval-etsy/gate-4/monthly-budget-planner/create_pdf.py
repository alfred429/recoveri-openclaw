#!/usr/bin/env python3
"""
Monthly Budget Planner PDF Generator
Creates an 8-12 page A4 PDF budget planner with RecoveriStudio footer
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import datetime

# Color palette - soft neutrals
COLOR_BG = colors.HexColor('#F5F0EB')  # Light beige background
COLOR_TEXT = colors.HexColor('#2C2C2C')  # Dark gray text
COLOR_ACCENT = colors.HexColor('#8B7355')  # Warm brown accent
COLOR_SECONDARY = colors.HexColor('#D4C5B2')  # Light brown secondary
COLOR_LIGHT = colors.HexColor('#FFFFFF')  # White for boxes

# Page dimensions
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 20 * mm
CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN)

def draw_header(c, page_title):
    """Draw page header with title and decorative line"""
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 10, page_title)
    
    # Decorative line
    c.setStrokeColor(COLOR_ACCENT)
    c.setLineWidth(1)
    c.line(MARGIN, PAGE_HEIGHT - MARGIN - 15, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - MARGIN - 15)

def draw_footer(c, page_num):
    """Draw RecoveriStudio footer on every page"""
    c.setFillColor(COLOR_SECONDARY)
    c.setFont("Helvetica", 8)
    footer_text = f"RecoveriStudio • Monthly Budget Planner • Page {page_num}"
    c.drawCentredString(PAGE_WIDTH / 2, MARGIN - 10, footer_text)

def create_title_page(c):
    """Create title/cover page"""
    # Background
    c.setFillColor(COLOR_BG)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    
    # Main title
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 28)
    title = "Monthly Budget Planner"
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 + 40, title)
    
    # Subtitle
    c.setFont("Helvetica", 16)
    subtitle = "Personal Finance Tracker & Expense Manager"
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2, subtitle)
    
    # Decorative line
    c.setStrokeColor(COLOR_ACCENT)
    c.setLineWidth(2)
    c.line(PAGE_WIDTH / 2 - 100, PAGE_HEIGHT / 2 - 20, PAGE_WIDTH / 2 + 100, PAGE_HEIGHT / 2 - 20)
    
    # Features
    c.setFont("Helvetica", 12)
    features = [
        "• Expense Tracking • Savings Goals • Debt Payoff Plan",
        "• Bill Calendar • Financial Review • Net Worth Tracker"
    ]
    for i, feature in enumerate(features):
        c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 - 60 - (i * 20), feature)
    
    # Year
    c.setFont("Helvetica-Oblique", 14)
    year = datetime.datetime.now().year
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 - 120, f"Designed for {year}")
    
    # Footer
    c.setFillColor(COLOR_SECONDARY)
    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_WIDTH / 2, MARGIN + 20, "RecoveriStudio • Professional Digital Planners")

def create_annual_goals_page(c):
    """Create annual financial goals page"""
    draw_header(c, "Annual Financial Goals")
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 40, "Set your financial goals for the year. Be specific and realistic.")
    
    # Goals table
    data = [
        ["Goal", "Target Amount", "Deadline", "Progress"],
        ["Emergency Fund", "£__________", "___/___/____", "[  ] [  ] [  ] [  ] [  ]"],
        ["Debt Payoff", "£__________", "___/___/____", "[  ] [  ] [  ] [  ] [  ]"],
        ["Savings Goal", "£__________", "___/___/____", "[  ] [  ] [  ] [  ] [  ]"],
        ["Investment", "£__________", "___/___/____", "[  ] [  ] [  ] [  ] [  ]"],
        ["Major Purchase", "£__________", "___/___/____", "[  ] [  ] [  ] [  ] [  ]"],
        ["Other", "£__________", "___/___/____", "[  ] [  ] [  ] [  ] [  ]"]
    ]
    
    # Create table
    table = Table(data, colWidths=[CONTENT_WIDTH * 0.3, CONTENT_WIDTH * 0.25, CONTENT_WIDTH * 0.25, CONTENT_WIDTH * 0.2])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), COLOR_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_SECONDARY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    table.drawOn(c, MARGIN, PAGE_HEIGHT - MARGIN - 200)
    
    # Notes section
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 250, "Notes & Action Steps:")
    
    c.setFont("Helvetica", 9)
    notes_y = PAGE_HEIGHT - MARGIN - 270
    for i in range(8):
        c.line(MARGIN, notes_y, PAGE_WIDTH - MARGIN, notes_y)
        notes_y -= 15

def create_monthly_budget_page(c, month_name):
    """Create monthly budget overview page"""
    draw_header(c, f"{month_name} Budget Overview")
    
    # Income section
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 40, "Monthly Income")
    
    c.setFont("Helvetica", 10)
    income_data = [
        ["Source", "Planned", "Actual"],
        ["Salary/Wages", "£__________", "£__________"],
        ["Freelance", "£__________", "£__________"],
        ["Investments", "£__________", "£__________"],
        ["Other", "£__________", "£__________"],
        ["TOTAL INCOME", "£__________", "£__________"]
    ]
    
    income_table = Table(income_data, colWidths=[CONTENT_WIDTH * 0.4, CONTENT_WIDTH * 0.3, CONTENT_WIDTH * 0.3])
    income_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_SECONDARY),
        ('BACKGROUND', (0, 5), (-1, 5), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 5), (-1, 5), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 5), (-1, 5), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_SECONDARY),
    ]))
    
    income_table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    income_table.drawOn(c, MARGIN, PAGE_HEIGHT - MARGIN - 120)
    
    # Expenses section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 200, "Monthly Expenses")
    
    expense_categories = [
        ["Housing", "£__________", "£__________"],
        ["Utilities", "£__________", "£__________"],
        ["Groceries", "£__________", "£__________"],
        ["Transport", "£__________", "£__________"],
        ["Entertainment", "£__________", "£__________"],
        ["Healthcare", "£__________", "£__________"],
        ["Debt Payments", "£__________", "£__________"],
        ["Savings", "£__________", "£__________"],
        ["Other", "£__________", "£__________"],
        ["TOTAL EXPENSES", "£__________", "£__________"]
    ]
    
    expense_table = Table(expense_categories, colWidths=[CONTENT_WIDTH * 0.4, CONTENT_WIDTH * 0.3, CONTENT_WIDTH * 0.3])
    expense_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_SECONDARY),
        ('BACKGROUND', (0, 9), (-1, 9), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 9), (-1, 9), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 9), (-1, 9), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_SECONDARY),
    ]))
    
    expense_table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    expense_table.drawOn(c, MARGIN, PAGE_HEIGHT - MARGIN - 380)
    
    # Summary
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 420, "Monthly Summary:")
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN + 150, PAGE_HEIGHT - MARGIN - 420, "Income - Expenses = £__________")
    c.drawString(MARGIN + 150, PAGE_HEIGHT - MARGIN - 435, "(Positive = Savings, Negative = Overspend)")

def create_expense_tracker_page(c):
    """Create daily expense tracker page"""
    draw_header(c, "Daily Expense Tracker")
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 40, "Track every expense daily. Use categories from your budget.")
    
    # Daily tracker table (2 weeks)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    data = [["Date", "Description", "Category", "Amount", "Paid With"]]
    
    for week in range(2):
        for day in days:
            data.append([f"___/___", "____________________", "__________", "£______", "__________"])
    
    # Add totals row
    data.append(["WEEK TOTAL", "", "", "£__________", ""])
    
    tracker_table = Table(data, colWidths=[CONTENT_WIDTH * 0.15, CONTENT_WIDTH * 0.3, CONTENT_WIDTH * 0.2, CONTENT_WIDTH * 0.15, CONTENT_WIDTH * 0.2])
    tracker_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 8), (-1, 8), COLOR_SECONDARY),
        ('BACKGROUND', (0, 16), (-1, 16), COLOR_SECONDARY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 8), (-1, 8), 'Helvetica-Bold'),
        ('FONTNAME', (0, 16), (-1, 16), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_SECONDARY),
    ]))
    
    tracker_table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    tracker_table.drawOn(c, MARGIN, PAGE_HEIGHT - MARGIN - 250)
    
    # Category totals
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 320, "Category Totals This Month:")
    
    categories = ["Housing", "Food", "Transport", "Entertainment", "Shopping", "Other"]
    y_pos = PAGE_HEIGHT - MARGIN - 340
    for i, category in enumerate(categories):
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN + (i % 3) * 140, y_pos - (i // 3) * 20, f"{category}: £__________")

def create_savings_tracker_page(c):
    """Create savings goals tracker page"""
    draw_header(c, "Savings Goals Tracker")
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 40, "Track progress toward your savings goals. Shade boxes as you save.")
    
    # Savings goals with progress bars
    goals = [
        {"name": "Emergency Fund", "target": 1000, "current": 0},
        {"name": "Vacation", "target": 800, "current": 0},
        {"name": "New Laptop", "target": 1200, "current": 0},
        {"name": "Car Maintenance", "target": 500, "current": 0},
        {"name": "Christmas Fund", "target": 400, "current": 0},
        {"name": "Investment", "target": 2000, "current": 0}
    ]
    
    y_pos = PAGE_HEIGHT - MARGIN - 80
    for i, goal in enumerate(goals):
        c.setFont("Helvetica-Bold", 10)
        c.drawString(MARGIN, y_pos, f"{goal['name']}: £{goal['target']}")
        
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN + 200, y_pos, "Progress: ")
        
        # Progress bar (10 boxes)
        bar_x = MARGIN + 260
        for box in range(10):
            c.setStrokeColor(COLOR_SECONDARY)
            c.setFillColor(COLOR_LIGHT)
            c.rect(bar_x + (box * 15), y_pos - 3, 12, 12, fill=1, stroke=1)
            c.setFont("Helvetica", 6)
            c.drawCentredString(bar_x + (box * 15) + 6, y_pos + 1, str(box + 1))
        
        # Monthly contributions
        c.setFont("Helvetica", 8)
        c.drawString(MARGIN, y_pos - 20, f"Monthly: £__________ | Saved: £__________ | Remaining: £__________")
        
        y_pos -= 50 if i < 3 else 40
    
    # Savings log
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y_pos - 20, "Savings Contributions Log:")
    
    log_data = [
        ["Date", "Goal", "Amount", "Balance"],
        ["___/___", "__________", "£______", "£__________"],
        ["___/___", "__________", "£______", "£__________"],
        ["___/___", "__________", "£______", "£__________"],
        ["___