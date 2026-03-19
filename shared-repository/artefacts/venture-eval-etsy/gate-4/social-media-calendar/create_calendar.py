#!/usr/bin/env python3
"""
Create Social Media Content Calendar PDF
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import Color, black, white, grey
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import datetime

# Custom colors from brand palette
COLOR_BG = Color(245/255, 240/255, 235/255, alpha=1)  # #F5F0EB
COLOR_TEXT = Color(44/255, 44/255, 44/255, alpha=1)   # #2C2C2C
COLOR_ACCENT = Color(139/255, 115/255, 85/255, alpha=1)  # #8B7355
COLOR_LIGHT = Color(212/255, 197/255, 178/255, alpha=1)  # #D4C5B2

def create_calendar_pdf(output_path):
    """Create the Social Media Content Calendar PDF"""
    
    # Create canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Create styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=COLOR_TEXT,
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=COLOR_ACCENT,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=COLOR_TEXT,
        alignment=TA_LEFT,
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLOR_TEXT,
        alignment=TA_LEFT,
        spaceAfter=6
    )
    
    # Page 1: Cover Page
    c.setFillColor(COLOR_BG)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width/2, height/2 + 40, "Social Media")
    c.drawCentredString(width/2, height/2, "Content Calendar")
    
    c.setFillColor(COLOR_ACCENT)
    c.setFont("Helvetica", 18)
    c.drawCentredString(width/2, height/2 - 40, "Plan. Schedule. Grow.")
    
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height/2 - 80, "2025 Edition")
    
    # Footer
    c.setFillColor(COLOR_ACCENT)
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width/2, 30, "RecoveriStudio | studio@recoveri.io")
    
    c.showPage()
    
    # Page 2: Introduction
    c.setFillColor(white)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Title
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, height - 60, "Welcome to Your Social Media")
    c.drawString(40, height - 85, "Content Calendar")
    
    # Introduction text
    intro_text = """
    <b>Congratulations on taking control of your social media strategy!</b><br/><br/>
    
    This content calendar is designed to help you plan, organize, and track all your social media activities in one place. Whether you're managing multiple platforms or just starting out, this planner will help you stay consistent and strategic.<br/><br/>
    
    <b>How to Use This Calendar:</b><br/>
    1. Start with the yearly overview to plan major campaigns and themes<br/>
    2. Use monthly pages to schedule content by platform<br/>
    3. Track performance and adjust your strategy<br/>
    4. Repurpose successful content using the content bank<br/><br/>
    
    <b>Tips for Success:</b><br/>
    • Batch create content to save time<br/>
    • Schedule posts in advance using your preferred tool<br/>
    • Review analytics monthly to identify what works<br/>
    • Engage with your audience daily<br/>
    • Stay authentic to your brand voice
    """
    
    intro = Paragraph(intro_text, body_style)
    intro.wrapOn(c, width - 80, height)
    intro.drawOn(c, 40, height - 200)
    
    # Footer
    c.setFillColor(COLOR_ACCENT)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 30, "RecoveriStudio")
    
    c.showPage()
    
    # Page 3: Yearly Overview
    c.setFillColor(white)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Title
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 50, "2025 Content Planning Overview")
    
    # Create monthly grid
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    cell_width = (width - 100) / 4
    cell_height = 40
    
    start_x = 50
    start_y = height - 100
    
    for i, month in enumerate(months):
        row = i // 4
        col = i % 4
        
        x = start_x + col * cell_width
        y = start_y - row * cell_height
        
        # Draw month box
        c.setStrokeColor(COLOR_LIGHT)
        c.setFillColor(white)
        c.rect(x, y - cell_height, cell_width, cell_height, fill=1, stroke=1)
        
        # Month name
        c.setFillColor(COLOR_TEXT)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 10, y - 25, month)
        
        # Lines for notes
        c.setStrokeColor(Color(0.9, 0.9, 0.9))
        for line in range(3):
            c.line(x + 10, y - 35 - line*5, x + cell_width - 10, y - 35 - line*5)
    
    # Key dates section
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, start_y - 200, "Key Dates & Campaigns")
    
    key_dates = [
        "Q1 Launch (Jan-Mar)",
        "Spring Campaign (Apr-Jun)", 
        "Summer Promo (Jul-Aug)",
        "Back to School (Sep)",
        "Holiday Prep (Oct-Nov)",
        "Year-End Review (Dec)"
    ]
    
    for i, date in enumerate(key_dates):
        y_pos = start_y - 220 - i*20
        c.setFillColor(COLOR_TEXT)
        c.setFont("Helvetica", 10)
        c.drawString(70, y_pos, "• " + date)
    
    # Footer
    c.setFillColor(COLOR_ACCENT)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 30, "RecoveriStudio")
    
    c.showPage()
    
    # Create 12 monthly pages
    for month_num in range(1, 13):
        # Start new page
        c.setFillColor(white)
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        # Month header
        month_name = datetime.date(2025, month_num, 1).strftime('%B %Y')
        c.setFillColor(COLOR_ACCENT)
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(width/2, height - 50, month_name)
        
        # Platform sections
        platforms = ["Instagram", "Facebook", "TikTok", "Pinterest", "Twitter/X", "LinkedIn"]
        section_height = (height - 100) / 3
        
        for i, platform in enumerate(platforms[:3]):  # First 3 on left
            y_start = height - 100 - i * section_height
            
            # Platform header
            c.setFillColor(COLOR_TEXT)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, y_start - 20, platform)
            
            # Content grid
            c.setStrokeColor(COLOR_LIGHT)
            for week in range(4):
                y = y_start - 40 - week * 20
                c.line(40, y, width/2 - 20, y)
            
            c.line(40, y_start - 40, 40, y_start - 120)
            c.line(width/2 - 20, y_start - 40, width/2 - 20, y_start - 120)
            
            # Week labels
            weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
            for w, week in enumerate(weeks):
                y = y_start - 35 - w * 20
                c.setFillColor(COLOR_TEXT)
                c.setFont("Helvetica", 8)
                c.drawString(45, y, week)
        
        for i, platform in enumerate(platforms[3:]):  # Last 3 on right
            y_start = height - 100 - i * section_height
            
            # Platform header
            c.setFillColor(COLOR_TEXT)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(width/2 + 20, y_start - 20, platform)
            
            # Content grid
            c.setStrokeColor(COLOR_LIGHT)
            for week in range(4):
                y = y_start - 40 - week * 20
                c.line(width/2 + 20, y, width - 40, y)
            
            c.line(width/2 + 20, y_start - 40, width/2 + 20, y_start - 120)
            c.line(width - 40, y_start - 40, width - 40, y_start - 120)
            
            # Week labels
            weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
            for w, week in enumerate(weeks):
                y = y_start - 35 - w * 20
                c.setFillColor(COLOR_TEXT)
                c.setFont("Helvetica", 8)
                c.drawString(width/2 + 25, y, week)
        
        # Notes section
        c.setFillColor(COLOR_TEXT)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, 150, "Monthly Notes & Goals")
        
        c.setStrokeColor(COLOR_LIGHT)
        for line in range(8):
            y = 130 - line * 15
            c.line(40, y, width - 40, y)
        
        # Footer
        c.setFillColor(COLOR_ACCENT)
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(width/2, 30, f"RecoveriStudio | {month_name}")
        
        c.showPage()
    
    # Final page: Content Bank
    c.setFillColor(white)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Title
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height - 50, "Content Bank")
    
    # Instructions
    instructions = """
    <b>Your Content Repurposing Hub</b><br/><br/>
    
    Use this section to store successful content ideas that can be repurposed across platforms. When you create content that performs well, add it here for future use.<br/><br/>
    
    <b>Content Bank Categories:</b><br/>
    • Educational Posts<br/>
    • Promotional Content<br/>
    • Engagement Questions<br/>
    • Story Ideas<br/>
    • Reels/TikTok Concepts<br/>
    • Carousel Topics<br/>
    • Blog Post Ideas<br/>
    • Newsletter Content
    """
    
    instr = Paragraph(instructions, body_style)
    instr.wrapOn(c, width - 80, height)
    instr.drawOn(c, 40, height - 150)
    
    # Content bank table
    data = [
        ["Category", "Idea", "Platforms", "Date Used"],
        ["Educational", "How-to guide for beginners", "IG, FB, Blog", ""],
        ["Promotional", "Limited time offer announcement", "All", ""],
        ["Engagement", "Poll: Favorite feature?", "IG Stories, Twitter", ""],
        ["Story", "Behind-the-scenes day", "IG Stories", ""],
        ["Reels", "Quick tip in 15 seconds", "IG, TikTok", ""],
        ["Carousel", "5 benefits of our product", "IG, LinkedIn", ""],
        ["Blog", "Industry trends analysis", "Blog, LinkedIn", ""],
        ["Newsletter", "Monthly roundup", "Email", ""]
    ]
    
    table = Table(data, colWidths=[80, 180, 80, 60])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_LIGHT),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_TEXT),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), white),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_LIGHT),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    table.wrapOn(c, width, height)
    table.drawOn(c, 40, height - 350)
    
    # Footer
    c.setFillColor(COLOR_ACCENT)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 30, "RecoveriStudio | Content Bank")
    
    c.showPage()
    
    # Save PDF
    c.save()
    print(f"PDF created successfully: {output_path}")

if __name__ == "__main__":
    output_path = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/social-media-calendar/product.pdf"
    create_calendar_pdf(output_path)