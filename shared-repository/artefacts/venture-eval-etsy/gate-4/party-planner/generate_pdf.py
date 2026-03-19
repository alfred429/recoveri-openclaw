#!/usr/bin/env python3
"""
Simple Party Planner PDF generator for RecoveriStudio
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import os

# Colors
BG_COLOR = HexColor('#F5F0EB')
TEXT_COLOR = HexColor('#2C2C2C')
ACCENT1 = HexColor('#8B7355')
ACCENT2 = HexColor('#D4C5B2')

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 20 * mm

def create_pdf():
    """Create the complete Party Planner PDF"""
    output_path = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/party-planner/product.pdf"
    c = canvas.Canvas(output_path, pagesize=A4)
    
    # Page 1: Cover
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    
    c.setFillColor(TEXT_COLOR)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 + 40, "Party Planner")
    
    c.setFont("Helvetica", 24)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2, "Digital Printable Template")
    
    c.setFont("Helvetica", 14)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 60, "Plan the perfect party with our comprehensive template")
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 90, "Includes guest lists, budget tracking, timeline checklist,")
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 120, "menu planning, decorations, vendor contacts, and more.")
    
    # Footer
    c.setFillColor(ACCENT1)
    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_WIDTH/2, MARGIN, "© RecoveriStudio | studio@recoveri.io")
    
    c.showPage()
    
    # Page 2: Guest List
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    
    c.setFillColor(ACCENT1)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 30, "Guest List & RSVP Tracker")
    
    c.setFillColor(TEXT_COLOR)
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 80, "Track your guests and their RSVP status:")
    
    y = PAGE_HEIGHT - MARGIN - 120
    for i in range(1, 16):
        c.setStrokeColor(ACCENT2)
        c.setLineWidth(0.5)
        c.rect(MARGIN, y - 15, PAGE_WIDTH - 2*MARGIN, 20, stroke=1, fill=0)
        c.setFillColor(TEXT_COLOR)
        c.setFont("Helvetica", 10)
        c.drawString(MARGIN + 10, y - 10, f"Guest {i}: [Name] | [Contact] | [RSVP Status] | [Notes]")
        y -= 30
    
    c.setFillColor(ACCENT1)
    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_WIDTH/2, MARGIN, "© RecoveriStudio | studio@recoveri.io")
    
    c.showPage()
    
    # Page 3: Budget Planner
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    
    c.setFillColor(ACCENT1)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 30, "Budget Planner")
    
    c.setFillColor(TEXT_COLOR)
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 80, "Total Budget: £ [Enter amount]")
    c.drawString(PAGE_WIDTH/2, PAGE_HEIGHT - MARGIN - 80, "Remaining: £ [Auto-calculated]")
    
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
    
    y = PAGE_HEIGHT - MARGIN - 120
    for category in categories:
        c.setStrokeColor(ACCENT2)
        c.setLineWidth(0.5)
        c.rect(MARGIN, y - 15, PAGE_WIDTH - 2*MARGIN, 20, stroke=1, fill=0)
        c.setFillColor(TEXT_COLOR)
        c.setFont("Helvetica", 10)
        c.drawString(MARGIN + 10, y - 10, f"{category}: Budget £ [ ] | Actual £ [ ] | Difference £ [ ] | Notes: [ ]")
        y -= 25
    
    c.setFillColor(ACCENT1)
    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_WIDTH/2, MARGIN, "© RecoveriStudio | studio@recoveri.io")
    
    c.showPage()
    
    # Page 4: Timeline
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    
    c.setFillColor(ACCENT1)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 30, "6-Week Party Timeline")
    
    weeks = [
        ("6 WEEKS BEFORE", "Set budget, Choose date, Create guest list, Book venue"),
        ("4 WEEKS BEFORE", "Send invitations, Plan menu, Book caterer, Order decorations"),
        ("2 WEEKS BEFORE", "Confirm RSVPs, Finalise menu, Purchase drinks, Plan seating"),
        ("1 WEEK BEFORE", "Confirm vendors, Prepare decorations, Shop for non-perishables"),
        ("2 DAYS BEFORE", "Grocery shopping, Prepare make-ahead food, Charge cameras"),
        ("PARTY DAY", "Set up venue, Prepare food, Welcome guests, Enjoy your party!")
    ]
    
    y = PAGE_HEIGHT - MARGIN - 80
    for week, tasks in weeks:
        c.setFillColor(ACCENT1)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(MARGIN, y, week)
        y -= 25
        
        c.setFillColor(TEXT_COLOR)
        c.setFont("Helvetica", 11)
        c.drawString(MARGIN + 20, y, tasks)
        y -= 40
    
    c.setFillColor(ACCENT1)
    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_WIDTH/2, MARGIN, "© RecoveriStudio | studio@recoveri.io")
    
    c.showPage()
    
    # Page 5: Menu Planner
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    
    c.setFillColor(ACCENT1)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 30, "Menu & Catering Planner")
    
    sections = ["Appetisers & Starters", "Main Courses", "Side Dishes", "Desserts", "Drinks"]
    
    y = PAGE_HEIGHT - MARGIN - 80
    for section in sections:
        c.setFillColor(ACCENT1)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(MARGIN, y, section)
        y -= 25
        
        for i in range(1, 4):
            c.setStrokeColor(ACCENT2)
            c.setLineWidth(0.5)
            c.rect(MARGIN, y - 15, PAGE_WIDTH - 2*MARGIN, 20, stroke=1, fill=0)
            c.setFillColor(TEXT_COLOR)
            c.setFont("Helvetica", 10)
            c.drawString(MARGIN + 10, y - 10, f"Item {i}: [Name] | Qty: [ ] | Special Diet: [ ] | Notes: [ ]")
            y -= 30
        y -= 10
    
    c.setFillColor(ACCENT1)
    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_WIDTH/2, MARGIN, "© RecoveriStudio | studio@recoveri.io")
    
    c.showPage()
    
    # Page 6: Decorations
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    
    c.setFillColor(ACCENT1)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 30, "Decorations & Theme Ideas")
    
    c.setFillColor(TEXT_COLOR)
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 80, "Party Theme: [Describe your theme, colours, and aesthetic]")
    
    decorations = [
        "Table centrepieces",
        "Wall decorations", 
        "Lighting (string lights, candles)",
        "Balloons & banners",
        "Tableware (plates, cups, napkins)",
        "Seating area decor",
        "Entryway welcome sign",
        "Photo booth backdrop",
        "Party favours packaging",
        "Cake table decor"
    ]
    
    y = PAGE_HEIGHT - MARGIN - 120
    for i, item in enumerate(decorations, 1):
        c.setStrokeColor(ACCENT2)
        c.setLineWidth(0.5)
        c.rect(MARGIN, y - 15, PAGE_WIDTH - 2*MARGIN, 20, stroke=1, fill=0)
        c.setFillColor(TEXT_COLOR)
        c.setFont("Helvetica", 10)
        c.drawString(MARGIN + 10, y - 10, f"{i}. {item} - Status: [To buy / Purchased] - Notes: [ ]")
        y -= 25
    
    c.setFillColor(ACCENT1)
    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_WIDTH/2, MARGIN, "© RecoveriStudio | studio@recoveri.io")
    
    c.showPage()
    
    # Page 7: Vendor Contacts
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    
    c.setFillColor(ACCENT1)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 30, "Vendor Contact Sheet")
    
    vendors = ["Venue", "Caterer", "Baker", "Decorator", "Entertainment", "Photographer", "Florist", "Rental"]
    
    y = PAGE_HEIGHT - MARGIN - 80
    for vendor in vendors:
        c.setStrokeColor(ACCENT2)
        c.setLineWidth(0.5)
        c.rect(MARGIN, y - 15, PAGE_WIDTH - 2*MARGIN, 20, stroke=1, fill=0)
        c.setFillColor(TEXT_COLOR)
        c.setFont("Helvetica", 10)
        c.drawString(MARGIN + 10, y - 10, f"{vendor}: [Company] | Contact: [ ] | Deposit: £ [ ] | Balance: £ [ ] | Notes: [ ]")
        y -= 25
    
    c.setFillColor(ACCENT1)
    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_WIDTH/2, MARGIN, "© RecoveriStudio | studio@recoveri.io")
    
    c.showPage()
    
    # Page 8: Seating & Thank Yous
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    
    c.setFillColor(ACCENT1)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 30, "Seating Chart & Thank You Notes")
    
    c.setFillColor(TEXT_COLOR)
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 80, "Seating Chart: [Draw your table arrangement here]")
    
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 160, "Thank You Notes Tracker:")
    
    y = PAGE_HEIGHT - MARGIN - 190
    for i in range(1, 9):
        c.setStrokeColor(ACCENT2)
        c.setLineWidth(0.5)
        c.rect(MARGIN, y - 15, PAGE_WIDTH - 2*MARGIN, 20, stroke=1, fill=0)
        c.setFillColor(TEXT_COLOR)
        c.setFont("Helvetica", 10)
        c.drawString(MARGIN + 10, y - 10, f"Guest {i}: Gift [Received?] | Thank You [Sent?] | Date: [ ] | Notes: [ ]")
        y -= 25
    
    c.setFillColor(ACCENT1)
    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_WIDTH/2, MARGIN, "© RecoveriStudio | studio@recoveri.io")
    
    # Save PDF
    c.save()
    
    print(f"✓ PDF created: {output_path}")
    print(f"✓ File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    print(f"✓ Pages: 8")
    print(f"✓ Format: A4 (210x297mm)")
    print(f"✓ Colors: RecoveriStudio palette")
    print(f"✓ Branding: RecoveriStudio footer on every page")

if __name__ == "__main__":
    create_pdf()