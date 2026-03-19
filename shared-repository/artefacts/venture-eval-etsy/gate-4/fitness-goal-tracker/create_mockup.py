#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# Color palette from skill
COLORS = {
    'background': '#F5F0EB',
    'text': '#2C2C2C',
    'accent': '#8B7355',
    'light': '#D4C5B2'
}

def hex_to_rgb(hex_code):
    """Convert hex color to RGB tuple"""
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def create_mockup_image(output_path):
    """Create Etsy listing mockup image"""
    # Etsy recommended size: 2700x2025px
    width, height = 2700, 2025
    
    # Create base image
    bg_color = hex_to_rgb(COLORS['background'])
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Add decorative elements
    accent_color = hex_to_rgb(COLORS['accent'])
    light_color = hex_to_rgb(COLORS['light'])
    text_color = hex_to_rgb(COLORS['text'])
    
    # Draw background pattern (subtle dots)
    dot_spacing = 80
    dot_size = 3
    for x in range(dot_spacing, width, dot_spacing):
        for y in range(dot_spacing, height, dot_spacing):
            draw.ellipse([x-dot_size, y-dot_size, x+dot_size, y+dot_size], 
                        fill=light_color, outline=None)
    
    # Create "product preview" area
    preview_width = 1800
    preview_height = 1200
    preview_x = (width - preview_width) // 2
    preview_y = 200
    
    # Draw product preview background (simulating a printed page)
    draw.rectangle([preview_x, preview_y, 
                   preview_x + preview_width, preview_y + preview_height], 
                  fill=(255, 255, 255), outline=accent_color, width=8)
    
    # Add shadow effect
    shadow_offset = 15
    draw.rectangle([preview_x + shadow_offset, preview_y + shadow_offset,
                   preview_x + preview_width + shadow_offset, 
                   preview_y + preview_height + shadow_offset],
                  fill=(220, 220, 220))
    
    # Draw the "product" inside (simplified version)
    product_padding = 100
    product_inner_x = preview_x + product_padding
    product_inner_y = preview_y + product_padding
    product_inner_width = preview_width - 2 * product_padding
    product_inner_height = preview_height - 2 * product_padding
    
    # Draw product cover
    draw.rectangle([product_inner_x, product_inner_y,
                   product_inner_x + product_inner_width,
                   product_inner_y + product_inner_height],
                  fill=bg_color, outline=light_color, width=4)
    
    # Add product title on the "cover"
    try:
        # Try to use a nice font, fall back to default
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Draw main title
    title = "FITNESS GOAL TRACKER"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    
    title_x = product_inner_x + (product_inner_width - title_width) // 2
    title_y = product_inner_y + 150
    
    draw.text((title_x, title_y), title, fill=accent_color, font=title_font)
    
    # Draw subtitle
    subtitle = "Printable PDF | Workout Planner | Exercise Journal"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    
    subtitle_x = product_inner_x + (product_inner_width - subtitle_width) // 2
    subtitle_y = title_y + title_height + 40
    
    draw.text((subtitle_x, subtitle_y), subtitle, fill=text_color, font=subtitle_font)
    
    # Draw feature bullets
    features = [
        "✓ Goal Setting & Planning",
        "✓ Weekly Workout Planner", 
        "✓ Exercise Log & Progress Tracker",
        "✓ Habit Tracker & Nutrition Notes",
        "✓ Motivational Quotes & Guidance"
    ]
    
    feature_y = subtitle_y + 120
    feature_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36) if os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf") else ImageFont.load_default()
    
    for i, feature in enumerate(features):
        feature_x = product_inner_x + 100
        draw.text((feature_x, feature_y + i * 70), feature, fill=text_color, font=feature_font)
    
    # Draw "pages" on the side (simulating a multi-page product)
    for i in range(5):
        page_offset = 20 * (i + 1)
        page_x = product_inner_x + product_inner_width - page_offset
        page_y = product_inner_y + page_offset
        
        draw.rectangle([page_x, page_y,
                       page_x + product_inner_width - 200,
                       page_y + product_inner_height - 200],
                      fill=(250, 250, 250), outline=light_color, width=2)
    
    # Add main title text overlay
    main_title = "FITNESS GOAL TRACKER\nPrintable PDF"
    try:
        main_title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 96)
    except:
        main_title_font = ImageFont.load_default()
    
    # Calculate title position (above product preview)
    title_lines = main_title.split('\n')
    line_height = 100
    total_title_height = len(title_lines) * line_height
    
    title_start_y = preview_y - total_title_height - 50
    
    for i, line in enumerate(title_lines):
        line_bbox = draw.textbbox((0, 0), line, font=main_title_font)
        line_width = line_bbox[2] - line_bbox[0]
        line_x = (width - line_width) // 2
        line_y = title_start_y + i * line_height
        
        # Draw text with shadow
        draw.text((line_x + 4, line_y + 4), line, fill=(200, 200, 200), font=main_title_font)
        draw.text((line_x, line_y), line, fill=accent_color, font=main_title_font)
    
    # Add price tag
    price_bg_x = width - 400
    price_bg_y = 100
    price_bg_width = 350
    price_bg_height = 120
    
    # Draw price tag background
    draw.rounded_rectangle([price_bg_x, price_bg_y,
                           price_bg_x + price_bg_width,
                           price_bg_y + price_bg_height],
                          radius=20, fill=accent_color)
    
    # Draw price text
    price_text = "£4.49"
    try:
        price_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
    except:
        price_font = ImageFont.load_default()
    
    price_bbox = draw.textbbox((0, 0), price_text, font=price_font)
    price_width = price_bbox[2] - price_bbox[0]
    price_height = price_bbox[3] - price_bbox[1]
    
    price_x = price_bg_x + (price_bg_width - price_width) // 2
    price_y = price_bg_y + (price_bg_height - price_height) // 2
    
    draw.text((price_x, price_y), price_text, fill=(255, 255, 255), font=price_font)
    
    # Add "Digital Download" badge
    badge_x = 100
    badge_y = 100
    badge_width = 400
    badge_height = 80
    
    draw.rounded_rectangle([badge_x, badge_y,
                           badge_x + badge_width,
                           badge_y + badge_height],
                          radius=15, fill=light_color)
    
    badge_text = "INSTANT DIGITAL DOWNLOAD"
    try:
        badge_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    except:
        badge_font = ImageFont.load_default()
    
    badge_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    badge_text_width = badge_bbox[2] - badge_bbox[0]
    badge_text_height = badge_bbox[3] - badge_bbox[1]
    
    badge_text_x = badge_x + (badge_width - badge_text_width) // 2
    badge_text_y = badge_y + (badge_height - badge_text_height) // 2
    
    draw.text((badge_text_x, badge_text_y), badge_text, fill=text_color, font=badge_font)
    
    # Add brand footer
    footer_text = "RecoveriStudio • studio@recoveri.io"
    try:
        footer_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        footer_font = ImageFont.load_default()
    
    footer_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    
    footer_x = (width - footer_width) // 2
    footer_y = height - 80
    
    draw.text((footer_x, footer_y), footer_text, fill=light_color, font=footer_font)
    
    # Save the image
    image.save(output_path, 'PNG', quality=95)
    print(f"Mockup image created successfully: {output_path}")

if __name__ == "__main__":
    output_dir = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/fitness-goal-tracker"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "mockup.png")
    create_mockup_image(output_path)