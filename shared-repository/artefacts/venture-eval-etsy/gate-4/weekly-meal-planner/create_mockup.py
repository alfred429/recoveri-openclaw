#!/usr/bin/env python3
"""
Create Etsy mockup image for Weekly Meal Planner
Size: 2700x2025px (Etsy recommended)
Show product on clean background with title overlay
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import os

# Color palette
COLORS = {
    'background': (245, 240, 235),  # #F5F0EB
    'text_dark': (44, 44, 44),      # #2C2C2C
    'accent': (139, 115, 85),       # #8B7355
    'light_accent': (212, 197, 178), # #D4C5B2
    'white': (255, 255, 255)
}

def create_mockup(output_path):
    """Create Etsy mockup image"""
    
    # Create blank image
    width, height = 2700, 2025
    image = Image.new('RGB', (width, height), COLORS['background'])
    draw = ImageDraw.Draw(image)
    
    # Add subtle texture/noise
    import random
    for _ in range(50000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        r, g, b = COLORS['background']
        # Add slight variation
        r = min(255, max(0, r + random.randint(-5, 5)))
        g = min(255, max(0, g + random.randint(-5, 5)))
        b = min(255, max(0, b + random.randint(-5, 5)))
        draw.point((x, y), fill=(r, g, b))
    
    # Create "paper" background for product
    paper_width, paper_height = 1800, 1350
    paper_x = (width - paper_width) // 2
    paper_y = (height - paper_height) // 2 - 100
    
    # Draw paper with shadow
    shadow_offset = 20
    draw.rectangle(
        [paper_x + shadow_offset, paper_y + shadow_offset, 
         paper_x + paper_width + shadow_offset, paper_y + paper_height + shadow_offset],
        fill=(220, 215, 210)
    )
    
    # Draw paper
    draw.rectangle(
        [paper_x, paper_y, paper_x + paper_width, paper_y + paper_height],
        fill=COLORS['white']
    )
    
    # Add paper texture
    for _ in range(20000):
        x = random.randint(paper_x, paper_x + paper_width - 1)
        y = random.randint(paper_y, paper_y + paper_height - 1)
        if random.random() < 0.1:  # 10% chance
            r, g, b = COLORS['white']
            r = min(255, max(0, r + random.randint(-3, 3)))
            g = min(255, max(0, g + random.randint(-3, 3)))
            b = min(255, max(0, b + random.randint(-3, 3)))
            draw.point((x, y), fill=(r, g, b))
    
    # Draw "PDF pages" on the paper
    page_count = 8
    page_width = paper_width - 100
    page_height = paper_height - 100
    page_x = paper_x + 50
    page_y = paper_y + 50
    
    for i in range(min(4, page_count)):  # Show up to 4 pages stacked
        offset = i * 15
        page_color = (250 - i*5, 250 - i*5, 250 - i*5)
        
        # Page shadow
        draw.rectangle(
            [page_x + offset + 5, page_y + offset + 5,
             page_x + offset + page_width + 5, page_y + offset + page_height + 5],
            fill=(230, 230, 230)
        )
        
        # Page
        draw.rectangle(
            [page_x + offset, page_y + offset,
             page_x + offset + page_width, page_y + offset + page_height],
            fill=page_color
        )
        
        # Page content preview
        if i == 0:  # Front page
            # Title on page
            try:
                font_large = ImageFont.truetype("arial.ttf", 72)
                font_medium = ImageFont.truetype("arial.ttf", 48)
                font_small = ImageFont.truetype("arial.ttf", 36)
            except:
                # Fallback to default font
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Draw title
            title = "Weekly Meal Planner"
            title_bbox = draw.textbbox((0, 0), title, font=font_large)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = page_x + offset + (page_width - title_width) // 2
            title_y = page_y + offset + 150
            draw.text((title_x, title_y), title, fill=COLORS['accent'], font=font_large)
            
            # Draw subtitle
            subtitle = "Simplify Your Meal Planning"
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = page_x + offset + (page_width - subtitle_width) // 2
            subtitle_y = title_y + 100
            draw.text((subtitle_x, subtitle_y), subtitle, fill=COLORS['text_dark'], font=font_medium)
            
            # Draw sample content
            content_y = subtitle_y + 150
            sample_lines = [
                "• Weekly meal planning spread",
                "• Grocery shopping list",
                "• Recipe ideas page",
                "• Nutrition tracking",
                "• 8-page printable PDF"
            ]
            
            for line in sample_lines:
                draw.text((page_x + offset + 100, content_y), line, fill=COLORS['text_dark'], font=font_small)
                content_y += 60
    
    # Add product title overlay at top
    try:
        font_title = ImageFont.truetype("arial.ttf", 120)
        font_subtitle = ImageFont.truetype("arial.ttf", 60)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
    
    # Title background
    title_bg_height = 300
    draw.rectangle(
        [0, 50, width, 50 + title_bg_height],
        fill=COLORS['accent']
    )
    
    # Main title
    main_title = "Weekly Meal Planner"
    main_bbox = draw.textbbox((0, 0), main_title, font=font_title)
    main_width = main_bbox[2] - main_bbox[0]
    main_x = (width - main_width) // 2
    main_y = 100
    draw.text((main_x, main_y), main_title, fill=COLORS['white'], font=font_title)
    
    # Subtitle
    subtitle = "Printable PDF | A4 Size | Instant Download"
    sub_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    sub_width = sub_bbox[2] - sub_bbox[0]
    sub_x = (width - sub_width) // 2
    sub_y = main_y + 140
    draw.text((sub_x, sub_y), subtitle, fill=COLORS['light_accent'], font=font_subtitle)
    
    # Add RecoveriStudio branding at bottom
    branding_y = height - 100
    draw.text(
        (width // 2 - 200, branding_y),
        "RecoveriStudio",
        fill=COLORS['text_dark'],
        font=font_subtitle
    )
    
    # Add price tag
    price_bg_width, price_bg_height = 400, 120
    price_bg_x = width - price_bg_width - 100
    price_bg_y = 100
    
    # Price background with rounded corners (simulated)
    draw.rectangle(
        [price_bg_x, price_bg_y, price_bg_x + price_bg_width, price_bg_y + price_bg_height],
        fill=COLORS['text_dark']
    )
    
    # Price text
    price_text = "£3.99"
    try:
        font_price = ImageFont.truetype("arial.ttf", 80)
    except:
        font_price = ImageFont.load_default()
    
    price_bbox = draw.textbbox((0, 0), price_text, font=font_price)
    price_width = price_bbox[2] - price_bbox[0]
    price_x = price_bg_x + (price_bg_width - price_width) // 2
    price_y = price_bg_y + (price_bg_height - 80) // 2
    draw.text((price_x, price_y), price_text, fill=COLORS['white'], font=font_price)
    
    # Save image
    image.save(output_path, 'PNG', quality=95)
    print(f"Mockup image saved to: {output_path}")
    print(f"Dimensions: {width}x{height}px")

if __name__ == "__main__":
    output_file = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/weekly-meal-planner/mockup.png"
    print(f"Creating Etsy mockup image at: {output_file}")
    create_mockup(output_file)