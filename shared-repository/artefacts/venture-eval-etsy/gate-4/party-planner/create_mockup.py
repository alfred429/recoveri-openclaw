#!/usr/bin/env python3
"""
Create Etsy mockup image for Party Planner Template
Size: 2700x2025px (Etsy recommended)
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Etsy recommended size
WIDTH = 2700
HEIGHT = 2025

# Colors from RecoveriStudio palette
BG_COLOR = (245, 240, 235)  # #F5F0EB
TEXT_COLOR = (44, 44, 44)   # #2C2C2C
ACCENT1 = (139, 115, 85)    # #8B7355
ACCENT2 = (212, 197, 178)   # #D4C5B2

def create_mockup():
    """Create the mockup image"""
    # Create blank image
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Add subtle background pattern (diagonal lines)
    for i in range(-HEIGHT, WIDTH + HEIGHT, 40):
        draw.line([(i, 0), (i + HEIGHT, HEIGHT)], fill=ACCENT2, width=2)
    
    # Create "product preview" area
    preview_width = 1800
    preview_height = 1350
    preview_x = (WIDTH - preview_width) // 2
    preview_y = (HEIGHT - preview_height) // 2 - 100
    
    # Draw product preview background (simulating pages)
    draw.rectangle([preview_x, preview_y, preview_x + preview_width, preview_y + preview_height], 
                   fill=(255, 255, 255), outline=ACCENT1, width=8)
    
    # Draw "pages" effect
    for i in range(1, 4):
        page_offset = i * 15
        draw.rectangle([preview_x + page_offset, preview_y + page_offset, 
                       preview_x + preview_width - page_offset, preview_y + preview_height - page_offset],
                       outline=ACCENT2, width=2)
    
    # Add page content preview
    # Page title
    draw.rectangle([preview_x + 100, preview_y + 100, preview_x + preview_width - 100, preview_y + 180],
                   fill=ACCENT2, outline=ACCENT1, width=3)
    
    # Sample text lines
    y = preview_y + 220
    for i in range(1, 9):
        line_width = 1400 if i % 3 == 0 else 1000
        draw.rectangle([preview_x + 150, y, preview_x + 150 + line_width, y + 40],
                       fill=BG_COLOR, outline=ACCENT2, width=2)
        y += 60
    
    # Add checkboxes
    y = preview_y + 250
    for i in range(1, 6):
        draw.rectangle([preview_x + 180, y, preview_x + 210, y + 30],
                       fill=(255, 255, 255), outline=TEXT_COLOR, width=2)
        y += 80
    
    # Product title
    try:
        # Try to use a system font
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 80)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Main title
    title = "PARTY PLANNER TEMPLATE"
    title_bbox = draw.textbbox((0, 0), title, font=font_large)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (WIDTH - title_width) // 2
    draw.text((title_x, preview_y - 300), title, fill=ACCENT1, font=font_large)
    
    # Subtitle
    subtitle = "Digital Printable | 8-Page A4 PDF"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (WIDTH - subtitle_width) // 2
    draw.text((subtitle_x, preview_y - 180), subtitle, fill=TEXT_COLOR, font=font_medium)
    
    # Features
    features = [
        "✓ Guest List & RSVP Tracker",
        "✓ Budget Planner with Categories", 
        "✓ 6-Week Timeline Checklist",
        "✓ Menu & Catering Planner",
        "✓ Decorations & Theme Ideas",
        "✓ Vendor Contact Sheet",
        "✓ Seating Chart Template",
        "✓ Thank You Notes Tracker"
    ]
    
    y = preview_y + preview_height + 100
    for feature in features:
        feature_bbox = draw.textbbox((0, 0), feature, font=font_small)
        feature_width = feature_bbox[2] - feature_bbox[0]
        feature_x = (WIDTH - feature_width) // 2
        draw.text((feature_x, y), feature, fill=TEXT_COLOR, font=font_small)
        y += 80
    
    # Price tag
    price_bg_x = WIDTH - 400
    price_bg_y = 150
    draw.rectangle([price_bg_x, price_bg_y, price_bg_x + 350, price_bg_y + 150],
                   fill=ACCENT1, outline=TEXT_COLOR, width=4)
    
    draw.text((price_bg_x + 50, price_bg_y + 30), "£4.99", fill=(255, 255, 255), font=font_large)
    
    # Instant download badge
    badge_x = 100
    badge_y = 150
    draw.rectangle([badge_x, badge_y, badge_x + 500, badge_y + 100],
                   fill=(76, 175, 80), outline=(255, 255, 255), width=4)
    
    draw.text((badge_x + 50, badge_y + 25), "INSTANT DIGITAL DOWNLOAD", 
              fill=(255, 255, 255), font=font_medium)
    
    # RecoveriStudio branding
    draw.text((WIDTH - 400, HEIGHT - 80), "RecoveriStudio", fill=ACCENT1, font=font_medium)
    draw.text((WIDTH - 400, HEIGHT - 150), "studio@recoveri.io", fill=TEXT_COLOR, font=font_small)
    
    # Save image
    output_path = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/party-planner/mockup.png"
    img.save(output_path, "PNG", quality=95)
    
    print(f"✓ Mockup created: {output_path}")
    print(f"✓ Size: {WIDTH}x{HEIGHT}px (Etsy recommended)")
    print(f"✓ Format: PNG")
    print(f"✓ File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    print(f"✓ Features: Product preview, price tag, instant download badge")
    print(f"✓ Branding: RecoveriStudio footer")

if __name__ == "__main__":
    create_mockup()