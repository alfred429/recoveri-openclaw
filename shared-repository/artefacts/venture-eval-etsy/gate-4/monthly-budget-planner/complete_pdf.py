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
        ["___def create_debt_tracker_page(c):
    """Create debt payoff tracker page"""
    draw_header(c, "Debt Payoff Plan")
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 40, "Choose snowball (smallest first) or avalanche (highest interest first) method.")
    
    # Debt table
    debt_data = [
        ["Creditor", "Balance", "Interest %", "Min Payment", "Target Payoff"],
        ["Credit Card", "£__________", "____%", "£______", "___/___/____"],
        ["Student Loan", "£__________", "____%", "£______", "___/___/____"],
        ["Car Loan", "£__________", "____%", "£______", "___/___/____"],
        ["Personal Loan", "£__________", "____%", "£______", "___/___/____"],
        ["Other", "£__________", "____%", "£______", "___/___/____"],
        ["TOTAL DEBT", "£__________", "", "£__________", ""]
    ]
    
    debt_table = Table(debt_data, colWidths=[CONTENT_WIDTH * 0.22, CONTENT_WIDTH * 0.18, CONTENT_WIDTH * 0.15, CONTENT_WIDTH * 0.18, CONTENT_WIDTH * 0.27])
    debt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 6), (-1, 6), COLOR_SECONDARY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 6), (-1, 6), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_SECONDARY),
    ]))
    
    debt_table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    debt_table.drawOn(c, MARGIN, PAGE_HEIGHT - MARGIN - 150)
    
    # Payoff strategy
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 200, "Payoff Strategy:")
    
    strategies = [
        "☐ Snowball Method: Pay minimums on all, extra on smallest balance",
        "☐ Avalanche Method: Pay minimums on all, extra on highest interest",
        "☐ Custom: _________________________________________________"
    ]
    
    y_pos = PAGE_HEIGHT - MARGIN - 220
    for strategy in strategies:
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN, y_pos, strategy)
        y_pos -= 20
    
    # Monthly payment plan
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y_pos - 20, "Monthly Extra Payment: £__________")
    c.drawString(MARGIN, y_pos - 40, "Estimated Payoff Date: ___/___/____")

def create_bill_calendar_page(c):
    """Create bill payment calendar page"""
    draw_header(c, "Bill Payment Calendar")
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 40, "Mark due dates and check off when paid. Avoid late fees!")
    
    # Calendar grid (4 weeks)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    data = [["Week", "Bill", "Amount", "Due Date", "Paid ✓", "Notes"]]
    
    for week in range(4):
        for i in range(3):  # 3 bills per week max
            data.append([f"Week {week+1}", "__________", "£______", "___", "[ ]", "__________"])
    
    bill_table = Table(data, colWidths=[CONTENT_WIDTH * 0.12, CONTENT_WIDTH * 0.25, CONTENT_WIDTH * 0.15, CONTENT_WIDTH * 0.12, CONTENT_WIDTH * 0.12, CONTENT_WIDTH * 0.24])
    bill_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_SECONDARY),
        ('BACKGROUND', (0, 1), (-1, 4), COLOR_LIGHT),
        ('BACKGROUND', (0, 5), (-1, 8), colors.HexColor('#F8F8F8')),
        ('BACKGROUND', (0, 9), (-1, 12), COLOR_LIGHT),
    ]))
    
    bill_table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    bill_table.drawOn(c, MARGIN, PAGE_HEIGHT - MARGIN - 250)
    
    # Recurring subscriptions
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 320, "Recurring Subscriptions:")
    
    subs = ["Netflix", "Spotify", "Amazon Prime", "Gym", "Software", "Other"]
    y_pos = PAGE_HEIGHT - MARGIN - 340
    for i, sub in enumerate(subs):
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN + (i % 3) * 140, y_pos - (i // 3) * 20, f"{sub}: £__________/mo")

def create_financial_review_page(c):
    """Create monthly financial review page"""
    draw_header(c, "Monthly Financial Review")
    
    # Review questions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 40, "End-of-Month Reflection")
    
    questions = [
        "1. Did I stay within my budget this month? What went well?",
        "________________________________________________________________",
        "________________________________________________________________",
        "",
        "2. Where did I overspend? Why?",
        "________________________________________________________________",
        "________________________________________________________________",
        "",
        "3. What unexpected expenses came up?",
        "________________________________________________________________",
        "________________________________________________________________",
        "",
        "4. Did I meet my savings goals? If not, what prevented me?",
        "________________________________________________________________",
        "________________________________________________________________",
        "",
        "5. What will I do differently next month?",
        "________________________________________________________________",
        "________________________________________________________________"
    ]
    
    y_pos = PAGE_HEIGHT - MARGIN - 70
    for question in questions:
        if question.startswith("1.") or question.startswith("2.") or question.startswith("3.") or question.startswith("4.") or question.startswith("5."):
            c.setFont("Helvetica-Bold", 10)
        elif question == "":
            y_pos -= 10
            continue
        else:
            c.setFont("Helvetica", 9)
        
        c.drawString(MARGIN, y_pos, question)
        y_pos -= 15
    
    # Action items
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y_pos - 30, "Action Items for Next Month:")
    
    for i in range(4):
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN, y_pos - 50 - (i * 15), f"{i+1}. [ ] _________________________________________")

def create_net_worth_page(c):
    """Create net worth tracker page"""
    draw_header(c, "Net Worth Tracker")
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 40, "Track your net worth quarterly. Assets minus liabilities.")
    
    # Assets section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 70, "Assets (What You Own)")
    
    assets = [
        ["Cash & Bank Accounts", "Q1", "Q2", "Q3", "Q4"],
        ["Savings Accounts", "£__________", "£__________", "£__________", "£__________"],
        ["Investment Accounts", "£__________", "£__________", "£__________", "£__________"],
        ["Retirement Funds", "£__________", "£__________", "£__________", "£__________"],
        ["Real Estate", "£__________", "£__________", "£__________", "£__________"],
        ["Vehicles", "£__________", "£__________", "£__________", "£__________"],
        ["Other Assets", "£__________", "£__________", "£__________", "£__________"],
        ["TOTAL ASSETS", "£__________", "£__________", "£__________", "£__________"]
    ]
    
    assets_table = Table(assets, colWidths=[CONTENT_WIDTH * 0.35] + [CONTENT_WIDTH * 0.16] * 4)
    assets_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 7), (-1, 7), COLOR_SECONDARY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 7), (-1, 7), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_SECONDARY),
    ]))
    
    assets_table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    assets_table.drawOn(c, MARGIN, PAGE_HEIGHT - MARGIN - 200)
    
    # Liabilities section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 280, "Liabilities (What You Owe)")
    
    liabilities = [
        ["Mortgage", "£__________", "£__________", "£__________", "£__________"],
        ["Car Loans", "£__________", "£__________", "£__________", "£__________"],
        ["Student Loans", "£__________", "£__________", "£__________", "£__________"],
        ["Credit Cards", "£__________", "£__________", "£__________", "£__________"],
        ["Personal Loans", "£__________", "£__________", "£__________", "£__________"],
        ["Other Debts", "£__________", "£__________", "£__________", "£__________"],
        ["TOTAL LIABILITIES", "£__________", "£__________", "£__________", "£__________"]
    ]
    
    liab_table = Table(liabilities, colWidths=[CONTENT_WIDTH * 0.35] + [CONTENT_WIDTH * 0.16] * 4)
    liab_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 6), (-1, 6), COLOR_SECONDARY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 6), (-1, 6), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_SECONDARY),
    ]))
    
    liab_table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    liab_table.drawOn(c, MARGIN, PAGE_HEIGHT - MARGIN - 380)
    
    # Net worth calculation
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 420, "Net Worth Calculation:")
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN + 50, PAGE_HEIGHT - MARGIN - 440, "Q1: Assets £__________ - Liabilities £__________ = Net Worth £__________")
    c.drawString(MARGIN + 50, PAGE_HEIGHT - MARGIN - 455, "Q2: Assets £__________ - Liabilities £__________ = Net Worth £__________")
    c.drawString(MARGIN + 50, PAGE_HEIGHT - MARGIN - 470, "Q3: Assets £__________ - Liabilities £__________ = Net Worth £__________")
    c.drawString(MARGIN + 50, PAGE_HEIGHT - MARGIN - 485, "Q4: Assets £__________ - Liabilities £__________ = Net Worth £__________")

def main():
    """Main function to create the PDF"""
    output_path = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/monthly-budget-planner/product.pdf"
    
    # Create canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    
    # Set metadata
    c.setTitle("Monthly Budget Planner - RecoveriStudio")
    c.setAuthor("RecoveriStudio")
    c.setSubject("Personal Finance Tracker")
    
    # Create pages
    pages = [
        (create_title_page, "Title"),
        (create_annual_goals_page, "Annual Goals"),
        (lambda c: create_monthly_budget_page(c, "January"), "January Budget"),
        (lambda c: create_monthly_budget_page(c, "February"), "February Budget"),
        (create_expense_tracker_page, "Expense Tracker"),
        (create_savings_tracker_page, "Savings Tracker"),
        (create_debt_tracker_page, "Debt Payoff"),
        (create_bill_calendar_page, "Bill Calendar"),
        (create_financial_review_page, "Financial Review"),
        (create_net_worth_page, "Net Worth Tracker")
    ]
    
    # Generate each page
    for i, (page_func, title) in enumerate(pages):
        page_func(c)
        draw_footer(c, i + 1)
        c.showPage()
    
    # Save PDF
    c.save()
    print(f"PDF created successfully: {output_path}")
    print(f"Total pages: {len(pages)}")

if __name__ == "__main__":
    main()