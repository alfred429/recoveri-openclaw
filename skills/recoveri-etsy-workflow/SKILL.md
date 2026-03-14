# RecoveriStudio Etsy Product Workflow

Read this skill when creating digital products for the RecoveriStudio Etsy shop.

## Shop Details
- Shop: RecoveriStudio on Etsy
- Brand: Clean, modern, professional. Neutral tones. Minimalist aesthetic.
- Email: studio@recoveri.io
- Product types: PDF planners, templates, wall art prints, budget trackers, checklists

## Workflow (follow in order)

### Step 1: Alpha (CRO) — Research & Listing Copy
1. Research trending Etsy digital products using web search
2. Pick ONE product to create — favour evergreen demand over seasonal
3. Write the complete Etsy listing:
   - Title (max 140 chars, front-load keywords)
   - Description (benefit-led, 300-500 words, include dimensions and what's included)
   - 13 tags (max 20 chars each, long-tail keywords)
   - Price (use Data's pricing research: planners £3-5, bundles £8-15, premium £15-25)
   - Category recommendation
4. Save listing copy to: ~/.openclaw/workspaces/cro-agent/etsy-products/[product-name]/listing.md

### Step 2: Data (CTO) — Create the Product
1. Read Alpha's listing.md for the product spec
2. Create the PDF using Python (reportlab or fpdf2)
3. Design rules:
   - A4 size (210x297mm)
   - Clean fonts: Helvetica or Arial
   - Colour palette: soft neutrals (#F5F0EB, #2C2C2C, #8B7355, #D4C5B2)
   - Include "RecoveriStudio" small footer on each page
   - High quality — this is a paid product
4. Save product to: ~/.openclaw/workspaces/cto-agent/etsy-products/[product-name]/product.pdf

### Step 3: Data (CTO) — Create Mockup Image
1. Create a listing thumbnail using Pillow (PIL)
2. Size: 2700x2025px (Etsy recommended)
3. Show the product on a clean background
4. Include product title text overlay
5. Save to: ~/.openclaw/workspaces/cto-agent/etsy-products/[product-name]/mockup.png

### Step 4: Alpha (CRO) — Email for Review
1. Compile: listing.md + product.pdf + mockup.png
2. Email to mike@recoveri.io with subject: "RecoveriStudio Review: [Product Name]"
3. Use gog: gog gmail send --to mike@recoveri.io --subject "..." --body "..." --attach file1 --attach file2
4. Wait for Boss approval before creating next product

### Step 5: Boss — Review and Upload
Boss reviews email, approves or requests changes. Upload to Etsy is manual.

## Pricing Rules (from Data's research)
- Always calculate backward from desired profit after Etsy fees
- Etsy fees: £0.16 listing + 6.5% transaction + payment processing
- Minimum viable price: £2.99 (below this, fees eat too much)
- Sweet spots: £3.49 single items, £7.99 small bundles, £14.99 premium packs
- Always offer a bundle option alongside singles

## Product Output Directory
All product files go in: ~/.openclaw/workspaces/[agent]/etsy-products/[product-name]/
Create the directory if it doesn't exist.

## Quality Checklist (before emailing Boss)
- [ ] PDF opens correctly and all pages render
- [ ] No placeholder text left in the product
- [ ] RecoveriStudio footer on every page
- [ ] Mockup image is 2700x2025px
- [ ] Listing has exactly 13 tags
- [ ] Price is set using the pricing rules above
