#!/usr/bin/env python3
"""
Create mockup image for Home Cleaning Planner Etsy listing.
Size: 2700x2025px (Etsy recommended)
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Color palette
COLORS = {
    'background': '#F5F0EB',
    'dark_text': '#2C2C2C',
    'accent': '#8B7355',
    'light_accent': '#D4C5B2',
    'white': '#FFFFFF'
}

def create_mockup():
    """Create Etsy listing mockup image."""
    
    # Create blank image
    width, height = 2700, 2025
    image = Image.new('RGB', (width, height), COLORS['background'])
    draw = ImageDraw.Draw(image)
    
    # Try to load a font (use default if not available)
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 70)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
    except:
        # Use default font if specific font not found
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Draw title
    title = "Home Cleaning Planner"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = 200
    
    draw.text((title_x, title_y), title, fill=COLORS['dark_text'], font=title_font)
    
    # Draw subtitle
    subtitle = "Printable PDF | Organize Your Cleaning Routine"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 150
    
    draw.text((subtitle_x, subtitle_y), subtitle, fill=COLORS['accent'], font=subtitle_font)
    
    # Draw product preview box
    box_width = 1800
    box_height = 1000
    box_x = (width - box_width) // 2
    box_y = subtitle_y + 150
    
    # Draw box with shadow effect
    shadow_offset = 15
    draw.rectangle(
        [box_x + shadow_offset, box_y + shadow_offset, 
         box_x + box_width + shadow_offset, box_y + box_height + shadow_offset],
        fill=COLORS['light_accent']
    )
    
    # Main box
    draw.rectangle(
        [box_x, box_y, box_x + box_width, box_y + box_height],
        fill=COLORS['white'],
        outline=COLORS['accent'],
        width=10
    )
    
    # Draw sample content inside box
    content_y = box_y + 80
    
    # Draw sample page titles
    page_titles = [
        "Daily Cleaning Checklist",
        "Weekly Cleaning Schedule", 
        "Monthly Deep Cleaning Planner",
        "Room-by-Room Cleaning Guide",
        "Cleaning Supplies Inventory",
        "Seasonal Cleaning Checklist",
        "Custom Cleaning Template"
    ]
    
    for i, page_title in enumerate(page_titles):
        y_pos = content_y + (i * 120)
        
        # Draw checkbox
        checkbox_x = box_x + 100
        checkbox_size = 40
        draw.rectangle(
            [checkbox_x, y_pos, checkbox_x + checkbox_size, y_pos + checkbox_size],
            outline=COLORS['accent'],
            width=3
        )
        
        # Draw page title
        text_x = checkbox_x + checkbox_size + 40
        draw.text((text_x, y_pos), page_title, fill=COLORS['dark_text'], font=text_font)
    
    # Draw features at bottom
    features_y = box_y + box_height + 100
    features = [
        "✓ 8 Printable Pages",
        "✓ A4 Size (210x297mm)",
        "✓ Instant Digital Download",
        "✓ Clean, Modern Design"
    ]
    
    for i, feature in enumerate(features):
        x_pos = box_x + (i * 450)
        if x_pos + 400 > box_x + box_width:
            break
        draw.text((x_pos, features_y), feature, fill=COLORS['dark_text'], font=text_font)
    
    # Draw brand footer
    footer = "RecoveriStudio"
    footer_bbox = draw.textbbox((0, 0), footer, font=subtitle_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    footer_x = (width - footer_width) // 2
    footer_y = height - 150
    
    draw.text((footer_x, footer_y), footer, fill=COLORS['accent'], font=subtitle_font)
    
    # Save image
    output_path = "mockup.png"
    image.save(output_path, 'PNG', quality=95)
    print(f"Mockup created: {output_path}")
    print(f"Size: {width}x{height}px")
    
    return output_path

if __name__ == "__main__":
    create_mockup()