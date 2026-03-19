#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, PageBreak, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import datetime

def create_baby_milestone_pdf(output_path):
    """Create Baby Milestone Tracker PDF"""
    
    # Create canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Define colors
    bg_color = colors.HexColor('#F5F0EB')  # Soft beige
    text_color = colors.HexColor('#2C2C2C')  # Dark gray
    accent_color = colors.HexColor('#8B7355')  # Warm brown
    light_accent = colors.HexColor('#D4C5B2')  # Light brown
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=accent_color,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=text_color,
        alignment=TA_CENTER,
        spaceAfter=15
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=text_color,
        alignment=TA_LEFT,
        spaceAfter=10
    )
    
    # Page 1: Cover Page
    c.setFillColor(bg_color)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(accent_color)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width/2, height/2 + 40, "Baby Milestone")
    c.drawCentredString(width/2, height/2, "Tracker")
    
    c.setFillColor(text_color)
    c.setFont("Helvetica", 18)
    c.drawCentredString(width/2, height/2 - 60, "First Year Memories")
    
    c.setFillColor(light_accent)
    c.setFont("Helvetica-Oblique", 14)
    c.drawCentredString(width/2, height/2 - 100, "Capture every precious moment")
    
    # Footer
    c.setFillColor(light_accent)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, 20, "RecoveriStudio")
    
    c.showPage()
    
    # Page 2: Instructions
    c.setFillColor(bg_color)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(accent_color)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(40, height - 60, "How to Use This Tracker")
    
    c.setFillColor(text_color)
    c.setFont("Helvetica", 11)
    
    instructions = [
        "1. Print all pages or select the ones you need",
        "2. Use a binder or folder to keep them organised",
        "3. Fill in milestones as they happen throughout the first year",
        "4. Add photos to corresponding pages",
        "5. Create a beautiful keepsake of your baby's first year"
    ]
    
    y_pos = height - 100
    for instruction in instructions:
        c.drawString(50, y_pos, instruction)
        y_pos -= 25
    
    c.setFillColor(accent_color)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y_pos - 40, "Tips:")
    
    c.setFillColor(text_color)
    c.setFont("Helvetica", 11)
    tips = [
        "• Update monthly for consistent tracking",
        "• Use archival-quality pens for longevity",
        "• Store in a dry, cool place",
        "• Make copies for grandparents"
    ]
    
    y_pos -= 70
    for tip in tips:
        c.drawString(60, y_pos, tip)
        y_pos -= 20
    
    # Footer
    c.setFillColor(light_accent)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, 20, "RecoveriStudio")
    
    c.showPage()
    
    # Monthly tracker pages (12 months)
    months = [
        "Month 1: Welcome to the World",
        "Month 2: First Smiles",
        "Month 3: Discovering Hands",
        "Month 4: Rolling Over",
        "Month 5: Sitting Up",
        "Month 6: First Foods",
        "Month 7: Crawling Adventures",
        "Month 8: Pulling Up",
        "Month 9: Babbling & Sounds",
        "Month 10: Standing Tall",
        "Month 11: Cruising Along",
        "Month 12: First Steps"
    ]
    
    for i, month in enumerate(months, 1):
        # Background
        c.setFillColor(bg_color)
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        # Month header
        c.setFillColor(accent_color)
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(width/2, height - 60, f"Month {i}")
        
        c.setFillColor(text_color)
        c.setFont("Helvetica", 16)
        c.drawCentredString(width/2, height - 90, month.split(": ")[1])
        
        # Milestone sections
        c.setFillColor(light_accent)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 140, "Milestones Achieved:")
        
        c.setFillColor(text_color)
        c.setFont("Helvetica", 11)
        
        # Create lines for writing milestones
        y_pos = height - 170
        for line in range(8):
            c.line(50, y_pos, width - 50, y_pos)
            y_pos -= 25
        
        # Development notes
        c.setFillColor(light_accent)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_pos - 20, "Development Notes:")
        
        y_pos -= 50
        for line in range(6):
            c.line(50, y_pos, width - 50, y_pos)
            y_pos -= 25
        
        # Measurements
        c.setFillColor(light_accent)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_pos - 20, "Measurements:")
        
        c.setFillColor(text_color)
        c.setFont("Helvetica", 11)
        c.drawString(60, y_pos - 45, "Weight: ________________ kg")
        c.drawString(60, y_pos - 65, "Height: ________________ cm")
        
        # Favorite things
        c.drawString(60, y_pos - 95, "Favorite toy: ________________")
        c.drawString(60, y_pos - 115, "Favorite food: ________________")
        
        # Footer
        c.setFillColor(light_accent)
        c.setFont("Helvetica", 8)
        c.drawCentredString(width/2, 20, "RecoveriStudio")
        
        c.showPage()
    
    # Special milestone cards page
    c.setFillColor(bg_color)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(accent_color)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 60, "Special Firsts")
    
    specials = [
        ("First Smile", "Date: ___________", "Time: ___________", "Notes: ________________"),
        ("First Laugh", "Date: ___________", "Time: ___________", "Notes: ________________"),
        ("First Tooth", "Date: ___________", "Which tooth: ___________"),
        ("First Steps", "Date: ___________", "Number of steps: ___________"),
        ("First Word", "Date: ___________", "Word: ___________"),
        ("First Solid Food", "Date: ___________", "Food: ___________")
    ]
    
    y_pos = height - 120
    for title, *details in specials:
        c.setFillColor(light_accent)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y_pos, title)
        
        c.setFillColor(text_color)
        c.setFont("Helvetica", 11)
        for i, detail in enumerate(details):
            c.drawString(70, y_pos - 20 - (i * 20), detail)
        
        y_pos -= 80
        if y_pos < 100:
            c.showPage()
            c.setFillColor(bg_color)
            c.rect(0, 0, width, height, fill=1, stroke=0)
            y_pos = height - 60
    
    # Footer
    c.setFillColor(light_accent)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, 20, "RecoveriStudio")
    
    c.showPage()
    
    # Growth chart page
    c.setFillColor(bg_color)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(accent_color)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 60, "Growth Chart")
    
    # Create simple growth chart
    c.setFillColor(text_color)
    c.setFont("Helvetica", 11)
    
    # Y-axis (weight)
    c.drawString(80, height - 120, "Weight (kg)")
    for i in range(12):
        y = height - 150 - (i * 30)
        c.line(100, y, width - 100, y)
        c.drawString(70, y - 5, f"{3 + i*0.5}")
    
    # X-axis (months)
    c.drawString(width/2, 80, "Months")
    for i in range(12):
        x = 120 + (i * 40)
        c.line(x, height - 150, x, height - 150 - 330)
        c.drawCentredString(x, height - 170, f"{i+1}")
    
    # Footer
    c.setFillColor(light_accent)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, 20, "RecoveriStudio")
    
    c.showPage()
    
    # Final page: Memory keeper
    c.setFillColor(bg_color)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(accent_color)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 60, "Special Memories")
    
    c.setFillColor(text_color)
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 100, "Use this space to write down special moments, funny stories,")
    c.drawString(50, height - 120, "or anything you want to remember about this amazing first year.")
    
    # Writing area
    y_pos = height - 160
    for line in range(20):
        c.line(50, y_pos, width - 50, y_pos)
        y_pos -= 25
    
    # Footer
    c.setFillColor(light_accent)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, 20, "RecoveriStudio")
    
    # Save PDF
    c.save()
    print(f"PDF created successfully: {output_path}")

if __name__ == "__main__":
    output_path = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/baby-milestone-tracker/product.pdf"
    create_baby_milestone_pdf(output_path)