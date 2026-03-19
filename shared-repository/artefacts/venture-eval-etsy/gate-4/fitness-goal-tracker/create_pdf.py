#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

# Color palette from skill
COLORS = {
    'background': '#F5F0EB',
    'text': '#2C2C2C',
    'accent': '#8B7355',
    'light': '#D4C5B2'
}

def hex_to_color(hex_code):
    """Convert hex color to ReportLab color"""
    hex_code = hex_code.lstrip('#')
    return colors.HexColor(f'#{hex_code}')

def create_fitness_tracker_pdf(output_path):
    """Create Fitness Goal Tracker PDF"""
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Create styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=hex_to_color(COLORS['text']),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=hex_to_color(COLORS['accent']),
        spaceAfter=8,
        alignment=TA_LEFT
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=hex_to_color(COLORS['text']),
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    # Page 1: Cover Page
    c.setFillColor(hex_to_color(COLORS['background']))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(hex_to_color(COLORS['accent']))
    c.rect(20*mm, height-60*mm, width-40*mm, 40*mm, fill=1, stroke=0)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width/2, height-45*mm, "FITNESS GOAL TRACKER")
    
    c.setFillColor(hex_to_color(COLORS['text']))
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height-65*mm, "Your Complete Fitness Journey Companion")
    
    c.setFillColor(hex_to_color(COLORS['accent']))
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(width/2, 100*mm, "RecoveriStudio | Digital Download")
    
    # Footer on every page
    def add_footer():
        c.setFillColor(hex_to_color(COLORS['light']))
        c.setFont("Helvetica", 8)
        c.drawCentredString(width/2, 10*mm, "RecoveriStudio • studio@recoveri.io")
    
    add_footer()
    c.showPage()
    
    # Page 2: Fitness Goal Setting
    c.setFillColor(hex_to_color(COLORS['background']))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(hex_to_color(COLORS['accent']))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(25*mm, height-30*mm, "FITNESS GOAL SETTING")
    
    c.setFillColor(hex_to_color(COLORS['text']))
    c.setFont("Helvetica", 11)
    c.drawString(25*mm, height-40*mm, "Define your objectives and create a clear roadmap for success.")
    
    # Goal setting sections
    y_pos = height - 60*mm
    sections = [
        ("Primary Goal:", "Weight Loss / Muscle Gain / Endurance / Flexibility / Other"),
        ("Target Date:", "________________________________"),
        ("Current Status:", "________________________________"),
        ("Measurements:", "Weight: ______ kg  |  Waist: ______ cm  |  Hips: ______ cm"),
        ("Why This Goal Matters:", "________________________________"),
        ("Specific Actions:", "________________________________"),
        ("Milestone 1 (30 days):", "________________________________"),
        ("Milestone 2 (60 days):", "________________________________"),
        ("Milestone 3 (90 days):", "________________________________"),
        ("Reward for Achieving Goal:", "________________________________")
    ]
    
    c.setFillColor(hex_to_color(COLORS['text']))
    c.setFont("Helvetica", 11)
    
    for label, placeholder in sections:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(25*mm, y_pos, label)
        c.setFont("Helvetica", 11)
        c.drawString(25*mm + 50*mm, y_pos, placeholder)
        y_pos -= 15*mm
    
    add_footer()
    c.showPage()
    
    # Page 3-4: Weekly Workout Planner (2 pages)
    for page_num in range(2):
        c.setFillColor(hex_to_color(COLORS['background']))
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        c.setFillColor(hex_to_color(COLORS['accent']))
        c.setFont("Helvetica-Bold", 18)
        c.drawString(25*mm, height-30*mm, f"WEEKLY WORKOUT PLANNER - WEEK {page_num + 1}")
        
        c.setFillColor(hex_to_color(COLORS['text']))
        c.setFont("Helvetica", 11)
        c.drawString(25*mm, height-40*mm, "Plan your exercise routine for the week ahead.")
        
        # Create table for days of week
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_width = (width - 50*mm) / 7
        
        y_start = height - 70*mm
        cell_height = 15*mm
        
        # Draw day headers
        c.setFillColor(hex_to_color(COLORS['accent']))
        for i, day in enumerate(days):
            x = 25*mm + i * day_width
            c.rect(x, y_start, day_width, cell_height, fill=1, stroke=1)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(x + day_width/2, y_start + cell_height/2 - 3*mm, day[:3])
            c.setFillColor(hex_to_color(COLORS['accent']))
        
        # Draw workout rows
        workout_types = ["Cardio", "Strength", "Flexibility", "Rest/Active Recovery"]
        for row, workout in enumerate(workout_types):
            y = y_start - (row + 1) * cell_height
            c.setFillColor(hex_to_color(COLORS['light']))
            c.rect(25*mm, y, day_width * 7, cell_height, fill=1, stroke=1)
            
            c.setFillColor(hex_to_color(COLORS['text']))
            c.setFont("Helvetica-Bold", 10)
            c.drawString(27*mm, y + cell_height/2 - 3*mm, workout)
            
            # Draw cells for each day
            for i in range(7):
                x = 25*mm + i * day_width
                c.setFillColor(colors.white)
                c.rect(x, y, day_width, cell_height, fill=0, stroke=1)
        
        # Notes section
        c.setFillColor(hex_to_color(COLORS['text']))
        c.setFont("Helvetica-Bold", 12)
        c.drawString(25*mm, y_start - 6*cell_height, "Weekly Notes:")
        
        c.setFillColor(colors.white)
        c.rect(25*mm, y_start - 7*cell_height, width - 50*mm, 40*mm, fill=1, stroke=1)
        
        add_footer()
        if page_num < 1:
            c.showPage()
    
    # Page 5-6: Exercise Log (2 pages)
    for page_num in range(2):
        c.setFillColor(hex_to_color(COLORS['background']))
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        c.setFillColor(hex_to_color(COLORS['accent']))
        c.setFont("Helvetica-Bold", 18)
        c.drawString(25*mm, height-30*mm, f"EXERCISE LOG - WEEK {page_num + 1}")
        
        # Table headers
        headers = ["Date", "Exercise", "Sets", "Reps", "Weight", "Duration", "Notes"]
        col_widths = [20*mm, 35*mm, 15*mm, 15*mm, 20*mm, 20*mm, 45*mm]
        
        y_start = height - 50*mm
        row_height = 8*mm
        
        # Draw headers
        x_pos = 25*mm
        c.setFillColor(hex_to_color(COLORS['accent']))
        for i, header in enumerate(headers):
            c.rect(x_pos, y_start, col_widths[i], row_height, fill=1, stroke=1)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(x_pos + col_widths[i]/2, y_start + row_height/2 - 2.5*mm, header)
            c.setFillColor(hex_to_color(COLORS['accent']))
            x_pos += col_widths[i]
        
        # Draw rows (14 rows per page)
        for row in range(14):
            y = y_start - (row + 1) * row_height
            x_pos = 25*mm
            for i in range(len(headers)):
                c.setFillColor(colors.white if row % 2 == 0 else hex_to_color(COLORS['background']))
                c.rect(x_pos, y, col_widths[i], row_height, fill=1, stroke=1)
                x_pos += col_widths[i]
        
        add_footer()
        if page_num < 1:
            c.showPage()
    
    # Page 7: Progress Tracker
    c.setFillColor(hex_to_color(COLORS['background']))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(hex_to_color(COLORS['accent']))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(25*mm, height-30*mm, "PROGRESS TRACKER")
    
    # Progress table
    headers = ["Week", "Weight (kg)", "Waist (cm)", "Hips (cm)", "Energy Level", "Notes"]
    col_widths = [20*mm, 25*mm, 25*mm, 25*mm, 30*mm, 65*mm]
    
    y_start = height - 50*mm
    row_height = 10*mm
    
    # Draw headers
    x_pos = 25*mm
    c.setFillColor(hex_to_color(COLORS['accent']))
    for i, header in enumerate(headers):
        c.rect(x_pos, y_start, col_widths[i], row_height, fill=1, stroke=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x_pos + col_widths[i]/2, y_start + row_height/2 - 2.5*mm, header)
        c.setFillColor(hex_to_color(COLORS['accent']))
        x_pos += col_widths[i]
    
    # Draw 12 weeks of tracking
    for week in range(1, 13):
        y = y_start - week * row_height
        x_pos = 25*mm
        for i in range(len(headers)):
            c.setFillColor(colors.white if week % 2 == 0 else hex_to_color(COLORS['background']))
            c.rect(x_pos, y, col_widths[i], row_height, fill=1, stroke=1)
            if i == 0:  # Week number
                c.setFillColor(hex_to_color(COLORS['text']))
                c.setFont("Helvetica-Bold", 9)
                c.drawCentredString(x_pos + col_widths[i]/2, y + row_height/2 - 3*mm, str(week))
            x_pos += col_widths[i]
    
    add_footer()
    c.showPage()
    
    # Page 8: Habit Tracker
    c.setFillColor(hex_to_color(COLORS['background']))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(hex_to_color(COLORS['accent']))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(25*mm, height-30*mm, "FITNESS HABIT TRACKER")
    
    habits = [
        "Morning Exercise",
        "Evening Walk",
        "8 Glasses Water",
        "7+ Hours Sleep",
        "Protein Goal",
        "Vegetables 5x",
        "No Sugary Drinks",
        "Stretching",
        "Meditation",
        "Step Goal (10k)"
    ]
    
    y_start = height - 50*mm
    habit_height = 12*mm
    day_width = 10*mm
    
    # Draw habit labels
    c.setFillColor(hex_to_color(COLORS['text']))
    c.setFont("Helvetica", 10)
    for i, habit in enumerate(habits):
        y = y_start - i * habit_height
        c.drawString(25*mm, y + habit_height/2 - 3*mm, habit)
    
    # Draw 30-day grid
    for day in range(30):
        x = 80*mm + day * day_width
        c.setFillColor(colors.white)
        c.rect(x, y_start, day_width, -len(habits)*habit_height, fill=0, stroke=1)
        
        # Day number
        c.setFillColor(hex_to_color(COLORS['text']))
        c.setFont("Helvetica", 7)
        c.drawCentredString(x + day_width/2, y_start + 2*mm, str(day + 1))
    
    add_footer()
    c.showPage()
    
    # Page 9-10: Nutrition Notes (2 pages)
    for page_num in range(2):
        c.setFillColor(hex_to_color(COLORS['background']))
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        c.setFillColor(hex_to_color(COLORS['accent']))
        c.setFont("Helvetica-Bold", 18)
        c.drawString(25*mm, height-30*mm, f"NUTRITION NOTES - WEEK {page_num + 1}")
        
        # Daily nutrition log
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        y_start = height - 50*mm
        
        for i, day in enumerate(days):
            y = y_start - i * 35*mm
            
            # Day header
            c.setFillColor(hex_to_color(COLORS['light']))
            c.rect(25*mm, y, width - 50*mm, 8*mm, fill=1, stroke=1)
            c.setFillColor(hex_to_color(COLORS['text']))
            c.setFont("Helvetica-Bold", 10)
            c.drawString(27*mm, y + 2*mm, day)
            
            # Meal sections
            meals = ["Breakfast:", "Lunch:", "Dinner:", "Snacks:", "Water:"]
            for j, meal in enumerate(meals):
                meal_y = y - (j + 1) * 5*mm
                c.setFillColor(hex_to_color(COLORS['text']))
                c.setFont("Helvetica", 9)
                c.drawString(27*mm, meal_y, meal)
        
        add_footer()
        if page_num < 1:
            c.showPage()
    
    # Page 11: Motivational Quotes
    c.setFillColor(hex_to_color(COLORS['background']))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(hex_to_color(COLORS['accent']))
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height-40*mm, "MOTIVATIONAL QUOTES")
    
    quotes = [
        "The only bad workout is the one that didn't happen.",
        "Progress, not perfection.",
        "Your body can stand almost anything. It's your mind you have to convince.",
        "The secret of getting ahead is getting started.",
        "Don't wish for it, work for it.",
        "Small steps every day lead to big results.",
        "You are stronger than you think.",
        "The pain you feel today will be the strength you feel tomorrow.",
        "Consistency is the key to results.",
        "Your future self will thank you."
    ]
    
    y_pos = height - 70*mm
    c.setFillColor(hex_to_color(COLORS['text']))
    c.setFont("Helvetica-Oblique", 12)
    
    for i, quote in enumerate(quotes):
        c.drawCentredString(width/2, y_pos, f'"{quote}"')
        y_pos -= 20*mm
    
    add_footer()
    c.showPage()
    
    # Page 12: Instructions & Final Page
    c.setFillColor(hex_to_color(COLORS['background']))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setFillColor(hex_to_color(COLORS['accent']))
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height-40*mm, "HOW TO USE THIS TRACKER")
    
    instructions = [
        "1. Start by setting clear fitness goals on page 2",
        "2. Plan your weekly workouts using the planner (pages 3-4)",
        "3. Log each exercise session in the exercise log (pages 5-6)",
        "4. Track your progress weekly (page 7)",
        "5. Build consistent habits with the habit tracker (page 8)",
        "6. Monitor nutrition and hydration (pages 9-10)",
        "7. Stay motivated with inspirational quotes (page 11)",
        "",
        "TIPS FOR SUCCESS:",
        "• Be consistent - use your tracker daily",
        "• Be honest - record accurate information",
        "• Celebrate small wins along the way",
        "• Review your progress weekly",
        "• Adjust your plan as needed",
        "",
        "Thank you for choosing RecoveriStudio!",
        "We wish you success on your fitness journey."
    ]
    
    y_pos = height - 70*mm
    c.setFillColor(hex_to_color(COLORS['text']))
    c.setFont("Helvetica", 11)
    
    for instruction in instructions:
        if instruction.startswith("TIPS FOR SUCCESS:"):
            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(hex_to_color(COLORS['accent']))
        elif instruction.startswith("•"):
            c.setFont("Helvetica", 10)
            c.setFillColor(hex_to_color(COLORS['text']))
        
        c.drawString(40*mm, y_pos, instruction)
        y_pos -= 6*mm if instruction.startswith("•") else 8*mm
    
    add_footer()
    
    # Save the PDF
    c.save()
    print(f"PDF created successfully: {output_path}")

if __name__ == "__main__":
    output_dir = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/fitness-goal-tracker"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "product.pdf")
    create_fitness_tracker_pdf(output_path)