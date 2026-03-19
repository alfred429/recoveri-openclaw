#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, PageBreak, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

# Colors from the skill: #F5F0EB, #2C2C2C, #8B7355, #D4C5B2
COLORS = {
    'background': colors.HexColor('#F5F0EB'),
    'text_dark': colors.HexColor('#2C2C2C'),
    'accent': colors.HexColor('#8B7355'),
    'light_accent': colors.HexColor('#D4C5B2')
}

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple for reportlab"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))

def create_goal_setting_pdf(output_path):
    """Create the Goal Setting Worksheet PDF"""
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Create styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=COLORS['text_dark'],
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=COLORS['accent'],
        spaceAfter=12,
        alignment=TA_LEFT
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=COLORS['accent'],
        spaceAfter=8,
        alignment=TA_LEFT
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=COLORS['text_dark'],
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    # Page 1: Cover Page
    c.setFillColor(COLORS['background'])
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(COLORS['accent'])
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width/2, height/2 + 40, "Goal Setting")
    c.drawCentredString(width/2, height/2 - 10, "Worksheet")
    
    c.setFillColor(COLORS['text_dark'])
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, height/2 - 60, "Turn Your Dreams Into Reality")
    
    c.setFillColor(COLORS['light_accent'])
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(width/2, 100, "RecoveriStudio | Personal Development Planner")
    
    # Add footer to first page
    c.setFillColor(COLORS['text_dark'])
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, 20, "© RecoveriStudio - For Personal Use Only")
    
    c.showPage()
    
    # Page 2: Introduction & How to Use
    c.setFillColor(COLORS['background'])
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(COLORS['accent'])
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, height - 60, "Welcome to Your Goal Journey")
    
    c.setFillColor(COLORS['text_dark'])
    c.setFont("Helvetica", 11)
    
    intro_text = """This Goal Setting Worksheet is designed to help you clarify your vision, set meaningful goals, and create actionable plans. Follow these steps:

1. <b>Vision Board</b> (Page 3): Visualize your ideal future
2. <b>Annual Goals</b> (Page 4): Set your big-picture objectives
3. <b>Quarterly Breakdown</b> (Page 5): Divide annual goals into quarters
4. <b>Monthly Planning</b> (Pages 6-7): Plan monthly actions and track habits
5. <b>Weekly Action</b> (Page 8): Break down monthly goals into weekly tasks
6. <b>Daily Reflection</b> (Page 9): Track daily progress and reflections
7. <b>SMART Goals</b> (Page 10): Apply the SMART framework
8. <b>Obstacle Planning</b> (Page 11): Identify and plan for challenges
9. <b>Progress Review</b> (Page 12): Celebrate wins and adjust plans

<b>Tip:</b> Be specific, be realistic, and review your progress regularly."""
    
    # Draw introduction text
    text_object = c.beginText(40, height - 100)
    text_object.setFont("Helvetica", 11)
    text_object.setFillColor(COLORS['text_dark'])
    
    # Simple text drawing (no HTML parsing in basic canvas)
    lines = intro_text.split('\n')
    for line in lines:
        if "<b>" in line and "</b>" in line:
            # Simple bold handling
            parts = line.split("<b>")
            for part in parts:
                if "</b>" in part:
                    bold_part, rest = part.split("</b>", 1)
                    text_object.setFont("Helvetica-Bold", 11)
                    text_object.textOut(bold_part)
                    text_object.setFont("Helvetica", 11)
                    if rest:
                        text_object.textOut(rest)
                else:
                    text_object.textOut(part)
        else:
            text_object.textOut(line)
        text_object.moveCursor(0, 15)
    
    c.drawText(text_object)
    
    # Add footer
    c.setFillColor(COLORS['text_dark'])
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, 20, "© RecoveriStudio - Page 2 of 12")
    
    c.showPage()
    
    # Pages 3-12: Worksheet Pages
    for page_num in range(3, 13):
        # Set background
        c.setFillColor(COLORS['background'])
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        # Page title based on page number
        page_titles = {
            3: "Vision Board - Your Ideal Future",
            4: "Annual Goals Overview",
            5: "Quarterly Breakdown",
            6: "Monthly Planning - Habit Tracking",
            7: "Monthly Planning - Action Items",
            8: "Weekly Action Plan",
            9: "Daily Reflection & Progress",
            10: "SMART Goals Framework",
            11: "Obstacle Identification & Solutions",
            12: "Progress Review & Celebration"
        }
        
        title = page_titles.get(page_num, f"Page {page_num}")
        
        # Draw title
        c.setFillColor(COLORS['accent'])
        c.setFont("Helvetica-Bold", 18)
        c.drawString(40, height - 60, title)
        
        # Draw page content area
        c.setStrokeColor(COLORS['light_accent'])
        c.setLineWidth(0.5)
        c.rect(30, 30, width - 60, height - 120, stroke=1, fill=0)
        
        # Add grid or lines for writing (simplified)
        if page_num in [3, 4, 5, 6, 7, 8, 9]:
            # Add writing lines
            c.setStrokeColor(COLORS['light_accent'])
            c.setLineWidth(0.3)
            y_pos = height - 100
            for i in range(15):
                c.line(40, y_pos, width - 40, y_pos)
                y_pos -= 25
        
        # Add section labels for specific pages
        if page_num == 10:  # SMART Goals
            sections = ["Specific:", "Measurable:", "Achievable:", "Relevant:", "Time-bound:"]
            y_pos = height - 100
            for section in sections:
                c.setFillColor(COLORS['accent'])
                c.setFont("Helvetica-Bold", 12)
                c.drawString(40, y_pos, section)
                y_pos -= 60
        
        if page_num == 11:  # Obstacle Planning
            sections = ["Obstacle:", "Potential Impact:", "Solution:", "Prevention Plan:"]
            y_pos = height - 100
            for section in sections:
                c.setFillColor(COLORS['accent'])
                c.setFont("Helvetica-Bold", 12)
                c.drawString(40, y_pos, section)
                y_pos -= 50
        
        if page_num == 12:  # Progress Review
            sections = ["Wins to Celebrate:", "Lessons Learned:", "Adjustments Needed:", "Next Steps:"]
            y_pos = height - 100
            for section in sections:
                c.setFillColor(COLORS['accent'])
                c.setFont("Helvetica-Bold", 12)
                c.drawString(40, y_pos, section)
                y_pos -= 50
        
        # Add footer with page number
        c.setFillColor(COLORS['text_dark'])
        c.setFont("Helvetica", 8)
        c.drawCentredString(width/2, 20, f"© RecoveriStudio - Page {page_num} of 12")
        
        if page_num < 12:
            c.showPage()
    
    # Save the PDF
    c.save()
    print(f"PDF created successfully: {output_path}")

if __name__ == "__main__":
    output_dir = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/goal-setting-worksheet"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "product.pdf")
    create_goal_setting_pdf(output_path)