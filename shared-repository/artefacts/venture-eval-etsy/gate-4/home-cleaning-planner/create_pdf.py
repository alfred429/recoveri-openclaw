#!/usr/bin/env python3
"""
Create Home Cleaning Planner PDF for RecoveriStudio Etsy shop.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

# Color palette from RecoveriStudio brand guidelines
COLORS = {
    'background': colors.HexColor('#F5F0EB'),
    'dark_text': colors.HexColor('#2C2C2C'),
    'accent': colors.HexColor('#8B7355'),
    'light_accent': colors.HexColor('#D4C5B2'),
    'white': colors.white
}

def create_pdf(output_path):
    """Create the Home Cleaning Planner PDF."""
    
    # Create document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=COLORS['dark_text'],
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=COLORS['accent'],
        spaceAfter=8,
        alignment=TA_LEFT
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=COLORS['accent'],
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=COLORS['dark_text'],
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    # Story elements
    story = []
    
    # Cover page
    story.append(Paragraph("Home Cleaning Planner", title_style))
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph("Organize Your Cleaning Routine", heading_style))
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph("Daily • Weekly • Monthly • Seasonal", subheading_style))
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph("RecoveriStudio", normal_style))
    story.append(PageBreak())
    
    # Page 1: Daily Cleaning Checklist
    story.append(Paragraph("Daily Cleaning Checklist", heading_style))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Complete these tasks every day to maintain a clean home:", normal_style))
    
    daily_tasks = [
        ["Task", "Completed"],
        ["Make beds", ""],
        ["Wipe down kitchen counters", ""],
        ["Load/unload dishwasher", ""],
        ["Quick bathroom wipe", ""],
        ["Pick up clutter", ""],
        ["Sweep/vacuum high-traffic areas", ""],
        ["Take out trash/recycling", ""],
        ["Wipe dining table", ""]
    ]
    
    daily_table = Table(daily_tasks, colWidths=[120*mm, 50*mm])
    daily_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['light_accent']),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLORS['dark_text']),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), COLORS['dark_text']),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(daily_table)
    story.append(PageBreak())
    
    # Page 2: Weekly Cleaning Schedule
    story.append(Paragraph("Weekly Cleaning Schedule", heading_style))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Assign specific cleaning tasks to each day of the week:", normal_style))
    
    weekly_schedule = [
        ["Day", "Tasks", "Completed"],
        ["Monday", "Bathrooms: clean toilets, sinks, mirrors", ""],
        ["Tuesday", "Dusting: all surfaces, shelves, electronics", ""],
        ["Wednesday", "Vacuuming: all carpets and rugs", ""],
        ["Thursday", "Kitchen: clean appliances, inside fridge", ""],
        ["Friday", "Mopping: hard floors, entryways", ""],
        ["Saturday", "Laundry: wash, fold, put away", ""],
        ["Sunday", "Planning: review next week's schedule", ""]
    ]
    
    weekly_table = Table(weekly_schedule, colWidths=[40*mm, 100*mm, 30*mm])
    weekly_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['light_accent']),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLORS['dark_text']),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), COLORS['dark_text']),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(weekly_table)
    story.append(PageBreak())
    
    # Page 3: Monthly Deep Cleaning Planner
    story.append(Paragraph("Monthly Deep Cleaning Planner", heading_style))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Complete these tasks once a month for a thorough clean:", normal_style))
    
    monthly_tasks = [
        ["Area", "Tasks", "Date Completed"],
        ["Kitchen", "Clean oven, degrease range hood, organize pantry", ""],
        ["Bathrooms", "Descale showerheads, clean grout, wash shower curtain", ""],
        ["Living Areas", "Wash windows, clean under furniture, dust light fixtures", ""],
        ["Bedrooms", "Wash bedding, rotate mattress, organize closets", ""],
        ["Whole House", "Check smoke detectors, clean vents, wipe baseboards", ""]
    ]
    
    monthly_table = Table(monthly_tasks, colWidths=[50*mm, 90*mm, 30*mm])
    monthly_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['light_accent']),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLORS['dark_text']),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), COLORS['dark_text']),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(monthly_table)
    story.append(PageBreak())
    
    # Page 4: Room-by-Room Cleaning Guide (Part 1)
    story.append(Paragraph("Room-by-Room Cleaning Guide", heading_style))
    story.append(Spacer(1, 5*mm))
    
    story.append(Paragraph("Kitchen", subheading_style))
    kitchen_tasks = [
        "• Clean countertops and backsplash",
        "• Wipe down appliances (outside)",
        "• Clean sink and faucet",
        "• Sweep and mop floor",
        "• Take out trash and recycling",
        "• Wipe cabinet fronts",
        "• Clean microwave (inside and out)"
    ]
    for task in kitchen_tasks:
        story.append(Paragraph(task, normal_style))
    
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Bathroom", subheading_style))
    bathroom_tasks = [
        "• Clean toilet (inside and out)",
        "• Scrub shower/tub",
        "• Clean sink and counter",
        "• Wipe mirrors",
        "• Restock supplies",
        "• Empty trash",
        "• Sweep and mop floor"
    ]
    for task in bathroom_tasks:
        story.append(Paragraph(task, normal_style))
    story.append(PageBreak())
    
    # Page 5: Room-by-Room Cleaning Guide (Part 2)
    story.append(Paragraph("Living Room", subheading_style))
    living_tasks = [
        "• Dust all surfaces",
        "• Vacuum carpets/rugs",
        "• Clean windows/mirrors",
        "• Fluff pillows and cushions",
        "• Organize media/books",
        "• Wipe electronics",
        "• Empty trash bins"
    ]
    for task in living_tasks:
        story.append(Paragraph(task, normal_style))
    
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Bedroom", subheading_style))
    bedroom_tasks = [
        "• Change bedding",
        "• Dust furniture",
        "• Vacuum floor",
        "• Organize closet",
        "• Wipe surfaces",
        "• Empty trash",
        "• Air out room"
    ]
    for task in bedroom_tasks:
        story.append(Paragraph(task, normal_style))
    story.append(PageBreak())
    
    # Page 6: Cleaning Supplies Inventory
    story.append(Paragraph("Cleaning Supplies Inventory", heading_style))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Track your cleaning supplies and know when to restock:", normal_style))
    
    supplies_data = [
        ["Item", "Quantity", "Need to Restock?", "Last Restocked"],
        ["All-purpose cleaner", "", "", ""],
        ["Glass cleaner", "", "", ""],
        ["Bathroom cleaner", "", "", ""],
        ["Floor cleaner", "", "", ""],
        ["Microfiber cloths", "", "", ""],
        ["Sponges", "", "", ""],
        ["Rubber gloves", "", "", ""],
        ["Trash bags", "", "", ""],
        ["Paper towels", "", "", ""],
        ["Dish soap", "", "", ""],
        ["Laundry detergent", "", "", ""]
    ]
    
    supplies_table = Table(supplies_data, colWidths=[60*mm, 30*mm, 40*mm, 40*mm])
    supplies_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['light_accent']),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLORS['dark_text']),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), COLORS['dark_text']),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(supplies_table)
    story.append(PageBreak())
    
    # Page 7: Seasonal Cleaning Checklist
    story.append(Paragraph("Seasonal Cleaning Checklist", heading_style))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Tasks to complete with each season change:", normal_style))
    
    story.append(Paragraph("Spring", subheading_style))
    spring_tasks = [
        "• Deep clean windows",
        "• Wash curtains/blinds",
        "• Clean outdoor furniture",
        "• Organize garage/shed",
        "• Clean gutters",
        "• Wash exterior windows"
    ]
    for task in spring_tasks:
        story.append(Paragraph(task, normal_style))
    
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Fall", subheading_style))
    fall_tasks = [
        "• Clean heating vents",
        "• Check weather stripping",
        "• Store summer items",
        "• Prepare winter supplies",
        "• Clean chimney/fireplace",
        "• Check insulation"
    ]
    for task in fall_tasks:
        story.append(Paragraph(task, normal_style))
    story.append(PageBreak())
    
    # Page 8: Blank Custom Cleaning Template
    story.append(Paragraph("Custom Cleaning Template", heading_style))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Create your own personalized cleaning schedule:", normal_style))
    
    custom_data = [
        ["Task", "Frequency", "Notes", "Completed"],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""]
    ]
    
    custom_table = Table(custom_data, colWidths=[70*mm, 30*mm, 40*mm, 30*mm])
    custom_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['light_accent']),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLORS['dark_text']),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), COLORS['dark_text']),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(custom_table)
    
    # Build PDF
    doc.build(story)
    
    # Add footer to each page
    add_footer(output_path)

def add_footer(pdf_path):
    """Add RecoveriStudio footer to each page of the PDF."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
    
    # Create a temporary file
    temp_path = pdf_path + ".temp"
    
    # Read existing PDF
    from reportlab.pdfgen.canvas import Canvas
    from PyPDF2 import PdfReader, PdfWriter
    import io
    
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    for page_num in range(len(reader.pages)):
        # Get existing page
        page = reader.pages[page_num]
        
        # Create a canvas to draw footer
        packet = io.BytesIO()
        can = Canvas(packet, pagesize=A4)
        
        # Set font and color
        can.setFont("Helvetica", 8)
        can.setFillColor(colors.HexColor('#8B7355'))
        
        # Draw footer text
        footer_text = "RecoveriStudio | www.recoveri.io/studio"
        can.drawString(20*mm, 10*mm, footer_text)
        
        # Save canvas
        can.save()
        
        # Move to beginning of packet
        packet.seek(0)
        
        # Merge footer with existing page
        from PyPDF2 import PdfReader as PdfReader2
        footer_pdf = PdfReader2(packet)
        footer_page = footer_pdf.pages[0]
        
        # Merge
        page.merge_page(footer_page)
        writer.add_page(page)
    
    # Write output
    with open(temp_path, 'wb') as output_file:
        writer.write(output_file)
    
    # Replace original with new version
    import os
    os.replace(temp_path, pdf_path)

if __name__ == "__main__":
    output_file = "product.pdf"
    print(f"Creating Home Cleaning Planner PDF: {output_file}")
    create_pdf(output_file)
    print(f"PDF created successfully: {output_file}")