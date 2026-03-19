#!/usr/bin/env python3
"""
Create Etsy mockup image for Daily Habit Tracker.
Size: 2700x2025px (Etsy recommended).
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Dimensions
WIDTH = 2700
HEIGHT = 2025

# Colour palette (same as PDF)
COLOR_BG = (245, 240, 235)      # #F5F0EB Light cream
COLOR_TEXT = (44, 44, 44)       # #2C2C2C Dark gray
COLOR_ACCENT = (139, 115, 85)   # #8B7355 Warm brown
COLOR_LIGHT = (212, 197, 178)   # #D4C5B2 Light tan

def create_mockup():
    """Create the Etsy mockup image."""
    # Create blank image
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fall back to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 120)
        subtitle_font = ImageFont.truetype("arial.ttf", 70)
        text_font = ImageFont.truetype("arial.ttf", 50)
        small_font = ImageFont.truetype("arial.ttf", 40)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw background elements
    # Top accent bar
    draw.rectangle([0, 0, WIDTH, 250], fill=COLOR_ACCENT)
    
    # Title
    draw.text((WIDTH//2, 125), "Daily Habit Tracker", 
              fill=COLOR_BG, font=title_font, anchor="mm")
    
    # Subtitle
    draw.text((WIDTH//2, 225), "Printable PDF Planner | A4 Size | 12 Pages", 
              fill=COLOR_LIGHT, font=subtitle_font, anchor="mm")
    
    # Create mockup of PDF pages
    page_width = 600
    page_height = int(page_width * 1.414)  # A4 ratio
    
    # Position for "open book" effect
    x_center = WIDTH // 2
    y_center = HEIGHT // 2 + 100
    
    # Left page (angled)
    left_page = [
        (x_center - page_width - 50, y_center - page_height//2),
        (x_center - 100, y_center - page_height//2),
        (x_center - 100, y_center + page_height//2),
        (x_center - page_width - 50, y_center + page_height//2)
    ]
    draw.polygon(left_page, fill=(255, 255, 255), outline=COLOR_TEXT, width=3)
    
    # Right page (angled)
    right_page = [
        (x_center + 100, y_center - page_height//2),
        (x_center + page_width + 50, y_center - page_height//2),
        (x_center + page_width + 50, y_center + page_height//2),
        (x_center + 100, y_center + page_height//2)
    ]
    draw.polygon(right_page, fill=(255, 255, 255), outline=COLOR_TEXT, width=3)
    
    # Add page content simulation
    # Left page content
    content_y = y_center - page_height//2 + 80
    draw.text((x_center - page_width - 20, content_y), "Daily Habit Tracker", 
              fill=COLOR_ACCENT, font=text_font)
    
    # Habit grid simulation
    grid_size = 30
    grid_start_x = x_center - page_width + 50
    grid_start_y = content_y + 100
    
    for row in range(5):
        for col in range(7):
            x = grid_start_x + col * (grid_size + 10)
            y = grid_start_y + row * (grid_size + 10)
            draw.rectangle([x, y, x + grid_size, y + grid_size], 
                          fill=COLOR_LIGHT, outline=COLOR_TEXT, width=1)
    
    # Right page content
    draw.text((x_center + 150, content_y), "Week 1 Reflection", 
              fill=COLOR_ACCENT, font=text_font)
    
    # Reflection text lines
    for i in range(4):
        y = content_y + 100 + i * 60
        draw.rectangle([x_center + 120, y, x_center + page_width - 50, y + 40], 
                      fill=COLOR_BG, outline=COLOR_LIGHT, width=2)
    
    # Shadow effect
    shadow_points = [
        (x_center - page_width - 60, y_center - page_height//2 - 10),
        (x_center + page_width + 60, y_center - page_height//2 - 10),
        (x_center + page_width + 40, y_center + page_height//2 + 20),
        (x_center - page_width - 40, y_center + page_height//2 + 20)
    ]
    draw.polygon(shadow_points, fill=(200, 200, 200, 128))
    
    # Features list on right side
    features = [
        "✓ 12 Printable A4 Pages",
        "✓ Undated - Use Any Time",
        "✓ Daily & Weekly Tracking",
        "✓ Habit Setup Section",
        "✓ Monthly Calendar Views",
        "✓ Weekly Reflection Pages",
        "✓ Achievement Badges",
        "✓ Clean Minimalist Design"
    ]
    
    features_x = WIDTH - 600
    features_y = y_center - 200
    
    for i, feature in enumerate(features):
        y = features_y + i * 70
        draw.text((features_x, y), feature, fill=COLOR_TEXT, font=text_font)
    
    # Price tag
    price_bg = (x_center - 300, HEIGHT - 300, x_center + 300, HEIGHT - 150)
    draw.rounded_rectangle(price_bg, radius=40, fill=COLOR_ACCENT)
    
    draw.text((x_center, HEIGHT - 280), "Instant Digital Download", 
              fill=COLOR_BG, font=subtitle_font, anchor="mm")
    
    draw.text((x_center, HEIGHT - 200), "£3.49", 
              fill=(255, 255, 255), font=ImageFont.truetype("arial.ttf", 100) if os.path.exists("arial.ttf") else ImageFont.load_default(), 
              anchor="mm")
    
    # Footer
    draw.text((WIDTH//2, HEIGHT - 50), "RecoveriStudio | studio@recoveri.io", 
              fill=COLOR_TEXT, font=small_font, anchor="mm")
    
    # Save image
    img.save("mockup.png", "PNG", quality=95)
    print(f"Created mockup: mockup.png ({WIDTH}x{HEIGHT}px)")

if __name__ == "__main__":
    create_mockup()