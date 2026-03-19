#!/usr/bin/env python3
"""
Create Daily Habit Tracker PDF for RecoveriStudio Etsy shop.
A4 size, 12 pages, neutral colour palette.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, PageBreak, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import datetime

# Colour palette
COLOR_BG = HexColor('#F5F0EB')      # Light cream background
COLOR_TEXT = HexColor('#2C2C2C')    # Dark gray text
COLOR_ACCENT = HexColor('#8B7355')  # Warm brown accent
COLOR_LIGHT = HexColor('#D4C5B2')   # Light tan

# Page dimensions
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 20 * mm

def create_pdf(filename):
    """Create the habit tracker PDF."""
    c = canvas.Canvas(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=COLOR_TEXT,
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=COLOR_ACCENT,
        alignment=TA_LEFT,
        spaceAfter=8
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=COLOR_TEXT,
        alignment=TA_LEFT,
        spaceAfter=6
    )
    
    # Create 12 pages
    for page_num in range(12):
        # Set background colour
        c.setFillColor(COLOR_BG)
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        # Draw header
        c.setFillColor(COLOR_ACCENT)
        c.rect(MARGIN, PAGE_HEIGHT - 40*mm, PAGE_WIDTH - 2*MARGIN, 30*mm, fill=1, stroke=0)
        
        # Title
        c.setFillColor(COLOR_BG)
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 55*mm, "Daily Habit Tracker")
        
        # Page number and footer
        c.setFillColor(COLOR_TEXT)
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN, 15*mm, f"Page {page_num + 1} of 12")
        c.drawRightString(PAGE_WIDTH - MARGIN, 15*mm, "RecoveriStudio")
        
        # Draw content based on page type
        if page_num == 0:
            # Cover page
            c.setFillColor(COLOR_TEXT)
            c.setFont("Helvetica", 14)
            c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 + 40*mm, "Build Better Habits")
            c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 + 20*mm, "One Day at a Time")
            
            c.setFont("Helvetica", 11)
            c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 10*mm, "Printable PDF Planner")
            c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 25*mm, "A4 Size • 12 Pages • Undated")
            
            # Decorative elements
            c.setFillColor(COLOR_LIGHT)
            for i in range(5):
                x = MARGIN + i * 40*mm
                y = 100*mm
                c.circle(x, y, 8*mm, fill=1, stroke=0)
                
        elif page_num == 1:
            # Instructions page
            c.setFillColor(COLOR_TEXT)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(MARGIN, PAGE_HEIGHT - 80*mm, "How to Use This Habit Tracker")
            
            c.setFont("Helvetica", 11)
            instructions = [
                "1. Choose 5-10 habits you want to build or track",
                "2. Write them in the 'My Habits' section on page 3",
                "3. Each day, mark completed habits with an X or ✓",
                "4. Review your progress weekly on the reflection pages",
                "5. Celebrate streaks and consistency!",
                "",
                "Tips for Success:",
                "• Start with just 2-3 easy habits to build momentum",
                "• Place your tracker where you'll see it daily",
                "• Be kind to yourself if you miss a day",
                "• Focus on consistency, not perfection"
            ]
            
            y_pos = PAGE_HEIGHT - 100*mm
            for line in instructions:
                c.drawString(MARGIN + 10*mm, y_pos, line)
                y_pos -= 7*mm
                
        elif page_num == 2:
            # Habits setup page
            c.setFillColor(COLOR_TEXT)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(MARGIN, PAGE_HEIGHT - 80*mm, "My Habits")
            c.setFont("Helvetica", 12)
            c.drawString(MARGIN, PAGE_HEIGHT - 95*mm, "List the habits you want to track this month:")
            
            # Habit input boxes
            c.setFillColor(COLOR_LIGHT)
            for i in range(12):
                y = PAGE_HEIGHT - (120 + i*15)*mm
                if y > 40*mm:  # Keep above footer
                    c.rect(MARGIN, y, PAGE_WIDTH - 2*MARGIN, 10*mm, fill=1, stroke=1)
                    c.setFillColor(COLOR_TEXT)
                    c.setFont("Helvetica", 10)
                    c.drawString(MARGIN + 5*mm, y + 3*mm, f"{i+1}.")
                    c.setFillColor(COLOR_LIGHT)
                    
        elif page_num in [3, 4, 5, 6]:
            # Monthly calendar pages (4 pages)
            month_offset = page_num - 3
            c.setFillColor(COLOR_TEXT)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(MARGIN, PAGE_HEIGHT - 80*mm, f"Month {month_offset + 1}")
            
            # Create calendar grid
            cell_width = (PAGE_WIDTH - 2*MARGIN) / 8
            cell_height = 15*mm
            
            # Day headers
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "✓"]
            c.setFont("Helvetica-Bold", 10)
            for col, day in enumerate(days):
                x = MARGIN + col * cell_width
                y = PAGE_HEIGHT - 100*mm
                c.rect(x, y, cell_width, cell_height, fill=0, stroke=1)
                c.drawCentredString(x + cell_width/2, y + cell_height/2 - 3*mm, day)
            
            # 31 days grid
            for day in range(1, 32):
                row = (day - 1) // 7
                col = (day - 1) % 7
                x = MARGIN + col * cell_width
                y = PAGE_HEIGHT - (100 + (row + 1) * cell_height)*mm
                
                if y > 50*mm:  # Keep above footer
                    c.rect(x, y, cell_width, cell_height, fill=0, stroke=1)
                    c.setFont("Helvetica", 9)
                    c.drawCentredString(x + cell_width/2, y + cell_height/2 - 2*mm, str(day))
            
            # Habit tracking columns
            habits = ["Habit 1", "Habit 2", "Habit 3", "Habit 4", "Habit 5"]
            for i, habit in enumerate(habits):
                x = MARGIN + 7 * cell_width
                y = PAGE_HEIGHT - (100 + i * cell_height)*mm
                if y > 50*mm:
                    c.rect(x, y, cell_width, cell_height, fill=0, stroke=1)
                    c.setFont("Helvetica", 8)
                    c.drawString(x + 2*mm, y + cell_height/2 - 2*mm, habit[:10])
                    
        elif page_num in [7, 8, 9, 10]:
            # Weekly reflection pages (4 pages)
            week_num = page_num - 6
            c.setFillColor(COLOR_TEXT)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(MARGIN, PAGE_HEIGHT - 80*mm, f"Week {week_num} Reflection")
            
            # Prompts
            prompts = [
                "What habits went well this week?",
                "What was challenging?",
                "What helped me stay consistent?",
                "What can I improve next week?",
                "My biggest achievement this week:",
                "One thing I learned about myself:",
                "How I'll reward my progress:"
            ]
            
            y_pos = PAGE_HEIGHT - 100*mm
            for i, prompt in enumerate(prompts):
                c.setFont("Helvetica-Bold", 11)
                c.drawString(MARGIN, y_pos, prompt)
                
                # Response area
                c.setFillColor(COLOR_LIGHT)
                c.rect(MARGIN, y_pos - 15*mm, PAGE_WIDTH - 2*MARGIN, 12*mm, fill=1, stroke=1)
                c.setFillColor(COLOR_TEXT)
                
                y_pos -= 30*mm
                
        elif page_num == 11:
            # Achievement page
            c.setFillColor(COLOR_TEXT)
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 80*mm, "Celebrate Your Progress!")
            
            c.setFont("Helvetica", 12)
            c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 100*mm, "Consistency is the key to lasting change.")
            c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 115*mm, "Every checkmark is a step toward a better you.")
            
            # Achievement badges
            badges = [
                ("7-Day Streak", "Consistency Starter"),
                ("30 Days Complete", "Habit Builder"),
                ("3 Months", "Transformation Trailblazer"),
                ("6 Months", "Master of Routine"),
                ("1 Year", "Legend of Discipline")
            ]
            
            y_pos = PAGE_HEIGHT - 150*mm
            for badge, title in badges:
                c.setFillColor(COLOR_ACCENT)
                c.circle(PAGE_WIDTH/2, y_pos, 15*mm, fill=1, stroke=0)
                c.setFillColor(COLOR_BG)
                c.setFont("Helvetica-Bold", 10)
                c.drawCentredString(PAGE_WIDTH/2, y_pos + 2*mm, badge)
                c.setFont("Helvetica", 9)
                c.drawCentredString(PAGE_WIDTH/2, y_pos - 8*mm, title)
                y_pos -= 40*mm
            
            c.setFillColor(COLOR_TEXT)
            c.setFont("Helvetica-Oblique", 10)
            c.drawCentredString(PAGE_WIDTH/2, 40*mm, "Thank you for choosing RecoveriStudio!")
            c.drawCentredString(PAGE_WIDTH/2, 30*mm, "studio@recoveri.io")
        
        # Add page
        c.showPage()
    
    # Save PDF
    c.save()
    print(f"Created PDF: {filename}")

if __name__ == "__main__":
    create_pdf("product.pdf")