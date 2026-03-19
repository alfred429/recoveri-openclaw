#!/usr/bin/env python3
"""
Create Etsy mockup image for Social Media Content Calendar
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Etsy recommended size: 2700x2025px
WIDTH = 2700
HEIGHT = 2025

# Brand colors
COLOR_BG = (245, 240, 235)  # #F5F0EB
COLOR_TEXT = (44, 44, 44)   # #2C2C2C
COLOR_ACCENT = (139, 115, 85)  # #8B7355
COLOR_LIGHT = (212, 197, 178)  # #D4C5B2
COLOR_WHITE = (255, 255, 255)

def create_mockup():
    """Create Etsy listing mockup image"""
    
    # Create blank image
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts, fall back to default if not available
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
        body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw decorative elements
    # Top accent bar
    draw.rectangle([0, 0, WIDTH, 100], fill=COLOR_ACCENT)
    
    # Bottom accent bar
    draw.rectangle([0, HEIGHT-100, WIDTH, HEIGHT], fill=COLOR_ACCENT)
    
    # Main product mockup area
    mockup_width = 1800
    mockup_height = 1200
    mockup_x = (WIDTH - mockup_width) // 2
    mockup_y = 200
    
    # Mockup background (represents a desk/table)
    draw.rectangle([mockup_x, mockup_y, mockup_x + mockup_width, mockup_y + mockup_height], 
                   fill=COLOR_WHITE, outline=COLOR_LIGHT, width=10)
    
    # Draw "PDF pages" on the mockup
    page_width = 600
    page_height = 800
    
    # First page (angled)
    page1_points = [
        (mockup_x + 400, mockup_y + 200),
        (mockup_x + 400 + page_width, mockup_y + 200),
        (mockup_x + 380 + page_width, mockup_y + 200 + page_height),
        (mockup_x + 380, mockup_y + 200 + page_height)
    ]
    draw.polygon(page1_points, fill=COLOR_WHITE, outline=COLOR_TEXT, width=3)
    
    # Second page (on top of first)
    page2_points = [
        (mockup_x + 420, mockup_y + 180),
        (mockup_x + 420 + page_width, mockup_y + 180),
        (mockup_x + 400 + page_width, mockup_y + 180 + page_height),
        (mockup_x + 400, mockup_y + 180 + page_height)
    ]
    draw.polygon(page2_points, fill=COLOR_WHITE, outline=COLOR_TEXT, width=3)
    
    # Draw page content preview
    # Calendar grid on first page
    grid_size = 80
    grid_start_x = mockup_x + 450
    grid_start_y = mockup_y + 250
    
    for i in range(4):
        for j in range(7):
            x = grid_start_x + j * grid_size
            y = grid_start_y + i * grid_size
            draw.rectangle([x, y, x + grid_size - 5, y + grid_size - 5], 
                          fill=COLOR_BG, outline=COLOR_LIGHT, width=2)
    
    # Month label
    draw.text((grid_start_x + 100, grid_start_y - 50), "JANUARY 2025", 
              fill=COLOR_ACCENT, font=subtitle_font)
    
    # Platform labels on second page
    platforms = ["Instagram", "Facebook", "TikTok", "Pinterest"]
    platform_start_x = mockup_x + 850
    platform_start_y = mockup_y + 250
    
    for i, platform in enumerate(platforms):
        y = platform_start_y + i * 100
        draw.rectangle([platform_start_x, y, platform_start_x + 400, y + 80], 
                      fill=COLOR_LIGHT, outline=COLOR_TEXT, width=2)
        draw.text((platform_start_x + 20, y + 20), platform, 
                  fill=COLOR_TEXT, font=body_font)
    
    # Title text
    title = "Social Media Content Calendar"
    title_width = draw.textlength(title, font=title_font)
    draw.text(((WIDTH - title_width) // 2, mockup_y + mockup_height + 100), 
              title, fill=COLOR_TEXT, font=title_font)
    
    # Subtitle
    subtitle = "Digital Planner | PDF Download | 48 Pages"
    subtitle_width = draw.textlength(subtitle, font=subtitle_font)
    draw.text(((WIDTH - subtitle_width) // 2, mockup_y + mockup_height + 200), 
              subtitle, fill=COLOR_ACCENT, font=subtitle_font)
    
    # Features list
    features = [
        "✓ 12-Month Content Planning",
        "✓ Multiple Platform Tracking", 
        "✓ Performance Analytics",
        "✓ Content Bank for Repurposing",
        "✓ A4 Size | Printable & Digital",
        "✓ Instant Download"
    ]
    
    features_start_y = mockup_y + mockup_height + 300
    for i, feature in enumerate(features):
        y = features_start_y + i * 60
        draw.text((mockup_x + 200, y), feature, fill=COLOR_TEXT, font=body_font)
    
    # Price tag
    price_bg_x = WIDTH - 500
    price_bg_y = 150
    price_bg_width = 400
    price_bg_height = 150
    
    # Price background
    draw.rounded_rectangle([price_bg_x, price_bg_y, 
                           price_bg_x + price_bg_width, 
                           price_bg_y + price_bg_height], 
                          radius=30, fill=COLOR_ACCENT)
    
    # Price text
    draw.text((price_bg_x + 100, price_bg_y + 30), "£4.99", 
              fill=COLOR_WHITE, font=title_font)
    
    draw.text((price_bg_x + 120, price_bg_y + 100), "Digital Download", 
              fill=COLOR_WHITE, font=small_font)
    
    # Brand footer
    brand_text = "RecoveriStudio | studio@recoveri.io"
    brand_width = draw.textlength(brand_text, font=small_font)
    draw.text(((WIDTH - brand_width) // 2, HEIGHT - 70), 
              brand_text, fill=COLOR_WHITE, font=small_font)
    
    # Save image
    output_path = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/social-media-calendar/mockup.png"
    img.save(output_path, "PNG", quality=95)
    print(f"Mockup created successfully: {output_path}")
    
    # Show image info
    print(f"Image size: {img.size}")
    print(f"Image mode: {img.mode}")

if __name__ == "__main__":
    create_mockup()