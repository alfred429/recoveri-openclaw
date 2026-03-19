#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# Colors from the skill
COLORS = {
    'background': (245, 240, 235),  # #F5F0EB
    'text_dark': (44, 44, 44),      # #2C2C2C
    'accent': (139, 115, 85),       # #8B7355
    'light_accent': (212, 197, 178) # #D4C5B2
}

def create_mockup_image(output_path):
    """Create mockup image for Etsy listing"""
    # Create image with Etsy recommended size
    width, height = 2700, 2025
    image = Image.new('RGB', (width, height), color=COLORS['background'])
    draw = ImageDraw.Draw(image)
    
    # Add a subtle texture or gradient background
    for y in range(0, height, 10):
        alpha = int(255 * (0.9 + 0.1 * (y / height)))
        color = (
            int(COLORS['background'][0] * (0.95 + 0.05 * (y / height))),
            int(COLORS['background'][1] * (0.95 + 0.05 * (y / height))),
            int(COLORS['background'][2] * (0.95 + 0.05 * (y / height)))
        )
        draw.rectangle([(0, y), (width, y + 10)], fill=color)
    
    # Create a "product" representation (simulated PDF pages)
    # Main product display area
    product_width, product_height = 1200, 1600
    product_x, product_y = (width - product_width) // 2, (height - product_height) // 2
    
    # Draw product background (simulated paper)
    draw.rectangle(
        [(product_x, product_y), (product_x + product_width, product_y + product_height)],
        fill=(255, 255, 255),
        outline=COLORS['light_accent'],
        width=10
    )
    
    # Add shadow effect
    shadow_offset = 20
    draw.rectangle(
        [(product_x + shadow_offset, product_y + shadow_offset), 
         (product_x + product_width + shadow_offset, product_y + product_height + shadow_offset)],
        fill=(220, 215, 200)
    )
    
    # Draw the product rectangle again on top
    draw.rectangle(
        [(product_x, product_y), (product_x + product_width, product_y + product_height)],
        fill=(255, 255, 255),
        outline=COLORS['light_accent'],
        width=10
    )
    
    # Add "page" lines to simulate a worksheet
    line_spacing = 40
    for i in range(1, 15):
        y = product_y + 100 + (i * line_spacing)
        if i % 5 == 0:  # Thicker line every 5 lines
            draw.line([(product_x + 100, y), (product_x + product_width - 100, y)], 
                     fill=COLORS['accent'], width=3)
        else:
            draw.line([(product_x + 100, y), (product_x + product_width - 100, y)], 
                     fill=COLORS['light_accent'], width=1)
    
    # Add section headers on the "worksheet"
    sections = ["VISION BOARD", "ANNUAL GOALS", "QUARTERLY PLAN", "MONTHLY TRACKER"]
    for i, section in enumerate(sections):
        y = product_y + 120 + (i * 120)
        # Section background
        draw.rectangle(
            [(product_x + 120, y - 15), (product_x + 400, y + 35)],
            fill=COLORS['light_accent']
        )
        # Section text
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        draw.text((product_x + 130, y), section, fill=COLORS['text_dark'], font=font)
    
    # Add checkboxes
    for i in range(4):
        y = product_y + 300 + (i * 80)
        draw.rectangle(
            [(product_x + product_width - 200, y), (product_x + product_width - 170, y + 30)],
            outline=COLORS['accent'],
            width=2
        )
    
    # Add product title overlay at the top
    title_bg_height = 200
    draw.rectangle(
        [(0, 50), (width, 50 + title_bg_height)],
        fill=COLORS['accent']
    )
    
    # Add title text
    try:
        title_font = ImageFont.truetype("arial.ttf", 80)
        subtitle_font = ImageFont.truetype("arial.ttf", 40)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Main title
    title = "Goal Setting Worksheet"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 80), title, fill=(255, 255, 255), font=title_font)
    
    # Subtitle
    subtitle = "SMART Goals Planner | Printable PDF | Personal Development"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, 170), subtitle, fill=COLORS['light_accent'], font=subtitle_font)
    
    # Add branding at the bottom
    branding_height = 100
    draw.rectangle(
        [(0, height - branding_height), (width, height)],
        fill=COLORS['text_dark']
    )
    
    try:
        branding_font = ImageFont.truetype("arial.ttf", 30)
    except:
        branding_font = ImageFont.load_default()
    
    branding_text = "RecoveriStudio | Digital Download | Instant Access"
    branding_bbox = draw.textbbox((0, 0), branding_text, font=branding_font)
    branding_width = branding_bbox[2] - branding_bbox[0]
    branding_x = (width - branding_width) // 2
    draw.text((branding_x, height - 70), branding_text, fill=COLORS['background'], font=branding_font)
    
    # Add price tag in the corner
    price_bg_size = 180
    price_x, price_y = width - price_bg_size - 50, 50
    draw.ellipse(
        [(price_x, price_y), (price_x + price_bg_size, price_y + price_bg_size)],
        fill=COLORS['accent'],
        outline=(255, 255, 255),
        width=5
    )
    
    try:
        price_font = ImageFont.truetype("arial.ttf", 50)
        currency_font = ImageFont.truetype("arial.ttf", 30)
    except:
        price_font = ImageFont.load_default()
        currency_font = ImageFont.load_default()
    
    price_text = "£4.49"
    price_bbox = draw.textbbox((0, 0), price_text, font=price_font)
    price_text_width = price_bbox[2] - price_bbox[0]
    price_text_x = price_x + (price_bg_size - price_text_width) // 2
    draw.text((price_text_x, price_y + 40), price_text, fill=(255, 255, 255), font=price_font)
    
    # Save the image
    image.save(output_path, 'PNG', quality=95)
    print(f"Mockup image created successfully: {output_path}")
    
    # Print image details
    print(f"Image size: {image.size}")
    print(f"Image mode: {image.mode}")

if __name__ == "__main__":
    output_dir = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/goal-setting-worksheet"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "mockup.png")
    create_mockup_image(output_path)