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
    c.setFont("Helvetica-Bold", 32)
    title = "Monthly Budget Planner"
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 + 40, title)
    
    # Subtitle
    c.setFont("Helvetica", 18)
    subtitle = "Personal Finance Tracker"
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 - 10, subtitle)
    
    # Description
    c.setFont("Helvetica", 12)
    desc = "Track expenses, manage savings, achieve financial goals"
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 - 40, desc)
    
    # Version and date
    c.setFont("Helvetica-Oblique", 10)
    version = f"Version 1.0 • {datetime.datetime.now().strftime('%B %Y')}"
    c.drawCentredString(PAGE_WIDTH / 2, MARGIN + 40, version)
    
    # RecoveriStudio branding
    c.setFillColor(COLOR_ACCENT)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(PAGE_WIDTH / 2, MARGIN + 20, "RecoveriStudio")

def create_annual_goals_page(c):
    """Create annual financial goals page"""
    draw_header(c, "Annual Financial Goals")
    
    y_pos = PAGE_HEIGHT - MARGIN - 50
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    instructions = "Set your financial goals for the year. Be specific and realistic."
    c.drawString(MARGIN, y_pos, instructions)
    y_pos -= 30
    
    # Goals table
    goals_data = [
        ["Goal Category", "Specific Goal", "Target Amount", "Deadline", "Progress"],
        ["Savings", "Emergency Fund", "£3,000", "Dec 2026", "___%"],
        ["Debt", "Pay off Credit Card", "£1,500", "Sep 2026", "___%"],
        ["Investment", "Start ISA", "£5,000", "Nov 2026", "___%"],
        ["Income", "Side Hustle Revenue", "£2,000", "Aug 2026", "___%"],
        ["Major Purchase", "New Laptop", "£1,200", "Jul 2026", "___%"],
        ["Education", "Online Course", "£500", "May 2026", "___%"],
    ]
    
    # Create table
    col_widths = [80, 120, 70, 70, 60]
    table = Table(goals_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_LIGHT),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), COLOR_LIGHT),
        ('TEXTCOLOR', (0, 1), (-1, -1), COLOR_TEXT),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_SECONDARY),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    table.drawOn(c, MARGIN, y_pos - 200)
    
    # Notes section
    y_pos = y_pos - 250
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y_pos, "Notes & Action Steps:")
    y_pos -= 20
    
    c.setFont("Helvetica", 9)
    notes = [
        "1. Review goals quarterly and adjust as needed",
        "2. Break large goals into monthly milestones",
        "3. Celebrate small wins along the way",
        "4. Track progress in the monthly review section"
    ]
    
    for note in notes:
        c.drawString(MARGIN + 10, y_pos, note)
        y_pos -= 15

def create_monthly_budget_page(c, month_name):
    """Create monthly budget overview page"""
    draw_header(c, f"{month_name} Budget Overview")
    
    y_pos = PAGE_HEIGHT - MARGIN - 50
    
    # Income section
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y_pos, "Income:")
    y_pos -= 25
    
    income_data = [
        ["Source", "Planned", "Actual", "Difference"],
        ["Salary", "£______", "£______", "£______"],
        ["Freelance", "£______", "£______", "£______"],
        ["Investments", "£______", "£______", "£______"],
        ["Other", "£______", "£______", "£______"],
        ["TOTAL", "£______", "£______", "£______"],
    ]
    
    col_widths = [100, 70, 70, 70]
    table = Table(income_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_LIGHT),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -2), COLOR_LIGHT),
        ('BACKGROUND', (0, -1), (-1, -1), COLOR_SECONDARY),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_SECONDARY),
    ]))
    
    table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    table.drawOn(c, MARGIN, y_pos - 120)
    
    # Expenses section
    y_pos = y_pos - 180
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y_pos, "Expenses:")
    y_pos -= 25
    
    expense_data = [
        ["Category", "Planned", "Actual", "Difference"],
        ["Housing", "£______", "£______", "£______"],
        ["Utilities", "£______", "£______", "£______"],
        ["Groceries", "£______", "£______", "£______"],
        ["Transport", "£______", "£______", "£______"],
        ["Entertainment", "£______", "£______", "£______"],
        ["Healthcare", "£______", "£______", "£______"],
        ["Debt Payments", "£______", "£______", "£______"],
        ["Savings", "£______", "£______", "£______"],
        ["Other", "£______", "£______", "£______"],
        ["TOTAL", "£______", "£______", "£______"],
    ]
    
    table2 = Table(expense_data, colWidths=col_widths)
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_LIGHT),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -2), COLOR_LIGHT),
        ('BACKGROUND', (0, -1), (-1, -1), COLOR_SECONDARY),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_SECONDARY),
    ]))
    
    table2.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    table2.drawOn(c, MARGIN, y_pos - 220)

def create_expense_tracker_page(c):
    """Create detailed expense tracker page"""
    draw_header(c, "Daily Expense Tracker")
    
    y_pos = PAGE_HEIGHT - MARGIN - 50
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, y_pos, "Track every expense daily for accurate budgeting:")
    y_pos -= 30
    
    # Expense log table
    expense_data = [
        ["Date", "Description", "Category", "Amount", "Payment Method"],
        ["__/__", "____________________", "__________", "£______", "__________"],
        ["__/__", "____________________", "__________", "£______", "__________"],
        ["__/__", "____________________", "__________", "£______", "__________"],
        ["__/__", "____________________", "__________", "£______", "__________"],
        ["__/__", "____________________", "__________", "£______", "__________"],
        ["__/__", "____________________", "__________", "£______", "__________"],
        ["__/__", "____________________", "__________", "£______", "__________"],
        ["__/__", "____________________", "__________", "£______", "__________"],
        ["__/__", "____________________", "__________", "£______", "__________"],
        ["__/__", "____________________", "__________", "£______", "__________"],
    ]
    
    col_widths = [50, 120, 80, 60, 80]
    table = Table(expense_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_LIGHT),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), COLOR_LIGHT),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_SECONDARY),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    table.drawOn(c, MARGIN, y_pos - 250)
    
    # Category totals
    y_pos = y_pos - 300
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y_pos, "Category Totals:")
    y_pos -= 20
    
    categories = ["Housing", "Utilities", "Groceries", "Transport", "Entertainment", "Healthcare", "Other"]
    for i, category in enumerate(categories):
        x_pos = MARGIN + (i % 3) * 140
        row = i // 3
        c.setFont("Helvetica", 9)
        c.drawString(x_pos, y_pos - (row * 20), f"{category}: £______")

def create_savings_tracker_page(c):
    """Create savings goals tracker page"""
    draw_header(c, "Savings Goals Tracker")
    
    y_pos = PAGE_HEIGHT - MARGIN - 50
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, y_pos, "Track progress toward your savings goals:")
    y_pos -= 40
    
    # Savings goals with progress bars
    goals = [
        ("Emergency Fund", 3000, "High"),
        ("Vacation", 1500, "Medium"),
        ("New Car Down Payment", 5000, "Low"),
        ("Home Renovation", 10000, "Medium"),
    ]
    
    for i, (goal, target, priority) in enumerate(goals):
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN, y_pos, f"{goal}:")
        
        c.setFont("Helvetica", 10)
        c.drawString(MARGIN + 120, y_pos, f"Target: £{target:,}")
        c.drawString(MARGIN + 250, y_pos, f"Priority: {priority}")
        
        # Progress bar background
        c.setStrokeColor(COLOR_SECONDARY)
        c.setLineWidth(2)
        c.line(MARGIN, y_pos - 10, MARGIN + 200, y_pos - 10)
        
        # Progress bar fill (partial)
        c.setStrokeColor(COLOR_ACCENT)
        c.setLineWidth(8)
        c.line(MARGIN, y_pos - 10, MARGIN + 60, y_pos - 10)  # 30% progress
        
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN + 210, y_pos - 5, "Saved: £______ / £______")
        
        y_pos -= 40
    
    # Savings log
    y_pos -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y_pos, "Savings Contributions Log:")
    y_pos -= 20
    
    log_data = [
        ["Date", "Goal", "Amount", "Balance"],
        ["__/__", "__________", "£______", "£______"],
        ["__/__", "__________", "£______", "£______"],
        ["__/__", "__________", "£______", "£______"],
        ["__/__", "__________", "£______", "£______"],
    ]
    
    col_widths = [50, 100, 70, 70]
    table = Table(log_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_LIGHT),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), COLOR_LIGHT),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_SECONDARY),
    ]))
    
    table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    table.drawOn(c, M