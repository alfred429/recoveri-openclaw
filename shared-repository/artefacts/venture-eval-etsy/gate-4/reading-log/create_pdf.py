#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, PageBreak, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import datetime

def create_reading_log_pdf(output_path):
    """Create a 25-page Reading Log Book PDF"""
    
    # Create canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Define colors from RecoveriStudio palette
    primary_color = colors.HexColor('#2C2C2C')  # Dark gray
    accent_color = colors.HexColor('#8B7355')   # Brown
    light_bg = colors.HexColor('#F5F0EB')       # Light beige
    secondary_color = colors.HexColor('#D4C5B2') # Light brown
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=primary_color,
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=accent_color,
        spaceAfter=15,
        alignment=TA_LEFT
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=primary_color,
        spaceAfter=10,
        alignment=TA_LEFT
    )
    
    # Function to add footer to every page
    def add_footer(canvas_obj, page_num):
        canvas_obj.saveState()
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(colors.gray)
        canvas_obj.drawString(20*mm, 10*mm, f"RecoveriStudio • Page {page_num}")
        canvas_obj.drawRightString(width - 20*mm, 10*mm, "© 2025 Recoveri Ltd")
        canvas_obj.restoreState()
    
    # Page 1: Cover Page
    c.setFillColor(light_bg)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(primary_color)
    c.setFont('Helvetica-Bold', 36)
    c.drawCentredString(width/2, height/2 + 40, "Reading Log Book")
    
    c.setFont('Helvetica', 18)
    c.setFillColor(accent_color)
    c.drawCentredString(width/2, height/2 - 20, "Track Your Literary Journey")
    
    c.setFont('Helvetica', 12)
    c.setFillColor(colors.gray)
    c.drawCentredString(width/2, height/2 - 60, "Digital Printable PDF")
    
    # Add decorative line
    c.setStrokeColor(accent_color)
    c.setLineWidth(1)
    c.line(width/2 - 100, height/2 - 80, width/2 + 100, height/2 - 80)
    
    c.setFont('Helvetica', 10)
    c.drawCentredString(width/2, 50, "RecoveriStudio | Digital Planners & Journals")
    
    add_footer(c, 1)
    c.showPage()
    
    # Page 2: Introduction
    c.setFillColor(colors.white)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(primary_color)
    c.setFont('Helvetica-Bold', 20)
    c.drawString(30*mm, height - 40*mm, "Welcome to Your Reading Journey")
    
    c.setFont('Helvetica', 11)
    intro_text = """
    This Reading Log Book is designed to help you track, reflect on, and celebrate your reading adventures. 
    Whether you're an avid reader, a student, or just beginning your reading journey, this log will help 
    you document every book you read.
    
    <b>How to Use This Journal:</b>
    1. Print all pages or select the ones you need
    2. Place in a binder or have it professionally bound
    3. Use pens, pencils, or markers to fill in your entries
    4. Refer back to track your progress and memories
    
    <b>Tips for Success:</b>
    • Set realistic reading goals
    • Update your log regularly
    • Be honest in your reviews
    • Celebrate your reading milestones
    """
    
    frame = Frame(30*mm, 30*mm, width - 60*mm, height - 100*mm, showBoundary=0)
    story = []
    story.append(Paragraph(intro_text, body_style))
    frame.addFromList(story, c)
    
    add_footer(c, 2)
    c.showPage()
    
    # Page 3: Yearly Reading Goals
    c.setFillColor(colors.white)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(primary_color)
    c.setFont('Helvetica-Bold', 20)
    c.drawString(30*mm, height - 40*mm, f"{datetime.datetime.now().year} Reading Goals")
    
    # Goals section
    c.setFont('Helvetica-Bold', 14)
    c.setFillColor(accent_color)
    c.drawString(30*mm, height - 60*mm, "My Reading Goals for This Year:")
    
    c.setFont('Helvetica', 11)
    c.setFillColor(primary_color)
    goals_y = height - 75*mm
    goals = [
        "Total books to read: _____",
        "Genres to explore: _____",
        "Longest book to tackle: _____",
        "Reading challenge to join: _____",
        "New authors to try: _____"
    ]
    
    for i, goal in enumerate(goals):
        c.drawString(40*mm, goals_y - i*15*mm, f"{i+1}. {goal}")
    
    # Reading statistics section
    c.setFont('Helvetica-Bold', 14)
    c.setFillColor(accent_color)
    c.drawString(30*mm, height - 160*mm, "Year-End Reading Statistics:")
    
    stats = [
        "Total books read: _____",
        "Average rating: _____",
        "Most-read genre: _____",
        "Longest book: _____",
        "Shortest book: _____",
        "Favorite book: _____"
    ]
    
    c.setFont('Helvetica', 11)
    c.setFillColor(primary_color)
    stats_y = height - 175*mm
    for i, stat in enumerate(stats):
        c.drawString(40*mm, stats_y - i*15*mm, f"• {stat}")
    
    add_footer(c, 3)
    c.showPage()
    
    # Pages 4-13: Monthly Reading Trackers (10 pages)
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    
    for month_idx in range(10):  # Create 10 monthly trackers
        month = months[month_idx % 12]
        c.setFillColor(colors.white)
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        # Month header
        c.setFillColor(accent_color)
        c.setFont('Helvetica-Bold', 24)
        c.drawCentredString(width/2, height - 40*mm, f"{month} Reading Tracker")
        
        # Create table for books
        c.setFont('Helvetica-Bold', 10)
        c.setFillColor(primary_color)
        
        # Table headers
        headers = ["Date", "Title", "Author", "Genre", "Rating", "Notes"]
        col_widths = [20*mm, 50*mm, 40*mm, 30*mm, 20*mm, 50*mm]
        start_x = 20*mm
        start_y = height - 70*mm
        
        # Draw headers
        x_pos = start_x
        for i, header in enumerate(headers):
            c.drawString(x_pos + 2, start_y, header)
            # Draw cell border
            c.setStrokeColor(colors.gray)
            c.setLineWidth(0.5)
            c.rect(x_pos, start_y - 15*mm, col_widths[i], 200*mm, stroke=1, fill=0)
            x_pos += col_widths[i]
        
        # Draw row lines
        for row in range(15):  # 15 rows for books
            y_pos = start_y - 15*mm - (row * 13*mm)
            c.line(start_x, y_pos, start_x + sum(col_widths), y_pos)
        
        # Monthly challenge section
        c.setFont('Helvetica-Bold', 14)
        c.setFillColor(accent_color)
        c.drawString(20*mm, 80*mm, f"{month} Reading Challenge:")
        
        c.setFont('Helvetica', 11)
        c.setFillColor(primary_color)
        challenges = [
            f"Books to read this month: _____",
            f"Challenge: Read a book about _____",
            f"Try a new genre: _____",
            f"Monthly reading time goal: _____ hours"
        ]
        
        for i, challenge in enumerate(challenges):
            c.drawString(30*mm, 65*mm - i*15*mm, f"• {challenge}")
        
        add_footer(c, 4 + month_idx)
        c.showPage()
    
    # Pages 14-18: Book Review Templates (5 pages)
    for review_num in range(5):
        c.setFillColor(colors.white)
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        c.setFillColor(primary_color)
        c.setFont('Helvetica-Bold', 20)
        c.drawCentredString(width/2, height - 40*mm, "Book Review")
        
        # Review fields
        c.setFont('Helvetica-Bold', 12)
        c.setFillColor(accent_color)
        
        fields = [
            ("Book Title:", 100*mm),
            ("Author:", 100*mm),
            ("Date Started:", 100*mm),
            ("Date Finished:", 100*mm),
            ("Genre:", 100*mm),
            ("Rating: ___ / 5", 100*mm),
            ("Summary (in your own words):", 180*mm),
            ("What I Loved:", 180*mm),
            ("What Could Be Better:", 180*mm),
            ("Memorable Quotes:", 180*mm),
            ("Would I Recommend? Yes/No:", 100*mm),
            ("To Whom:", 100*mm)
        ]
        
        start_y = height - 70*mm
        for i, (field, height_mm) in enumerate(fields):
            y_pos = start_y - (i * 20*mm)
            c.drawString(30*mm, y_pos, field)
            
            # Draw line for writing
            c.setStrokeColor(colors.gray)
            c.setLineWidth(0.5)
            line_y = y_pos - 5*mm
            if "Summary" in field or "Loved" in field or "Better" in field or "Quotes" in field:
                # Multi-line fields
                c.line(30*mm, line_y, width - 30*mm, line_y)
                c.line(30*mm, line_y - 15*mm, width - 30*mm, line_y - 15*mm)
                c.line(30*mm, line_y - 30*mm, width - 30*mm, line_y - 30*mm)
            else:
                # Single line fields
                c.line(30*mm, line_y, width - 30*mm, line_y)
        
        add_footer(c, 14 + review_num)
        c.showPage()
    
    # Pages 19-21: Reading Wishlist (3 pages)
    for wishlist_page in range(3):
        c.setFillColor(colors.white)
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        c.setFillColor(primary_color)
        c.setFont('Helvetica-Bold', 20)
        c.drawCentredString(width/2, height - 40*mm, f"Reading Wishlist")
        
        if wishlist_page == 0:
            subtitle = "Books I Want to Read"
        elif wishlist_page == 1:
            subtitle = "Recommended by Friends"
        else:
            subtitle = "Award Winners & Classics"
        
        c.setFont('Helvetica', 14)
        c.setFillColor(accent_color)
        c.drawCentredString(width/2, height - 55*mm, subtitle)
        
        # Create wishlist table
        c.setFont('Helvetica-Bold', 10)
        c.setFillColor(primary_color)
        
        headers = ["Priority", "Title", "Author", "Why I Want to Read It", "Source"]
        col_widths = [20*mm, 50*mm, 40*mm, 60*mm, 30*mm]
        start_x = 20*mm
        start_y = height - 80*mm
        
        # Draw headers
        x_pos = start_x
        for i, header in enumerate(headers):
            c.drawString(x_pos + 2, start_y, header)
            # Draw cell border
            c.setStrokeColor(colors.gray)
            c.setLineWidth(0.5)
            c.rect(x_pos, start_y - 15*mm, col_widths[i], 150*mm, stroke=1, fill=0)
            x_pos += col_widths[i]
        
        # Draw row lines
        for row in range(12):  # 12 rows per page
            y_pos = start_y - 15*mm - (row * 12.5*mm)
            c.line(start_x, y_pos, start_x + sum(col_widths), y_pos)
        
        add_footer(c, 19 + wishlist_page)
        c.showPage()
    
    # Pages 22-23: Reading Statistics (2 pages)
    for stats_page in range(2):
        c.setFillColor(colors.white)
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        if stats_page == 0:
            c.setFillColor(primary_color)
            c.setFont('Helvetica-Bold', 20)
            c.drawCentredString(width/2, height - 40*mm, "Reading Statistics & Insights")
            
            # Statistics categories
            c.setFont('Helvetica-Bold', 14)
            c.setFillColor(accent_color)
            
            categories = [
                "Genre Distribution:",
                "Monthly Reading Pace:",
                "Author Diversity:",
                "Book Length Analysis:",
                "Rating Trends:",
                "Reading Time Patterns:"
            ]
            
            start_y = height - 70*mm
            for i, category in enumerate(categories):
                y_pos = start_y - (i * 25*mm)
                c.drawString(30*mm, y_pos, category)
                
                # Space for charts/notes
                c.setStrokeColor(colors.lightgrey)
                c.setLineWidth(0.5)
                c.rect(30*mm, y_pos - 15*mm, width - 60*mm, 15*mm, stroke=1, fill=0)
        
        else:  # Page 23
            c.setFillColor(primary_color)
            c.setFont('Helvetica-Bold', 20)
            c.drawCentredString(width/2, height - 40*mm, "Reading Milestones & Achievements")
            
            # Achievement tracker
            c.setFont('Helvetica-Bold', 14)
            c.setFillColor(accent_color)
            c.drawString(30*mm, height - 70*mm, "My Reading Achievements:")
            
            achievements = [
                "Read 10 books: □",
                "Read a book over 500 pages: □",
                "Read a classic novel: □",
                "Read a book in 24 hours: □",
                "Complete a series: □",
                "Read a book in another language: □",
                "Attend a book club: □",
                "Meet an author: □",
                "Read a banned book: □",
                "Read a book from every continent: □"
            ]
            
            c.setFont('Helvetica', 11)
            c.setFillColor(primary_color)
            start_y = height - 90*mm
            for i, achievement in enumerate(achievements):
                y_pos = start_y - (i * 15*mm)
                c.drawString(40*mm, y_pos, f"• {achievement}")
        
        add_footer(c, 22 + stats_page)
        c.showPage()
    
    # Pages 24-25: Notes & Resources (2 pages)
    for notes_page in range(2):
        c.setFillColor(colors.white)
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        if notes_page == 0:
            c.setFillColor(primary_color)
            c.setFont('Helvetica-Bold', 20)
            c.drawCentredString(width/2, height - 40*mm, "Reading Notes & Reflections")
            
            c.setFont('Helvetica', 11)
            c.setFillColor(primary_color)
            c.drawString(30*mm, height - 70*mm, "Use this