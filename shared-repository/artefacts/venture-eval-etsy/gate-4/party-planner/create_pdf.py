#!/usr/bin/env python3
"""
Create Party Planner Template PDF for RecoveriStudio Etsy shop.
8-page A4 PDF with clean design and editable fields.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Colors from RecoveriStudio palette
COLOR_BG = HexColor('#F5F0EB')  # Soft beige background
COLOR_TEXT = HexColor('#2C2C2C')  # Dark gray text
COLOR_ACCENT1 = HexColor('#8B7355')  # Brown accent
COLOR_ACCENT2 = HexColor('#D4C5B2')  # Light brown

# Page dimensions
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 20 * mm
CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN)

def draw_header(c, page_num, title):
    """Draw header with title and page number"""
    c.setFillColor(COLOR_ACCENT1)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 15, title)
    
    # Page number
    c.setFont("Helvetica", 10)
    c.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - MARGIN - 15, f"Page {page_num}")
    
    # Divider line
    c.setStrokeColor(COLOR_ACCENT2)
    c.setLineWidth(0.5)
    c.line(MARGIN, PAGE_HEIGHT - MARGIN - 25, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - MARGIN - 25)

def draw_footer(c):
    """Draw footer with RecoveriStudio branding"""
    c.setFillColor(COLOR_ACCENT1)
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_WIDTH / 2, MARGIN - 10, "© RecoveriStudio | studio@recoveri.io")
    
    # Divider line
    c.setStrokeColor(COLOR_ACCENT2)
    c.setLineWidth(0.3)
    c.line(MARGIN, MARGIN, PAGE_WIDTH - MARGIN, MARGIN)

def create_cover_page(c):
    """Create cover page"""
    draw_header(c, 1, "Party Planner Template")
    
    # Title
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 32)
    title = "Party Planner"
    title_width = c.stringWidth(title, "Helvetica-Bold", 32)
    c.drawString((PAGE_WIDTH - title_width) / 2, PAGE_HEIGHT / 2 + 40, title)
    
    c.setFont("Helvetica", 20)
    subtitle = "Digital Printable Template"
    subtitle_width = c.stringWidth(subtitle, "Helvetica", 20)
    c.drawString((PAGE_WIDTH - subtitle_width) / 2, PAGE_HEIGHT / 2, subtitle)
    
    # Description
    c.setFont("Helvetica", 12)
    lines = [
        "Plan the perfect party with our comprehensive template!",
        "Includes guest lists, budget tracking, timeline checklist,",
        "menu planning, decorations, vendor contacts, and more.",
        "",
        "Simply type into the editable fields or print and write.",
        "Instant digital download - start planning immediately!"
    ]
    
    y_pos = PAGE_HEIGHT / 2 - 60
    for line in lines:
        line_width = c.stringWidth(line, "Helvetica", 12)
        c.drawString((PAGE_WIDTH - line_width) / 2, y_pos, line)
        y_pos -= 20
    
    draw_footer(c)

def create_guest_list_page(c, page_num):
    """Create guest list page"""
    draw_header(c, page_num, "Guest List & RSVP Tracker")
    
    y_pos = PAGE_HEIGHT - MARGIN - 60
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, y_pos, "Track your guests and their RSVP status. Use the notes column for dietary requirements or special requests.")
    y_pos -= 30
    
    # Table header
    c.setFillColor(COLOR_ACCENT1)
    c.setFont("Helvetica-Bold", 11)
    headers = ["Name", "Email/Phone", "Invited", "RSVP", "Notes"]
    col_widths = [CONTENT_WIDTH * 0.25, CONTENT_WIDTH * 0.25, CONTENT_WIDTH * 0.15, CONTENT_WIDTH * 0.15, CONTENT_WIDTH * 0.2]
    
    x_pos = MARGIN
    for i, header in enumerate(headers):
        c.drawString(x_pos, y_pos, header)
        x_pos += col_widths[i]
    
    y_pos -= 20
    c.setStrokeColor(COLOR_ACCENT2)
    c.setLineWidth(0.5)
    c.line(MARGIN, y_pos, PAGE_WIDTH - MARGIN, y_pos)
    y_pos -= 10
    
    # Table rows (editable fields)
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    for row in range(15):
        x_pos = MARGIN
        for i in range(len(headers)):
            # Draw editable field background
            c.setStrokeColor(COLOR_ACCENT2)
            c.setLineWidth(0.3)
            c.rect(x_pos, y_pos - 15, col_widths[i], 20, stroke=1, fill=0)
            x_pos += col_widths[i]
        y_pos -= 25
    
    draw_footer(c)

def create_budget_planner_page(c, page_num):
    """Create budget planner page"""
    draw_header(c, page_num, "Budget Planner")
    
    y_pos = PAGE_HEIGHT - MARGIN - 60
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, y_pos, "Track all party expenses by category. Set your budget and monitor actual spending.")
    y_pos -= 30
    
    # Budget summary
    c.setFillColor(COLOR_ACCENT1)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y_pos, "Total Budget: £")
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN + 100, y_pos, "[Enter your total budget]")
    
    c.setFillColor(COLOR_ACCENT1)
    c.drawString(PAGE_WIDTH / 2, y_pos, "Remaining: £")
    c.setFillColor(COLOR_TEXT)
    c.drawString(PAGE_WIDTH / 2 + 80, y_pos, "[Auto-calculated]")
    y_pos -= 30
    
    # Expense table header
    c.setFillColor(COLOR_ACCENT1)
    c.setFont("Helvetica-Bold", 11)
    headers = ["Category", "Budgeted", "Actual", "Difference", "Notes"]
    col_widths = [CONTENT_WIDTH * 0.25, CONTENT_WIDTH * 0.15, CONTENT_WIDTH * 0.15, CONTENT_WIDTH * 0.15, CONTENT_WIDTH * 0.3]
    
    x_pos = MARGIN
    for i, header in enumerate(headers):
        c.drawString(x_pos, y_pos, header)
        x_pos += col_widths[i]
    
    y_pos -= 20
    c.setStrokeColor(COLOR_ACCENT2)
    c.setLineWidth(0.5)
    c.line(MARGIN, y_pos, PAGE_WIDTH - MARGIN, y_pos)
    y_pos -= 10
    
    # Expense categories
    categories = [
        "Venue/Rental",
        "Food & Catering",
        "Drinks & Bar",
        "Decorations",
        "Entertainment",
        "Invitations",
        "Photography",
        "Cake/Dessert",
        "Party Favours",
        "Miscellaneous"
    ]
    
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    for category in categories:
        x_pos = MARGIN
        for i in range(len(headers)):
            # Draw editable field
            c.setStrokeColor(COLOR_ACCENT2)
            c.setLineWidth(0.3)
            c.rect(x_pos, y_pos - 15, col_widths[i], 20, stroke=1, fill=0)
            if i == 0:  # Category name
                c.drawString(x_pos + 5, y_pos - 10, category)
            x_pos += col_widths[i]
        y_pos -= 25
    
    draw_footer(c)

def create_timeline_page(c, page_num):
    """Create timeline checklist page"""
    draw_header(c, page_num, "6-Week Party Timeline")
    
    y_pos = PAGE_HEIGHT - MARGIN - 60
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, y_pos, "Follow this checklist to ensure everything is ready for your party day.")
    y_pos -= 30
    
    # Timeline sections
    weeks = [
        ("6 WEEKS BEFORE", ["Set budget", "Choose date & time", "Create guest list", "Book venue"]),
        ("4 WEEKS BEFORE", ["Send invitations", "Plan menu", "Book caterer", "Order decorations"]),
        ("2 WEEKS BEFORE", ["Confirm RSVPs", "Finalise menu", "Purchase drinks", "Plan seating"]),
        ("1 WEEK BEFORE", ["Confirm vendors", "Prepare decorations", "Shop for non-perishables", "Create playlist"]),
        ("2 DAYS BEFORE", ["Grocery shopping", "Prepare make-ahead food", "Charge cameras", "Confirm weather plan"]),
        ("PARTY DAY", ["Set up venue", "Prepare food", "Welcome guests", "Enjoy your party!"])
    ]
    
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    
    for week_title, tasks in weeks:
        # Week title
        c.setFillColor(COLOR_ACCENT1)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(MARGIN, y_pos, week_title)
        y_pos -= 20
        
        # Tasks with checkboxes
        c.setFillColor(COLOR_TEXT)
        c.setFont("Helvetica", 10)
        for task in tasks:
            # Checkbox
            c.setStrokeColor(COLOR_ACCENT2)
            c.setLineWidth(0.5)
            c.rect(MARGIN + 5, y_pos - 15, 10, 10, stroke=1, fill=0)
            # Task text
            c.drawString(MARGIN + 25, y_pos - 10, task)
            y_pos -= 20
        
        y_pos -= 10  # Space between weeks
    
    draw_footer(c)

def create_menu_planner_page(c, page_num):
    """Create menu and catering planner page"""
    draw_header(c, page_num, "Menu & Catering Planner")
    
    y_pos = PAGE_HEIGHT - MARGIN - 60
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, y_pos, "Plan your party menu, track dietary requirements, and coordinate with caterers.")
    y_pos -= 30
    
    # Menu sections
    sections = [
        ("APPETISERS & STARTERS", 3),
        ("MAIN COURSES", 4),
        ("SIDE DISHES", 3),
        ("DESSERTS", 3),
        ("DRINKS", 4)
    ]
    
    for section_title, item_count in sections:
        # Section title
        c.setFillColor(COLOR_ACCENT1)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(MARGIN, y_pos, section_title)
        y_pos -= 20
        
        # Item table header
        c.setFillColor(COLOR_ACCENT1)
        c.setFont("Helvetica-Bold", 10)
        headers = ["Item", "Quantity", "Special Diet", "Notes", "Assigned To"]
        col_widths = [CONTENT_WIDTH * 0.25, CONTENT_WIDTH * 0.15, CONTENT_WIDTH * 0.15, CONTENT_WIDTH * 0.25, CONTENT_WIDTH * 0.2]
        
        x_pos = MARGIN
        for i, header in enumerate(headers):
            c.drawString(x_pos, y_pos, header)
            x_pos += col_widths[i]
        
        y_pos -= 20
        c.setStrokeColor(COLOR_ACCENT2)
        c.setLineWidth(0.5)
        c.line(MARGIN, y_pos, PAGE_WIDTH - MARGIN, y_pos)
        y_pos -= 10
        
        # Item rows
        c.setFillColor(COLOR_TEXT)
        c.setFont("Helvetica", 9)
        for _ in range(item_count):
            x_pos = MARGIN
            for i in range(len(headers)):
                # Draw editable field
                c.setStrokeColor(COLOR_ACCENT2)
                c.setLineWidth(0.3)
                c.rect(x_pos, y_pos - 12, col_widths[i], 15, stroke=1, fill=0)
                x_pos += col_widths[i]
            y_pos -= 20
        
        y_pos -= 15  # Space between sections
    
    draw_footer(c)

def create_decorations_page(c, page_num):
    """Create decorations and theme ideas page"""
    draw_header(c, page_num, "Decorations & Theme Ideas")
    
    y_pos = PAGE_HEIGHT - MARGIN - 60
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, y_pos, "Brainstorm decoration ideas, track purchases, and plan your party theme.")
    y_pos -= 30
    
    # Theme section
    c.setFillColor(COLOR_ACCENT1)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y_pos, "Party Theme:")
    y_pos -= 20
    
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, y_pos, "[Describe your party theme, colour scheme, and overall aesthetic]")
    y_pos -= 40
    
    # Decorations checklist
    c.setFillColor(COLOR_ACCENT1)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y_pos, "Decorations Checklist:")
    y_pos -= 20
    
    decorations = [
        "Table centrepieces",
        "Wall decorations",
        "Lighting (string lights, candles)",
        "Balloons & banners",
        "Tableware (plates, cups, napkins)",
        "Seating area decor",
        "Entryway/ welcome sign",
        "Photo booth backdrop",
        "Party favours packaging",
        "Cake table decor"
    ]
    
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    for i, item in enumerate(decorations):
        # Checkbox
        c.setStrokeColor(COLOR_ACCENT2)
        c.setLineWidth(0.5)
        c.rect(MARGIN + 5, y_pos - 15, 10, 10, stroke=1, fill=0)
        # Item
        c.drawString(MARGIN + 25, y_pos - 10, item)
        
        # Purchase status
        c.setFont("Helvetica", 9)
        status_x = PAGE_WIDTH - MARGIN - 100
        c.drawString(status_x, y_pos - 10, "Status: [To buy/Purchased]")
        c.setFont("Helvetica", 10)
        
        y_pos -= 25
    
    draw_footer(c)

def create_vendor_page(c, page_num):
    """Create vendor contact sheet"""
    draw_header(c, page_num, "Vendor Contact Sheet")
    
    y_pos = PAGE_HEIGHT - MARGIN - 60
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, y_pos, "Keep all your vendor contacts in one place. Track deposits, balances, and important details.")
    y_pos -= 30
    
    # Vendor table
    c.setFillColor(COLOR_ACCENT1)
    c.setFont("Helvetica-Bold", 11)
    headers = ["Vendor", "Service", "Contact", "Deposit", "Balance Due", "Notes"]
    col_widths = [
        CONTENT_WIDTH * 0.2,  # Vendor
        CONTENT_WIDTH * 0.15,  # Service
        CONTENT_WIDTH * 0.2,   # Contact
        CONTENT_WIDTH * 0.1,   # Deposit
        CONTENT_WIDTH * 0.1,   # Balance
        CONTENT_WIDTH * 0.25   # Notes
    ]
    
    x_pos = MARGIN
    for i, header in enumerate(headers):
        c.drawString(x_pos, y_pos, header)
        x_pos += col_widths[i]
    
    y_pos -= 20
    c.setStrokeColor(COLOR_ACCENT2)
    c.setLineWidth(0.5)
    c.line(MARGIN, y_pos, PAGE_WIDTH - MARGIN, y_pos)
    y_pos -=