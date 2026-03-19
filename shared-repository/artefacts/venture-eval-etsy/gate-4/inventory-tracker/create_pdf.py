#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, PageBreak, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

def create_home_inventory_pdf(output_path):
    """Create a 12-page Home Inventory Tracker PDF"""
    
    # Create canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Define colors
    primary_color = colors.HexColor('#2C2C2C')  # Dark gray
    accent_color = colors.HexColor('#8B7355')   # Brown
    light_bg = colors.HexColor('#F5F0EB')       # Light beige
    border_color = colors.HexColor('#D4C5B2')   # Light brown
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=primary_color,
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=accent_color,
        spaceAfter=8,
        alignment=TA_CENTER
    )
    
    section_style = ParagraphStyle(
        'CustomSection',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=primary_color,
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=primary_color,
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    # Page 1: Cover Page
    c.setFillColor(light_bg)
    c.rect(0, 0, width, height, fill=1)
    
    c.setFillColor(primary_color)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width/2, height/2 + 40, "Home Inventory")
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width/2, height/2 - 10, "Tracker")
    
    c.setFillColor(accent_color)
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height/2 - 60, "Organize • Document • Protect")
    
    c.setFillColor(border_color)
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width/2, 50, "RecoveriStudio | Digital Download")
    
    c.showPage()
    
    # Page 2: Instructions
    c.setFillColor(light_bg)
    c.rect(0, 0, width, height, fill=1)
    
    c.setFillColor(primary_color)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, height - 60, "How to Use This Inventory Tracker")
    
    instructions = [
        "1. Print all pages or specific room sheets as needed",
        "2. Start with one room at a time - don't feel overwhelmed",
        "3. Document each item with as much detail as possible",
        "4. Take photos of valuable items and attach receipts",
        "5. Update annually or after major purchases",
        "6. Store completed inventory in a safe place",
        "7. Share a copy with your insurance provider"
    ]
    
    c.setFont("Helvetica", 12)
    y_pos = height - 100
    for instruction in instructions:
        c.drawString(60, y_pos, instruction)
        y_pos -= 25
    
    # Add footer
    c.setFillColor(border_color)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 30, "RecoveriStudio - Page 2 of 12")
    
    c.showPage()
    
    # Room pages (pages 3-8)
    rooms = [
        ("Living Room", "Furniture, electronics, decor, artwork"),
        ("Kitchen", "Appliances, cookware, dishes, small appliances"),
        ("Bedroom", "Furniture, bedding, clothing, jewelry"),
        ("Bathroom", "Fixtures, towels, toiletries, medicine"),
        ("Office", "Electronics, furniture, supplies, documents"),
        ("Garage/Storage", "Tools, equipment, seasonal items, vehicles")
    ]
    
    for i, (room_name, room_items) in enumerate(rooms):
        # Room header
        c.setFillColor(light_bg)
        c.rect(0, height - 100, width, 100, fill=1)
        
        c.setFillColor(primary_color)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(40, height - 60, f"{room_name} Inventory")
        
        c.setFillColor(accent_color)
        c.setFont("Helvetica", 12)
        c.drawString(40, height - 85, f"Common items: {room_items}")
        
        # Table header
        c.setFillColor(border_color)
        c.rect(30, height - 150, width - 60, 30, fill=1)
        
        c.setFillColor(primary_color)
        c.setFont("Helvetica-Bold", 10)
        headers = ["Item Description", "Purchase Date", "Price", "Serial No.", "Photo/Receipt"]
        col_width = (width - 60) / 5
        
        for j, header in enumerate(headers):
            x_pos = 30 + (col_width * j) + 5
            c.drawString(x_pos, height - 140, header)
        
        # Table rows (10 rows per page)
        c.setFillColor(colors.white)
        for row in range(10):
            y_pos = height - 180 - (row * 25)
            if row % 2 == 0:
                c.setFillColor(colors.HexColor('#FAFAFA'))
            else:
                c.setFillColor(colors.white)
            c.rect(30, y_pos, width - 60, 25, fill=1)
        
        # Grid lines
        c.setStrokeColor(border_color)
        c.setLineWidth(0.5)
        for col in range(6):
            x_pos = 30 + (col_width * col)
            c.line(x_pos, height - 150, x_pos, height - 430)
        
        for row in range(12):
            y_pos = height - 150 - (row * 25)
            c.line(30, y_pos, width - 30, y_pos)
        
        # Footer
        c.setFillColor(border_color)
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(width/2, 30, f"RecoveriStudio - Page {i+3} of 12")
        
        c.showPage()
    
    # Page 9: Insurance Documentation
    c.setFillColor(light_bg)
    c.rect(0, 0, width, height, fill=1)
    
    c.setFillColor(primary_color)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height - 80, "Insurance Documentation")
    
    insurance_info = [
        "Insurance Company: ________________________",
        "Policy Number: _____________________________",
        "Agent Name: ________________________________",
        "Phone: ____________________________________",
        "Email: ____________________________________",
        "Policy Renewal Date: ______________________",
        "Total Insured Value: £_____________________"
    ]
    
    c.setFont("Helvetica", 14)
    y_pos = height - 140
    for info in insurance_info:
        c.drawString(60, y_pos, info)
        y_pos -= 40
    
    c.setFont("Helvetica", 12)
    c.drawString(40, 200, "Notes & Special Instructions:")
    c.rect(40, 100, width - 80, 80, stroke=1, fill=0)
    
    c.setFillColor(border_color)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 30, "RecoveriStudio - Page 9 of 12")
    
    c.showPage()
    
    # Page 10: Maintenance Schedule
    c.setFillColor(light_bg)
    c.rect(0, 0, width, height, fill=1)
    
    c.setFillColor(primary_color)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height - 80, "Home Maintenance Schedule")
    
    # Maintenance table
    c.setFillColor(border_color)
    c.rect(30, height - 150, width - 60, 30, fill=1)
    
    c.setFillColor(primary_color)
    c.setFont("Helvetica-Bold", 10)
    maint_headers = ["Item/System", "Last Service", "Next Due", "Service Provider", "Cost"]
    maint_col_width = (width - 60) / 5
    
    for j, header in enumerate(maint_headers):
        x_pos = 30 + (maint_col_width * j) + 5
        c.drawString(x_pos, height - 140, header)
    
    # Table rows
    for row in range(8):
        y_pos = height - 180 - (row * 30)
        if row % 2 == 0:
            c.setFillColor(colors.HexColor('#FAFAFA'))
        else:
            c.setFillColor(colors.white)
        c.rect(30, y_pos, width - 60, 30, fill=1)
    
    # Grid lines
    c.setStrokeColor(border_color)
    c.setLineWidth(0.5)
    for col in range(6):
        x_pos = 30 + (maint_col_width * col)
        c.line(x_pos, height - 150, x_pos, height - 420)
    
    for row in range(10):
        y_pos = height - 150 - (row * 30)
        c.line(30, y_pos, width - 30, y_pos)
    
    c.setFillColor(border_color)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 30, "RecoveriStudio - Page 10 of 12")
    
    c.showPage()
    
    # Page 11: Value Summary
    c.setFillColor(light_bg)
    c.rect(0, 0, width, height, fill=1)
    
    c.setFillColor(primary_color)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height - 80, "Total Value Summary")
    
    rooms_summary = [
        ("Living Room", "£__________"),
        ("Kitchen", "£__________"),
        ("Bedroom", "£__________"),
        ("Bathroom", "£__________"),
        ("Office", "£__________"),
        ("Garage/Storage", "£__________"),
        ("Other Areas", "£__________")
    ]
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(80, height - 140, "Room")
    c.drawString(width - 150, height - 140, "Total Value")
    
    c.setFont("Helvetica", 12)
    y_pos = height - 170
    for room, value in rooms_summary:
        c.drawString(80, y_pos, room)
        c.drawString(width - 150, y_pos, value)
        y_pos -= 30
    
    # Total line
    c.setFont("Helvetica-Bold", 16)
    c.drawString(80, y_pos - 20, "TOTAL HOME VALUE:")
    c.drawString(width - 150, y_pos - 20, "£__________")
    
    c.setFillColor(border_color)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 30, "RecoveriStudio - Page 11 of 12")
    
    c.showPage()
    
    # Page 12: Notes & Contacts
    c.setFillColor(light_bg)
    c.rect(0, 0, width, height, fill=1)
    
    c.setFillColor(primary_color)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height - 80, "Important Contacts & Notes")
    
    contacts = [
        "Emergency Services: 999",
        "Gas Emergency: 0800 111 999",
        "Electricity Emergency: 105",
        "Water Emergency: [Local Provider]",
        "Police Non-Emergency: 101",
        "NHS Non-Emergency: 111"
    ]
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, height - 140, "Emergency Contacts:")
    
    c.setFont("Helvetica", 12)
    y_pos = height - 170
    for contact in contacts:
        c.drawString(80, y_pos, contact)
        y_pos -= 25
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, y_pos - 20, "Additional Notes:")
    c.rect(60, 100, width - 120, y_pos - 140, stroke=1, fill=0)
    
    c.setFillColor(border_color)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 30, "RecoveriStudio - Page 12 of 12 | studio@recoveri.io")
    
    c.save()
    print(f"PDF created successfully: {output_path}")

if __name__ == "__main__":
    output_path = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/inventory-tracker/product.pdf"
    create_home_inventory_pdf(output_path)