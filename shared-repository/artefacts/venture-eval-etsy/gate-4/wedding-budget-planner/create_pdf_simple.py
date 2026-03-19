#!/usr/bin/env python3
"""
Create Wedding Budget Planner PDF - Simplified version
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

# Color palette
COLORS = {
    'accent': colors.HexColor('#8B7355'),
    'text_dark': colors.HexColor('#2C2C2C'),
    'light_accent': colors.HexColor('#D4C5B2'),
    'table_header': colors.HexColor('#E8DFD6'),
}

def create_pdf(output_path):
    """Create the Wedding Budget Planner PDF."""
    
    # Create document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=20*mm,
        bottomMargin=20*mm,
        leftMargin=15*mm,
        rightMargin=15*mm
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Modify existing styles
    styles['Title'].fontSize = 24
    styles['Title'].textColor = COLORS['accent']
    styles['Title'].alignment = TA_CENTER
    
    styles['Heading1'].fontSize = 16
    styles['Heading1'].textColor = COLORS['accent']
    styles['Heading1'].spaceAfter = 6
    
    styles['Heading2'].fontSize = 14
    styles['Heading2'].textColor = COLORS['text_dark']
    styles['Heading2'].spaceAfter = 4
    
    styles['Normal'].fontSize = 10
    styles['Normal'].textColor = COLORS['text_dark']
    
    # Story elements
    story = []
    
    # Cover page
    story.append(Paragraph("Wedding Budget Planner", styles['Title']))
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph("Your Complete Financial Planning Solution", styles['Heading1']))
    story.append(Spacer(1, 30*mm))
    
    cover_text = "Take control of your wedding finances with this comprehensive budget planner. Track every expense, compare vendors, and stay on budget for your special day."
    story.append(Paragraph(cover_text, styles['Normal']))
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph("RecoveriStudio", styles['Normal']))
    story.append(PageBreak())
    
    # Page 1: Budget Overview
    story.append(Paragraph("Budget Overview", styles['Heading1']))
    story.append(Paragraph("Start by determining your total wedding budget. Allocate amounts to each category below.", styles['Normal']))
    story.append(Spacer(1, 10))
    
    # Simple budget table
    budget_data = [
        ['Category', 'Estimated', 'Actual'],
        ['Venue', '£__________', '£__________'],
        ['Catering', '£__________', '£__________'],
        ['Photography', '£__________', '£__________'],
        ['Attire', '£__________', '£__________'],
        ['Florals', '£__________', '£__________'],
        ['Entertainment', '£__________', '£__________'],
        ['Stationery', '£__________', '£__________'],
        ['Transport', '£__________', '£__________'],
        ['TOTAL', '£__________', '£__________']
    ]
    
    table = Table(budget_data, colWidths=[80*mm, 45*mm, 45*mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['table_header']),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, -1), (-1, -1), COLORS['light_accent']),
    ]))
    
    story.append(table)
    story.append(PageBreak())
    
    # Page 2: Payment Schedule
    story.append(Paragraph("Payment Schedule", styles['Heading1']))
    story.append(Paragraph("Track payments and due dates:", styles['Normal']))
    story.append(Spacer(1, 10))
    
    payment_data = [
        ['Vendor', 'Amount', 'Due Date', 'Paid'],
        ['Venue Deposit', '£__________', '__________', '□'],
        ['Catering Deposit', '£__________', '__________', '□'],
        ['Photographer', '£__________', '__________', '□'],
        ['Florist', '£__________', '__________', '□'],
        ['Entertainment', '£__________', '__________', '□']
    ]
    
    payment_table = Table(payment_data, colWidths=[70*mm, 40*mm, 40*mm, 30*mm])
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['table_header']),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('ALIGN', (3, 0), (3, -1), 'CENTER'),
    ]))
    
    story.append(payment_table)
    story.append(PageBreak())
    
    # Page 3: Guest List
    story.append(Paragraph("Guest List", styles['Heading1']))
    
    guest_data = [
        ['Name', 'RSVP', 'Meal'],
        ['__________', '□ Yes □ No', '__________'],
        ['__________', '□ Yes □ No', '__________'],
        ['__________', '□ Yes □ No', '__________'],
        ['__________', '□ Yes □ No', '__________'],
        ['__________', '□ Yes □ No', '__________']
    ]
    
    guest_table = Table(guest_data, colWidths=[80*mm, 50*mm, 50*mm])
    guest_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['table_header']),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ]))
    
    story.append(guest_table)
    
    # Footer function
    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.gray)
        canvas.drawString(15*mm, 10*mm, "RecoveriStudio | Wedding Budget Planner")
        canvas.drawRightString(195*mm, 10*mm, "Page %d" % doc.page)
        canvas.restoreState()
    
    # Build PDF
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    
    print(f"PDF created: {output_path}")

if __name__ == "__main__":
    output_path = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/wedding-budget-planner/product.pdf"
    create_pdf(output_path)