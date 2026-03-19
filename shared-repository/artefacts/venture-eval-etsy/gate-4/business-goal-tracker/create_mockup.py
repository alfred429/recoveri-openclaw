#!/usr/bin/env python3
"""
Business Goal Tracker Mockup Generator
Creates Etsy listing thumbnail (2700x2025px)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# Color palette from RecoveriStudio brand guidelines
COLORS = {
    'background': '#F5F0EB',  # Soft beige
    'dark': '#2C2C2C',        # Dark charcoal
    'accent': '#8B7355',      # Warm brown
    'light': '#D4C5B2',       # Light tan
    'highlight': '#4A6FA5',   # Professional blue
}

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_mockup_image(output_path):
    """Create Etsy mockup image (2700x2025px)"""
    
    # Create blank image
    width, height = 2700, 2025
    image = Image.new('RGB', (width, height), hex_to_rgb(COLORS['background']))
    draw = ImageDraw.Draw(image)
    
    # Add subtle texture/noise
    import random
    for _ in range(5000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        r, g, b = hex_to_rgb(COLORS['background'])
        # Add slight variation
        r = min(255, max(0, r + random.randint(-5, 5)))
        g = min(255, max(0, g + random.randint(-5, 5)))
        b = min(255, max(0, b + random.randint(-5, 5)))
        draw.point((x, y), fill=(r, g, b))
    
    # Create "paper" background for product display
    paper_width, paper_height = 1800, 1350
    paper_x = (width - paper_width) // 2
    paper_y = (height - paper_height) // 2 - 100
    
    # Draw paper with shadow
    shadow_offset = 15
    draw.rectangle(
        [paper_x + shadow_offset, paper_y + shadow_offset,
         paper_x + paper_width + shadow_offset, paper_y + paper_height + shadow_offset],
        fill=hex_to_rgb('#D0C8B8')
    )
    
    # Draw paper
    draw.rectangle(
        [paper_x, paper_y, paper_x + paper_width, paper_y + paper_height],
        fill=hex_to_rgb('#FFFFFF')
    )
    
    # Add paper texture
    for _ in range(2000):
        x = random.randint(paper_x, paper_x + paper_width - 1)
        y = random.randint(paper_y, paper_y + paper_height - 1)
        if random.random() < 0.1:  # 10% chance
            r, g, b = 240, 240, 240
            draw.point((x, y), fill=(r, g, b))
    
    # Draw "PDF pages" on the paper
    page_spacing = 20
    num_pages = 8
    page_width = paper_width - 100
    page_height = paper_height - 100
    
    for i in range(num_pages):
        page_x = paper_x + 50 + (i * page_spacing)
        page_y = paper_y + 50 + (i * page_spacing)
        
        # Page shadow
        draw.rectangle(
            [page_x + 3, page_y + 3, page_x + page_width + 3, page_y + page_height + 3],
            fill=hex_to_rgb('#E8E4DD')
        )
        
        # Page
        page_color = (255, 255, 255) if i == num_pages - 1 else (248, 248, 248)
        draw.rectangle(
            [page_x, page_y, page_x + page_width, page_y + page_height],
            fill=page_color
        )
        
        # Page edge
        draw.rectangle(
            [page_x + page_width - 5, page_y, page_x + page_width, page_y + page_height],
            fill=hex_to_rgb('#F0F0F0')
        )
        
        # Add some content to the front page
        if i == num_pages - 1:
            # Title on front page
            try:
                # Try to load a font
                font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
                font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
                font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            except:
                # Fallback to default font
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Draw title
            title = "Business Goal Tracker"
            title_bbox = draw.textbbox((0, 0), title, font=font_large)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = page_x + (page_width - title_width) // 2
            title_y = page_y + 150
            
            draw.text((title_x, title_y), title, fill=hex_to_rgb(COLORS['dark']), font=font_large)
            
            # Draw subtitle
            subtitle = "Strategic Planning & Progress Tracking"
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = page_x + (page_width - subtitle_width) // 2
            subtitle_y = title_y + 90
            
            draw.text((subtitle_x, subtitle_y), subtitle, fill=hex_to_rgb(COLORS['accent']), font=font_medium)
            
            # Draw feature list
            features = [
                "• Annual Business Vision",
                "• Quarterly Goal Breakdown",
                "• Monthly Action Planning",
                "• KPI Tracking",
                "• Resource Allocation",
                "• Progress Review"
            ]
            
            feature_y = subtitle_y + 120
            for feature in features:
                draw.text((page_x + 100, feature_y), feature, fill=hex_to_rgb(COLORS['dark']), font=font_small)
                feature_y += 50
    
    # Add main title text overlay
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
    
    # Main title
    main_title = "Business Goal Tracker"
    title_bbox = draw.textbbox((0, 0), main_title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = paper_y + paper_height + 100
    
    # Text shadow
    draw.text((title_x + 4, title_y + 4), main_title, fill=hex_to_rgb('#888888'), font=font_title)
    # Main text
    draw.text((title_x, title_y), main_title, fill=hex_to_rgb(COLORS['dark']), font=font_title)
    
    # Subtitle
    subtitle = "Professional PDF Template | Strategic Planning"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 130
    
    draw.text((subtitle_x, subtitle_y), subtitle, fill=hex_to_rgb(COLORS['accent']), font=font_subtitle)
    
    # Add RecoveriStudio branding
    branding = "RecoveriStudio"
    try:
        font_brand = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
    except:
        font_brand = ImageFont.load_default()
    
    brand_bbox = draw.textbbox((0, 0), branding, font=font_brand)
    brand_width = brand_bbox[2] - brand_bbox[0]
    brand_x = (width - brand_width) // 2
    brand_y = height - 80
    
    draw.text((brand_x, brand_y), branding, fill=hex_to_rgb(COLORS['highlight']), font=font_brand)
    
    # Add tagline
    tagline = "Digital Product | Instant Download"
    tagline_bbox = draw.textbbox((0, 0), tagline, font=font_brand)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    tagline_x = (width - tagline_width) // 2
    tagline_y = brand_y + 50
    
    draw.text((tagline_x, tagline_y), tagline, fill=hex_to_rgb(COLORS['accent']), font=font_brand)
    
    # Save image
    image.save(output_path, 'PNG', quality=95)
    print(f"Mockup image created successfully: {output_path}")
    
    # Also create a smaller version for quick preview
    preview = image.resize((900, 675), Image.Resampling.LANCZOS)
    preview_path = output_path.replace('.png', '_preview.png')
    preview.save(preview_path, 'PNG', quality=90)
    print(f"Preview image created: {preview_path}")

if __name__ == "__main__":
    output_file = "mockup.png"
    create_mockup_image(output_file)