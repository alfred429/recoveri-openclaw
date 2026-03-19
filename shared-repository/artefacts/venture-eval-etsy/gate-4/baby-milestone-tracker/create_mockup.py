#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

def create_mockup():
    """Create Etsy mockup image for Baby Milestone Tracker"""
    
    # Dimensions (Etsy recommended)
    width, height = 2700, 2025
    
    # Create blank image with background color
    bg_color = (245, 240, 235)  # #F5F0EB
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Define colors
    text_color = (44, 44, 44)  # #2C2C2C
    accent_color = (139, 115, 85)  # #8B7355
    light_accent = (212, 197, 178)  # #D4C5B2
    
    # Try to load a font, fall back to default
    try:
        # Try different font paths
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf"
        ]
        
        title_font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                title_font = ImageFont.truetype(font_path, 120)
                break
        
        if title_font is None:
            # Use default font
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
        else:
            subtitle_font = ImageFont.truetype(font_path, 80)
            body_font = ImageFont.truetype(font_path, 60)
    except:
        # Fall back to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
    
    # Draw title
    title = "Baby Milestone Tracker"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 200), title, fill=accent_color, font=title_font)
    
    # Draw subtitle
    subtitle = "Digital Download - First Year Memories"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, 350), subtitle, fill=text_color, font=subtitle_font)
    
    # Draw product preview area
    preview_width = 1800
    preview_height = 1200
    preview_x = (width - preview_width) // 2
    preview_y = 500
    
    # Draw preview background (simulating pages)
    draw.rectangle(
        [preview_x, preview_y, preview_x + preview_width, preview_y + preview_height],
        fill=(255, 255, 255),
        outline=light_accent,
        width=10
    )
    
    # Draw sample pages inside preview
    page_spacing = 20
    num_pages = 3
    
    for i in range(num_pages):
        page_x = preview_x + 50 + (i * page_spacing)
        page_y = preview_y + 50 + (i * page_spacing)
        page_width = preview_width - 100 - ((num_pages - 1) * page_spacing)
        page_height = preview_height - 100 - ((num_pages - 1) * page_spacing)
        
        # Page background
        draw.rectangle(
            [page_x, page_y, page_x + page_width, page_y + page_height],
            fill=(255, 255, 255),
            outline=light_accent if i == num_pages - 1 else (230, 230, 230),
            width=3
        )
        
        # Draw page content (simplified)
        if i == 0:  # Cover page
            # Title on page
            cover_title = "Month 1"
            cover_bbox = draw.textbbox((0, 0), cover_title, font=subtitle_font)
            cover_width = cover_bbox[2] - cover_bbox[0]
            cover_x = page_x + (page_width - cover_width) // 2
            draw.text((cover_x, page_y + 100), cover_title, fill=accent_color, font=subtitle_font)
            
            # Milestone lines
            for line in range(5):
                line_y = page_y + 200 + (line * 40)
                draw.line([page_x + 50, line_y, page_x + page_width - 50, line_y], fill=light_accent, width=2)
        
        elif i == 1:  # Growth chart
            # Chart title
            draw.text((page_x + 100, page_y + 80), "Growth Chart", fill=accent_color, font=body_font)
            
            # Simple chart
            chart_x = page_x + 100
            chart_y = page_y + 150
            chart_width = page_width - 200
            chart_height = 300
            
            # Draw grid
            for grid_y in range(6):
                y = chart_y + (grid_y * (chart_height // 5))
                draw.line([chart_x, y, chart_x + chart_width, y], fill=(200, 200, 200), width=1)
            
            for grid_x in range(13):
                x = chart_x + (grid_x * (chart_width // 12))
                draw.line([x, chart_y, x, chart_y + chart_height], fill=(200, 200, 200), width=1)
        
        elif i == 2:  # Special moments
            draw.text((page_x + 100, page_y + 80), "Special Firsts", fill=accent_color, font=body_font)
            
            # Firsts list
            firsts = ["First Smile", "First Laugh", "First Steps"]
            for j, first in enumerate(firsts):
                draw.text((page_x + 120, page_y + 150 + (j * 60)), f"• {first}", fill=text_color, font=body_font)
    
    # Draw features list
    features_y = preview_y + preview_height + 100
    features = [
        "✓ 12 Monthly Tracker Pages",
        "✓ Growth Chart & Measurements",
        "✓ Special Firsts Cards",
        "✓ Memory Keeper Pages",
        "✓ A4 Size - Instant Download"
    ]
    
    for i, feature in enumerate(features):
        draw.text((preview_x + 100, features_y + (i * 80)), feature, fill=text_color, font=body_font)
    
    # Draw price
    price_text = "£4.49"
    price_bbox = draw.textbbox((0, 0), price_text, font=title_font)
    price_width = price_bbox[2] - price_bbox[0]
    price_x = width - preview_x - 100 - price_width
    draw.text((price_x, features_y), price_text, fill=accent_color, font=title_font)
    
    # Draw brand footer
    footer_text = "RecoveriStudio"
    footer_bbox = draw.textbbox((0, 0), footer_text, font=body_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    footer_x = (width - footer_width) // 2
    draw.text((footer_x, height - 100), footer_text, fill=light_accent, font=body_font)
    
    # Save image
    output_path = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/baby-milestone-tracker/mockup.png"
    image.save(output_path, 'PNG', quality=95)
    print(f"Mockup created successfully: {output_path}")
    
    return output_path

if __name__ == "__main__":
    create_mockup()