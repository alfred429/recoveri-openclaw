#!/usr/bin/env python3
"""
Create Wedding Budget Planner PDF for RecoveriStudio Etsy shop.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Color palette from RecoveriStudio brand guidelines
COLORS = {
    'background': colors.HexColor('#F5F0EB'),
    'text_dark': colors.HexColor('#2C2C2C'),
    'accent': colors.HexColor('#8B7355'),
    'light_accent': colors.HexColor('#D4C5B2'),
    'table_header': colors.HexColor('#E8DFD6'),
    'table_row_even': colors.HexColor('#F9F6F3'),
}

def create_wedding_budget_planner(output_path):
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
    
    # Get default styles
    styles = getSampleStyleSheet()
    
    # Custom styles - use unique names
    styles.add(ParagraphStyle(
        name='WeddingTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=COLORS['accent'],
        spaceAfter=12,
        alignment=TA_CENTER
    ))
    
    styles.add(ParagraphStyle(
        name='WeddingHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=COLORS['accent'],
        spaceAfter=6,
        spaceBefore=12
    ))
    
    styles.add(ParagraphStyle(
        name='WeddingHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=COLORS['text_dark'],
        spaceAfter=4,
        spaceBefore=8
    ))
    
    styles.add(ParagraphStyle(
        name='WeddingBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLORS['text_dark'],
        spaceAfter=6
    ))
    
    styles.add(ParagraphStyle(
        name='WeddingFooter',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.gray,
        alignment=TA_CENTER
    ))
    
    # Story elements
    story = []
    
    # Cover page
    story.append(Paragraph("Wedding Budget Planner", styles['WeddingTitle']))
    story.append(Spacer(1, 20*mm))
    
    story.append(Paragraph("Your Complete Financial Planning Solution", styles['WeddingHeading1']))
    story.append(Spacer(1, 30*mm))
    
    cover_text = """
    <para>
    Take control of your wedding finances with this comprehensive budget planner.<br/>
    Track every expense, compare vendors, and stay on budget for your special day.
    </para>
    """
    story.append(Paragraph(cover_text, styles['WeddingBody']))
    story.append(Spacer(1, 40*mm))
    
    story.append(Paragraph("RecoveriStudio", styles['WeddingFooter']))
    story.append(PageBreak())
    
    # Page 1: Introduction & How to Use
    story.append(Paragraph("Introduction", styles['Heading1']))
    
    intro_text = """
    <para>
    Congratulations on your engagement! Planning a wedding is an exciting journey, 
    but it can also be financially stressful. This Wedding Budget Planner is designed 
    to help you organize all your expenses in one place, ensuring you can enjoy 
    your special day without financial worries.
    </para>
    """
    story.append(Paragraph(intro_text, styles['BodyText']))
    
    story.append(Paragraph("How to Use This Planner", styles['Heading2']))
    
    how_to_text = """
    <para>
    1. <b>Budget Overview</b> (Page 2): Start by setting your total budget and allocating amounts to each category.<br/>
    2. <b>Vendor Tracking</b> (Pages 3-6): Compare quotes and track payments for each vendor.<br/>
    3. <b>Payment Schedule</b> (Page 7): Record due dates and payment amounts.<br/>
    4. <b>Guest Management</b> (Page 8): Track guests, RSVPs, and meal preferences.<br/>
    5. <b>Honeymoon Planning</b> (Page 9): Budget for your post-wedding getaway.<br/>
    6. <b>Contingency Planning</b> (Page 10): Set aside funds for unexpected expenses.<br/>
    7. <b>Gift Registry</b> (Page 11): Track gifts received and thank-you notes sent.<br/>
    8. <b>Review Regularly</b>: Update your planner monthly or after each major decision.
    </para>
    """
    story.append(Paragraph(how_to_text, styles['BodyText']))
    story.append(PageBreak())
    
    # Page 2: Budget Overview
    story.append(Paragraph("Budget Overview", styles['Heading1']))
    
    budget_text = """
    <para>
    Start by determining your total wedding budget. Consider contributions from yourselves, 
    parents, or other sources. Then allocate amounts to each category below.
    </para>
    """
    story.append(Paragraph(budget_text, styles['BodyText']))
    
    # Budget table
    budget_data = [
        ['Category', 'Estimated Cost', 'Actual Cost', 'Difference', 'Notes'],
        ['Venue & Rental', '£__________', '£__________', '£__________', ''],
        ['Catering & Bar', '£__________', '£__________', '£__________', ''],
        ['Photography & Video', '£__________', '£__________', '£__________', ''],
        ['Attire & Accessories', '£__________', '£__________', '£__________', ''],
        ['Rings', '£__________', '£__________', '£__________', ''],
        ['Florals & Decor', '£__________', '£__________', '£__________', ''],
        ['Entertainment', '£__________', '£__________', '£__________', ''],
        ['Stationery', '£__________', '£__________', '£__________', ''],
        ['Transportation', '£__________', '£__________', '£__________', ''],
        ['Wedding Party Gifts', '£__________', '£__________', '£__________', ''],
        ['Beauty & Wellness', '£__________', '£__________', '£__________', ''],
        ['Ceremony Fees', '£__________', '£__________', '£__________', ''],
        ['Contingency (10%)', '£__________', '£__________', '£__________', ''],
        ['TOTAL', '£__________', '£__________', '£__________', '']
    ]
    
    budget_table = Table(budget_data, colWidths=[60*mm, 30*mm, 30*mm, 30*mm, 40*mm])
    budget_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['table_header']),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLORS['text_dark']),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (3, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, -1), (-1, -1), COLORS['light_accent']),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    
    story.append(Spacer(1, 6))
    story.append(budget_table)
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("Total Budget: £__________", styles['Heading2']))
    story.append(Paragraph("Amount Allocated: £__________", styles['BodyText']))
    story.append(Paragraph("Remaining: £__________", styles['BodyText']))
    
    story.append(PageBreak())
    
    # Page 3: Vendor Comparison - Venue
    story.append(Paragraph("Vendor Comparison: Venue", styles['Heading1']))
    
    venue_data = [
        ['Vendor', 'Quote', 'Deposit', 'Balance Due', 'Date', 'Notes'],
        ['', '£__________', '£__________', '£__________', '', ''],
        ['', '£__________', '£__________', '£__________', '', ''],
        ['', '£__________', '£__________', '£__________', '', ''],
        ['SELECTED:', '£__________', '£__________', '£__________', '', '']
    ]
    
    venue_table = Table(venue_data, colWidths=[50*mm, 25*mm, 25*mm, 25*mm, 25*mm, 40*mm])
    venue_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['table_header']),
        ('BACKGROUND', (0, -1), (-1, -1), COLORS['light_accent']),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 0), (3, -1), 'RIGHT'),
    ]))
    
    story.append(venue_table)
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("Venue Details", styles['Heading2']))
    story.append(Paragraph("Capacity: __________", styles['BodyText']))
    story.append(Paragraph("Included: __________", styles['BodyText']))
    story.append(Paragraph("Restrictions: __________", styles['BodyText']))
    
    story.append(PageBreak())
    
    # Page 4: Vendor Comparison - Catering
    story.append(Paragraph("Vendor Comparison: Catering", styles['Heading1']))
    
    catering_data = [
        ['Vendor', 'Per Person', 'Total', 'Deposit', 'Menu Options', 'Notes'],
        ['', '£__________', '£__________', '£__________', '', ''],
        ['', '£__________', '£__________', '£__________', '', ''],
        ['', '£__________', '£__________', '£__________', '', ''],
        ['SELECTED:', '£__________', '£__________', '£__________', '', '']
    ]
    
    catering_table = Table(catering_data, colWidths=[45*mm, 20*mm, 20*mm, 20*mm, 35*mm, 40*mm])
    catering_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['table_header']),
        ('BACKGROUND', (0, -1), (-1, -1), COLORS['light_accent']),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 0), (3, -1), 'RIGHT'),
    ]))
    
    story.append(catering_table)
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("Guest Count: __________", styles['BodyText']))
    story.append(Paragraph("Dietary Requirements: __________", styles['BodyText']))
    
    story.append(PageBreak())
    
    # Page 5: Payment Schedule
    story.append(Paragraph("Payment Schedule", styles['Heading1']))
    
    payment_text = """
    <para>
    Track all payments and due dates to avoid late fees and ensure vendors are paid on time.
    </para>
    """
    story.append(Paragraph(payment_text, styles['BodyText']))
    
    payment_data = [
        ['Vendor', 'Amount Due', 'Due Date', 'Paid?', 'Date Paid', 'Receipt #'],
        ['Venue Deposit', '£__________', '', '□', '', ''],
        ['Catering Deposit', '£__________', '', '□', '', ''],
        ['Photographer', '£__________', '', '□', '', ''],
        ['Florist', '£__________', '', '□', '', ''],
        ['Entertainment', '£__________', '', '□', '', ''],
        ['Attire', '£__________', '', '□', '', ''],
        ['Stationery', '£__________', '', '□', '', ''],
        ['Venue Balance', '£__________', '', '□', '', ''],
        ['Catering Balance', '£__________', '', '□', '', ''],
        ['Other', '£__________', '', '□', '', ''],
        ['Other', '£__________', '', '□', '', '']
    ]
    
    payment_table = Table(payment_data, colWidths=[50*mm, 25*mm, 25*mm, 15*mm, 25*mm, 30*mm])
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['table_header']),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('ALIGN', (3, 0), (3, -1), 'CENTER'),
    ]))
    
    story.append(Spacer(1, 6))
    story.append(payment_table)
    
    story.append(PageBreak())
    
    # Page 6: Guest List & RSVP Tracker
    story.append(Paragraph("Guest List & RSVP Tracker", styles['Heading1']))
    
    guest_data = [
        ['Name', 'Invited?', 'RSVP', 'Meal', 'Gift', 'Thank You'],
        ['', '□', '□ Yes □ No', '', '', '□'],
        ['', '□', '□ Yes □ No', '', '', '□'],
        ['', '□', '□ Yes □ No', '', '', '□'],
        ['', '□', '□ Yes □ No', '', '', '□'],
        ['', '□', '□ Yes □ No', '', '', '□'],
        ['', '□', '□ Yes □ No', '', '', '□'],
        ['', '□', '□ Yes □ No', '', '', '□'],
        ['', '□', '□ Yes □ No', '', '', '□'],
        ['', '□', '□ Yes □ No', '', '', '□'],
        ['', '□', '□ Yes □ No', '', '', '□'],
        ['', '□', '□ Yes □ No', '', '', '□']
    ]
    
    guest_table = Table(guest_data, colWidths=[50*mm, 20*mm, 30*mm, 25*mm, 25*mm, 20*mm])
    guest_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['table_header']),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ]))
    
    story.append(guest_table)
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("Total Invited: __________", styles['BodyText']))
    story.append(Paragraph("Total Attending: __________", styles['BodyText']))
    story.append(Paragraph("Meal Counts: __________", styles['BodyText']))
    
    story.append(PageBreak())
    
    # Page 7: Honeymoon Budget
    story.append(Paragraph("Honeymoon Budget", styles['Heading1']))
    
    honeymoon_data = [
        ['Expense', 'Estimated', 'Actual', 'Paid', 'Notes'],
        ['Flights', '£__________', '£__________', '□', ''],
        ['Accommodation', '£__________', '£__________', '□', ''],
        ['Transportation', '£__________', '£__________', '□', ''],
        ['Activities', '£__________', '£__________', '□', ''],
        ['Food & Drink', '£__________', '£__________', '□', ''],
        ['Shopping', '£__________', '£__________', '□', ''],
        ['Travel Insurance', '£__________', '£__________', '□', ''],
        ['Visa/Passport', '£__________', '£__________', '□', ''],
        ['Emergency Fund', '£__________', '£__________', '□', ''],
        ['TOTAL', '£__________', '£__________', '', '']
    ]
    
    honeymoon_table = Table(honeymoon_data, colWidths=[50*mm, 30*mm, 30*mm, 20*mm, 40*mm])
    honeymoon_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['table_header']),
        ('BACKGROUND', (0, -1), (-1, -1), COLORS['light_accent']),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 0), (2, -1), 'RIGHT'),
        ('ALIGN', (3, 0), (3, -2), 'CENTER'),
    ]))
    
    story.append(honeymoon_table)
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("Destination: __________", styles['BodyText']))
    story.append(Paragraph("Dates: __________ to __________", styles['BodyText']))
    
    story.append(PageBreak())
    
    # Page 8: Contingency & Emergency Fund
    story.append(Paragraph("Contingency & Emergency Fund", styles['Heading1']))
    
    contingency_text = """
    <para>
    It's recommended to set aside 10-15% of your total budget for unexpected expenses. 
    Common unexpected costs include weather-related changes, last-minute guest additions, 
    vendor cancellations, or additional decor needs.
    </para>
    """
    story.append(Paragraph(contingency_text, styles['BodyText']))
    
    contingency_data = [
        ['Potential Issue', 'Estimated Cost', 'Priority', 'Notes'],
        ['Weather backup plan', '£__________', 'High/Med/Low', ''],
        ['Additional guests', '£__________', 'High/Med/Low', ''],
        ['Vendor cancellation fee', '£__________', 'High/Med/Low', ''],
        ['Attire alterations', '£__________', 'High/Med/Low', ''],
        ['Transportation issues', '£__________', 'High/Med/Low', ''],
        ['Last-minute decor', '£__________', 'High/Med/Low', ''],
        ['Other', '£__________', 'High/Med/Low', ''],
        ['Other', '£__________', 'High/Med/Low', ''],
        ['TOTAL CONTINGENCY', '£__________', '', '']
    ]
    
    contingency_table = Table(contingency_data, colWidths=[60*mm, 30*mm, 40*mm, 50*mm])
    contingency_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['table_header']),
        ('BACKGROUND', (0, -1), (-1, -1), COLORS['light_accent']),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    
    story.append(Spacer(1, 6))
    story.append(contingency_table)
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("Contingency Fund Allocated: £__________", styles['BodyText']))
    story.append(Paragraph("Amount Used: £__________", styles['BodyText']))
    story.append(Paragraph("Remaining: £__________", styles['BodyText']))
    
    story.append(PageBreak())
    
    # Page 9: Gift Registry Tracker
    story.append(Paragraph("Gift Registry Tracker", styles['Heading1']))
    
    gift_data = [
        ['Item', 'Store', 'Price', 'Purchased?', 'By Whom', 'Thank You Sent'],
        ['', '', '£__________', '□', '', '□'],
        ['', '', '£__________', '□', '', '□'],
        ['', '', '£__________', '□', '', '□'],
        ['', '', '£__________', '□', '', '□'],
        ['', '', '£__________', '□', '', '□'],
        ['', '', '£__________', '□', '', '□'],
        ['', '', '£__________', '□', '', '□'],
        ['', '', '£__________', '□', '', '□'],
        ['', '', '£__________', '□', '', '□'],
        ['', '', '£__________', '□', '', '□']
    ]
    
    gift_table = Table(gift_data, colWidths=[50*mm, 40*mm, 25*mm, 25*mm, 30*mm, 30*mm])
    gift_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['table_header']),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('ALIGN', (3, 0), (-1, -1), 'CENTER'),
    ]))
    
    story.append(gift_table)
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("Cash Gifts Received: £__________", styles['BodyText']))
    story.append(Paragraph("Thank You Notes Sent: __________ of __________", styles['BodyText']))
    
    story.append(PageBreak())
    
    # Page 10: Notes & Final Checklist
    story.append(Paragraph("Final Notes & Checklist", styles['Heading1']))
    
    checklist_text = """
    <para>
    <b>One Month Before:</b><br/>
    □ Finalize guest count with caterer<br/>
    □ Confirm all vendor arrangements<br/>
    □ Create seating chart<br/>
    □ Pick up marriage license<br/>
    □ Final dress fitting<br/>
    <br/>
    <b>Two Weeks Before:</b><br/>
    □ Confirm delivery times with all vendors<br/>
    □ Create day-of timeline<br/>
    □ Pack for honeymoon<br/>
    □ Break in wedding shoes<br/>
    □ Final payment to vendors<br/>
    <br/>
    <b>One Week Before:</b><br/>
    □ Delegate day-of tasks<br/>
    □ Confirm honeymoon travel<br/>
    □ Get final haircut/color<br/>
    □ Practice vows<br/>
    □ Pack emergency kit<br/>
    <br/>
    <b>Day Before:</b><br/>
    □ Get plenty of rest<br/>
    □ Eat well and stay hydrated<br/>
    □ Charge phones/cameras<br/>
    □ Lay out everything for tomorrow<br/>
    □ Take a deep breath - you've got this!
    </para>
    """
    story.append(Paragraph(checklist_text, styles['BodyText']))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("Personal Notes", styles['Heading2']))
    story.append(Paragraph("________________________________________________________________", styles['BodyText']))
    story.append(Paragraph("________________________________________________________________", styles['BodyText']))
    story.append(Paragraph("________________________________________________________________", styles['BodyText']))
    story.append(Paragraph("________________________________________________________________", styles['BodyText']))
    
    # Footer on every page
    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.gray)
        canvas.drawString(15*mm, 10*mm, "RecoveriStudio | Wedding Budget Planner")
        canvas.drawRightString(195*mm, 10*mm, "Page %d" % doc.page)
        canvas.restoreState()
    
    # Build PDF
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    
    print(f"PDF created successfully: {output_path}")

if __name__ == "__main__":
    output_path = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/wedding-budget-planner/product.pdf"
    create_wedding_budget_planner(output_path)