#!/usr/bin/env python3
"""
Create Etsy mockup image for Wedding Budget Planner.
Size: 2700x2025px (Etsy recommended)
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create blank image
width, height = 2700, 2025
image = Image.new('RGB', (width, height), color='#F5F0EB')  # Background color
draw = ImageDraw.Draw(image)

# Colors from RecoveriStudio palette
colors = {
    'accent': '#8B7355',
    'text_dark': '#2C2C2C',
    'light_accent': '#D4C5B2',
}

# Try to load a font, fall back to default
try:
    # Try to use a nice font if available
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 70)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
except:
    # Fall back to default font
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Draw title
title = "Wedding Budget Planner"
title_bbox = draw.textbbox((0, 0), title, font=font_large)
title_width = title_bbox[2] - title_bbox[0]
title_x = (width - title_width) // 2
draw.text((title_x, 300), title, fill=colors['accent'], font=font_large)

# Draw subtitle
subtitle = "Printable PDF | Financial Planning Template"
subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (width - subtitle_width) // 2
draw.text((subtitle_x, 450), subtitle, fill=colors['text_dark'], font=font_medium)

# Draw "PDF Preview" box
box_width, box_height = 1800, 1000
box_x = (width - box_width) // 2
box_y = 650

# Draw box with shadow effect
shadow_offset = 15
draw.rectangle(
    [box_x + shadow_offset, box_y + shadow_offset, 
     box_x + box_width + shadow_offset, box_y + box_height + shadow_offset],
    fill='#D4C5B2'
)

# Main box
draw.rectangle(
    [box_x, box_y, box_x + box_width, box_y + box_height],
    fill='white',
    outline=colors['accent'],
    width=8
)

# Draw PDF preview content inside box
# Title inside PDF
pdf_title = "Wedding Budget Planner"
pdf_title_bbox = draw.textbbox((0, 0), pdf_title, font=font_medium)
pdf_title_width = pdf_title_bbox[2] - pdf_title_bbox[0]
pdf_title_x = box_x + (box_width - pdf_title_width) // 2
draw.text((pdf_title_x, box_y + 80), pdf_title, fill=colors['accent'], font=font_medium)

# Draw sample content lines
line_y = box_y + 200
for i in range(1, 8):
    # Draw bullet point
    draw.ellipse([box_x + 100, line_y - 15, box_x + 130, line_y + 15], fill=colors['light_accent'])
    
    # Draw line text
    line_text = f"Sample content line {i} for wedding budget planning"
    draw.text((box_x + 150, line_y - 25), line_text, fill=colors['text_dark'], font=font_small)
    
    # Draw line
    draw.line([box_x + 100, line_y + 40, box_x + box_width - 100, line_y + 40], fill='#E8DFD6', width=2)
    
    line_y += 100

# Draw features
features = [
    "✓ 12-page printable PDF",
    "✓ Budget tracking worksheets", 
    "✓ Vendor comparison tables",
    "✓ Payment schedule tracker",
    "✓ Guest list & RSVP manager",
    "✓ Honeymoon budget planner"
]

features_x = box_x + 100
features_y = box_y + box_height - 300

for i, feature in enumerate(features):
    draw.text((features_x, features_y + i*70), feature, fill=colors['accent'], font=font_small)

# Draw price tag
price_box_width, price_box_height = 400, 120
price_box_x = width - price_box_width - 150
price_box_y = 150

draw.rectangle(
    [price_box_x, price_box_y, price_box_x + price_box_width, price_box_y + price_box_height],
    fill=colors['accent'],
    outline=colors['text_dark'],
    width=4
)

draw.text(
    (price_box_x + 20, price_box_y + 20), 
    "Only", 
    fill='white', 
    font=font_small
)

draw.text(
    (price_box_x + 100, price_box_y + 50), 
    "£5.49", 
    fill='white', 
    font=font_large
)

# Draw footer
footer = "RecoveriStudio | Digital Download | Instant Access"
footer_bbox = draw.textbbox((0, 0), footer, font=font_small)
footer_width = footer_bbox[2] - footer_bbox[0]
footer_x = (width - footer_width) // 2
draw.text((footer_x, height - 100), footer, fill=colors['text_dark'], font=font_small)

# Save image
output_path = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/wedding-budget-planner/mockup.png"
image.save(output_path, 'PNG', quality=95)
print(f"Mockup created: {output_path}")
print(f"Image size: {image.size}")