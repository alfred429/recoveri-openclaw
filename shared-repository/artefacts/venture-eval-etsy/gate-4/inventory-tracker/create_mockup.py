#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

def create_mockup_image(output_path):
    """Create a mockup image for the Home Inventory Tracker"""
    
    # Create a blank image (2700x2025px as per Etsy recommendation)
    width, height = 2700, 2025
    image = Image.new('RGB', (width, height), color='#F5F0EB')  # Light beige background
    draw = ImageDraw.Draw(image)
    
    # Define colors
    primary_color = (44, 44, 44)      # #2C2C2C - Dark gray
    accent_color = (139, 115, 85)     # #8B7355 - Brown
    border_color = (212, 197, 178)    # #D4C5B2 - Light brown
    white = (255, 255, 255)
    
    # Try to load fonts, fall back to default if not available
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 70)
        body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Create a "paper" background for the product
    paper_width, paper_height = 1800, 1200
    paper_x = (width - paper_width) // 2
    paper_y = (height - paper_height) // 2 - 100
    
    # Draw paper with shadow
    shadow_offset = 20
    draw.rectangle(
        [paper_x + shadow_offset, paper_y + shadow_offset, 
         paper_x + paper_width + shadow_offset, paper_y + paper_height + shadow_offset],
        fill=(220, 215, 205)
    )
    
    # Draw paper
    draw.rectangle(
        [paper_x, paper_y, paper_x + paper_width, paper_y + paper_height],
        fill=white,
        outline=border_color,
        width=10
    )
    
    # Add "pages" effect
    for i in range(1, 6):
        page_offset = i * 8
        draw.rectangle(
            [paper_x + page_offset, paper_y + page_offset, 
             paper_x + paper_width - page_offset, paper_y + paper_height - page_offset],
            outline=(240, 240, 240),
            width=2
        )
    
    # Add title to the paper
    title = "Home Inventory Tracker"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = paper_x + (paper_width - title_width) // 2
    title_y = paper_y + 100
    
    draw.text((title_x, title_y), title, fill=primary_color, font=title_font)
    
    # Add subtitle
    subtitle = "Printable PDF Organizer"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = paper_x + (paper_width - subtitle_width) // 2
    subtitle_y = title_y + 150
    
    draw.text((subtitle_x, subtitle_y), subtitle, fill=accent_color, font=subtitle_font)
    
    # Add feature list
    features = [
        "✓ Room-by-room inventory sheets",
        "✓ Insurance documentation pages",
        "✓ Maintenance schedule tracker",
        "✓ Value calculation summary",
        "✓ Emergency contacts section",
        "✓ Clean, printable A4 format"
    ]
    
    feature_y = subtitle_y + 150
    for feature in features:
        draw.text((paper_x + 150, feature_y), feature, fill=primary_color, font=body_font)
        feature_y += 90
    
    # Add page count
    page_count = "12-Page Printable PDF"
    page_bbox = draw.textbbox((0, 0), page_count, font=body_font)
    page_width = page_bbox[2] - page_bbox[0]
    page_x = paper_x + (paper_width - page_width) // 2
    page_y = feature_y + 50
    
    draw.rectangle(
        [page_x - 30, page_y - 20, page_x + page_width + 30, page_y + 70],
        fill=accent_color,
        outline=primary_color,
        width=3
    )
    draw.text((page_x, page_y), page_count, fill=white, font=body_font)
    
    # Add price tag
    price_tag_width, price_tag_height = 400, 150
    price_tag_x = paper_x + paper_width - price_tag_width - 100
    price_tag_y = paper_y + 100
    
    # Draw price tag background
    draw.rounded_rectangle(
        [price_tag_x, price_tag_y, price_tag_x + price_tag_width, price_tag_y + price_tag_height],
        radius=30,
        fill=primary_color,
        outline=accent_color,
        width=5
    )
    
    # Add price
    price = "£4.99"
    price_bbox = draw.textbbox((0, 0), price, font=title_font)
    price_width = price_bbox[2] - price_bbox[0]
    price_x = price_tag_x + (price_tag_width - price_width) // 2
    price_y = price_tag_y + (price_tag_height - 120) // 2
    
    draw.text((price_x, price_y), price, fill=white, font=title_font)
    
    # Add "Instant Digital Download"
    download_text = "Instant Digital Download"
    download_bbox = draw.textbbox((0, 0), download_text, font=small_font)
    download_width = download_bbox[2] - download_bbox[0]
    download_x = price_tag_x + (price_tag_width - download_width) // 2
    download_y = price_y + 120
    
    draw.text((download_x, download_y), download_text, fill=border_color, font=small_font)
    
    # Add branding at bottom
    branding = "RecoveriStudio | Digital Product"
    branding_bbox = draw.textbbox((0, 0), branding, font=small_font)
    branding_width = branding_bbox[2] - branding_bbox[0]
    branding_x = (width - branding_width) // 2
    branding_y = height - 80
    
    draw.text((branding_x, branding_y), branding, fill=border_color, font=small_font)
    
    # Add decorative elements
    # Left decorative line
    draw.line([(100, height//2 - 300), (100, height//2 + 300)], fill=accent_color, width=8)
    draw.line([(110, height//2 - 290), (110, height//2 + 290)], fill=border_color, width=4)
    
    # Right decorative line
    draw.line([(width - 100, height//2 - 300), (width - 100, height//2 + 300)], fill=accent_color, width=8)
    draw.line([(width - 110, height//2 - 290), (width - 110, height//2 + 290)], fill=border_color, width=4)
    
    # Save the image
    image.save(output_path, 'PNG', quality=95)
    print(f"Mockup image created successfully: {output_path}")
    
    # Print image info
    print(f"Image size: {width}x{height}px")
    print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")

if __name__ == "__main__":
    output_path = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/inventory-tracker/mockup.png"
    create_mockup_image(output_path)