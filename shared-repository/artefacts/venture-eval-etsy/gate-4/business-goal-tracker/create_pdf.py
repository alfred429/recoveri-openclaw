#!/usr/bin/env python3
"""
Business Goal Tracker PDF Generator
Creates an 8-page professional business goal tracking PDF
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import datetime

# Color palette from RecoveriStudio brand guidelines
COLORS = {
    'background': colors.HexColor('#F5F0EB'),  # Soft beige
    'dark': colors.HexColor('#2C2C2C'),        # Dark charcoal
    'accent': colors.HexColor('#8B7355'),      # Warm brown
    'light': colors.HexColor('#D4C5B2'),       # Light tan
    'highlight': colors.HexColor('#4A6FA5'),   # Professional blue
}

def create_business_goal_tracker(output_path):
    """Create the Business Goal Tracker PDF"""
    
    # Create canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Set up styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=COLORS['dark'],
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=COLORS['accent'],
        spaceAfter=12
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=COLORS['highlight'],
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=COLORS['dark'],
        spaceAfter=6
    )
    
    # Page 1: Cover Page
    c.setFillColor(COLORS['background'])
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(COLORS['dark'])
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width/2, height/2 + 40, "Business")
    c.drawCentredString(width/2, height/2, "Goal Tracker")
    
    c.setFont("Helvetica", 18)
    c.drawCentredString(width/2, height/2 - 40, "Strategic Planning & Progress Tracking")
    
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height/2 - 80, "Professional Template for Entrepreneurs & Business Leaders")
    
    # Footer
    c.setFont("Helvetica", 9)
    c.drawCentredString(width/2, 30, "© RecoveriStudio | studio@recoveri.io")
    c.drawCentredString(width/2, 20, "Instant Digital Download")
    
    c.showPage()
    
    # Page 2: Annual Business Vision
    c.setFillColor(COLORS['background'])
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(COLORS['dark'])
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, height - 60, "Annual Business Vision")
    
    c.setFont("Helvetica", 11)
    c.drawString(40, height - 85, "Year: ___________")
    
    # Vision statement area
    c.setStrokeColor(COLORS['light'])
    c.setLineWidth(0.5)
    c.rect(40, height - 380, width - 80, 280, stroke=1, fill=0)
    
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(COLORS['accent'])
    c.drawString(45, height - 110, "Describe your business vision for the year. What do you want to achieve?")
    
    # Key focus areas
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(COLORS['highlight'])
    c.drawString(40, height - 400, "Key Focus Areas:")
    
    focus_areas = [
        "1. Revenue & Profitability",
        "2. Customer Growth & Retention",
        "3. Product/Service Development",
        "4. Team & Operations",
        "5. Marketing & Brand Awareness",
        "6. Personal Development"
    ]
    
    c.setFont("Helvetica", 11)
    c.setFillColor(COLORS['dark'])
    y_pos = height - 425
    for area in focus_areas:
        c.drawString(50, y_pos, area)
        y_pos -= 25
    
    # Footer
    c.setFont("Helvetica", 8)
    c.setFillColor(COLORS['accent'])
    c.drawCentredString(width/2, 30, "RecoveriStudio Business Goal Tracker | Page 2 of 8")
    
    c.showPage()
    
    # Page 3: Quarterly Goal Breakdown - Q1 & Q2
    c.setFillColor(COLORS['background'])
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(COLORS['dark'])
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 60, "Quarterly Goal Breakdown")
    
    # Q1 Section
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(COLORS['accent'])
    c.drawString(40, height - 100, "Quarter 1: January - March")
    
    c.setStrokeColor(COLORS['light'])
    c.setLineWidth(0.5)
    c.rect(40, height - 280, (width - 100)/2, 170, stroke=1, fill=0)
    
    # Q1 table headers
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(COLORS['dark'])
    c.drawString(45, height - 120, "Goal")
    c.drawString(45, height - 135, "Actions")
    c.drawString(45, height - 150, "Resources")
    c.drawString(45, height - 165, "Success Metrics")
    
    # Q2 Section
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(COLORS['accent'])
    c.drawString(width/2 + 20, height - 100, "Quarter 2: April - June")
    
    c.rect(width/2 + 20, height - 280, (width - 100)/2, 170, stroke=1, fill=0)
    
    # Q2 table headers
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(COLORS['dark'])
    c.drawString(width/2 + 25, height - 120, "Goal")
    c.drawString(width/2 + 25, height - 135, "Actions")
    c.drawString(width/2 + 25, height - 150, "Resources")
    c.drawString(width/2 + 25, height - 165, "Success Metrics")
    
    # Footer
    c.setFont("Helvetica", 8)
    c.setFillColor(COLORS['accent'])
    c.drawCentredString(width/2, 30, "RecoveriStudio Business Goal Tracker | Page 3 of 8")
    
    c.showPage()
    
    # Page 4: Quarterly Goal Breakdown - Q3 & Q4
    c.setFillColor(COLORS['background'])
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(COLORS['dark'])
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 60, "Quarterly Goal Breakdown")
    
    # Q3 Section
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(COLORS['accent'])
    c.drawString(40, height - 100, "Quarter 3: July - September")
    
    c.setStrokeColor(COLORS['light'])
    c.setLineWidth(0.5)
    c.rect(40, height - 280, (width - 100)/2, 170, stroke=1, fill=0)
    
    # Q3 table headers
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(COLORS['dark'])
    c.drawString(45, height - 120, "Goal")
    c.drawString(45, height - 135, "Actions")
    c.drawString(45, height - 150, "Resources")
    c.drawString(45, height - 165, "Success Metrics")
    
    # Q4 Section
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(COLORS['accent'])
    c.drawString(width/2 + 20, height - 100, "Quarter 4: October - December")
    
    c.rect(width/2 + 20, height - 280, (width - 100)/2, 170, stroke=1, fill=0)
    
    # Q4 table headers
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(COLORS['dark'])
    c.drawString(width/2 + 25, height - 120, "Goal")
    c.drawString(width/2 + 25, height - 135, "Actions")
    c.drawString(width/2 + 25, height - 150, "Resources")
    c.drawString(width/2 + 25, height - 165, "Success Metrics")
    
    # Notes section at bottom
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(COLORS['highlight'])
    c.drawString(40, 150, "Quarterly Review Notes:")
    
    c.setStrokeColor(COLORS['light'])
    c.rect(40, 80, width - 80, 60, stroke=1, fill=0)
    
    # Footer
    c.setFont("Helvetica", 8)
    c.setFillColor(COLORS['accent'])
    c.drawCentredString(width/2, 30, "RecoveriStudio Business Goal Tracker | Page 4 of 8")
    
    c.showPage()
    
    # Page 5: Monthly Action Planning (Months 1-6)
    c.setFillColor(COLORS['background'])
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(COLORS['dark'])
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 60, "Monthly Action Planning")
    
    months = ["January", "February", "March", "April", "May", "June"]
    
    y_start = height - 100
    for i, month in enumerate(months):
        row_y = y_start - (i * 70)
        
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(COLORS['accent'])
        c.drawString(40, row_y, month)
        
        c.setStrokeColor(COLORS['light'])
        c.rect(40, row_y - 50, width - 80, 40, stroke=1, fill=0)
        
        c.setFont("Helvetica", 9)
        c.setFillColor(COLORS['dark'])
        c.drawString(45, row_y - 35, "Key Actions:")
        c.drawString(45, row_y - 50, "Success Metrics:")
    
    # Footer
    c.setFont("Helvetica", 8)
    c.setFillColor(COLORS['accent'])
    c.drawCentredString(width/2, 30, "RecoveriStudio Business Goal Tracker | Page 5 of 8")
    
    c.showPage()
    
    # Page 6: Monthly Action Planning (Months 7-12)
    c.setFillColor(COLORS['background'])
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(COLORS['dark'])
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 60, "Monthly Action Planning")
    
    months = ["July", "August", "September", "October", "November", "December"]
    
    y_start = height - 100
    for i, month in enumerate(months):
        row_y = y_start - (i * 70)
        
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(COLORS['accent'])
        c.drawString(40, row_y, month)
        
        c.setStrokeColor(COLORS['light'])
        c.rect(40, row_y - 50, width - 80, 40, stroke=1, fill=0)
        
        c.setFont("Helvetica", 9)
        c.setFillColor(COLORS['dark'])
        c.drawString(45, row_y - 35, "Key Actions:")
        c.drawString(45, row_y - 50, "Success Metrics:")
    
    # Footer
    c.setFont("Helvetica", 8)
    c.setFillColor(COLORS['accent'])
    c.drawCentredString(width/2, 30, "RecoveriStudio Business Goal Tracker | Page 6 of 8")
    
    c.showPage()
    
    # Page 7: KPI Tracker & Resource Allocation
    c.setFillColor(COLORS['background'])
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Left column: KPI Tracker
    c.setFillColor(COLORS['dark'])
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, height - 80, "KPI Tracker")
    
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 100, "Track key metrics monthly:")
    
    kpi_headers = ["KPI", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Draw KPI table grid
    c.setStrokeColor(COLORS['light'])
    c.setLineWidth(0.3)
    
    # Horizontal lines
    for i in range(8):
        y = height - 120 - (i * 25)
        c.line(40, y, width/2 - 20, y)
    
    # Vertical lines
    for i in range(14):
        x = 40 + (i * 30)
        if x < width/2 - 20:
            c.line(x, height - 120, x, height - 120 - (7 * 25))
    
    # Header labels
    c.setFont("Helvetica-Bold", 8)
    for i, header in enumerate(kpi_headers):
        x = 40 + (i * 30) + 2
        c.drawString(x, height - 115, header[:8])  # Truncate if too long
    
    # Right column: Resource Allocation
    c.setFont("Helvetica-Bold", 18)
    c.drawString(width/2 + 20, height - 80, "Resource Allocation")
    
    resources = [
        "Budget Planning",
        "Team Hours",
        "Marketing Spend",
        "Software/Tools",
        "Training & Development",
        "Contingency Fund"
    ]
    
    c.setFont("Helvetica", 11)
    y_pos = height - 110
    for resource in resources:
        c.drawString(width/2 + 25, y_pos, f"• {resource}")
        c.setStrokeColor(COLORS['light'])
        c.rect(width/2 + 25, y_pos - 15, 150, 12, stroke=1, fill=0)
        y_pos -= 30
    
    # Footer
    c.setFont("Helvetica", 8)
    c.setFillColor(COLORS['accent'])
    c.drawCentredString(width/2, 30, "RecoveriStudio Business Goal Tracker | Page 7 of 8")
    
    c.showPage()
    
    # Page 8: Progress Review & Team Accountability
    c.setFillColor(COLORS['background'])
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(COLORS['dark'])
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 60, "Progress Review & Team Accountability")
    
    # Progress Review section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(COLORS['accent'])
    c.drawString(40, height - 100, "Quarterly Progress Review")
    
    questions = [
        "1. What were our biggest achievements this quarter?",
        "2. What challenges did we face and how did we overcome them?",
        "3. What lessons did we learn?",
        "4. What adjustments should we make for next quarter?",
        "5. Are we on track to achieve our annual goals?"
    ]
    
    c.setFont("Helvetica", 11)
    c.setFillColor(COLORS['dark'])
    y_pos = height - 130
    for question in questions:
        c.drawString(45, y_pos, question)
        c.setStrokeColor(COLORS['light'])
        c.rect(45, y_pos - 20, width - 90, 15, stroke=1, fill=0)
        y_pos -= 40
    
    # Team Accountability section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(COLORS['highlight'])
    c.drawString(40, 200, "Team Accountability Checklist")
    
    checklist_items = [
        "□ Goals communicated clearly to team",
        "□ Resources allocated appropriately",
        "□ Regular check-ins scheduled",
        "□ Success metrics defined and tracked",
        "□ Feedback mechanisms in place",
        "□ Celebrations planned for milestones"
    ]
    
    c.setFont("Helvetica", 11)
    c.setFillColor(COLORS['dark'])
    y_pos = 180
    for item in checklist_items:
        c.drawString(45, y_pos, item)
        y_pos -= 20
    
    # Final footer with usage instructions
    c.setFont("Helvetica", 8)
    c.setFillColor(COLORS['accent'])
    c.drawCentredString(width/2, 50, "RecoveriStudio Business Goal Tracker | Page 8 of 8")
    
    c.setFont("Helvetica", 7)
    c.drawCentredString(width/2, 40, "Print and use throughout the year. Update quarterly. Keep in your business planner.")
    c.drawCentredString(width/2, 30, "© RecoveriStudio. For personal or commercial use. Not for resale.")
    
    c.save()
    print(f"PDF created successfully: {output_path}")

if __name__ == "__main__":
    output_file = "business_goal_tracker.pdf"
    create_business_goal_tracker(output_file)