def create_debt_tracker_page(c):
    """Create debt payoff tracker page"""
    draw_header(c, "Debt Payoff Plan")
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 40, "Choose snowball (smallest first) or avalanche (highest interest first) method.")
    
    # Debt table
    debt_data = [
        ["Creditor", "Balance", "Interest %", "Min Payment", "Target Payoff"],
        ["Credit Card", "£__________", "____%", "£______", "___/___/____"],
        ["Student Loan", "£__________", "____%", "£______", "___/___/____"],
        ["Car Loan", "£__________", "____%", "£______", "___/___/____"],
        ["Personal Loan", "£__________", "____%", "£______", "___/___/____"],
        ["Other", "£__________", "____%", "£______", "___/___/____"],
        ["TOTAL DEBT", "£__________", "", "£__________", ""]
    ]
    
    debt_table = Table(debt_data, colWidths=[CONTENT_WIDTH * 0.22, CONTENT_WIDTH * 0.18, CONTENT_WIDTH * 0.15, CONTENT_WIDTH * 0.18, CONTENT_WIDTH * 0.27])
    debt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 6), (-1, 6), COLOR_SECONDARY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 6), (-1, 6), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_SECONDARY),
    ]))
    
    debt_table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    debt_table.drawOn(c, MARGIN, PAGE_HEIGHT - MARGIN - 150)
    
    # Payoff strategy
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 200, "Payoff Strategy:")
    
    strategies = [
        "☐ Snowball Method: Pay minimums on all, extra on smallest balance",
        "☐ Avalanche Method: Pay minimums on all, extra on highest interest",
        "☐ Custom: _________________________________________________"
    ]
    
    y_pos = PAGE_HEIGHT - MARGIN - 220
    for strategy in strategies:
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN, y_pos, strategy)
        y_pos -= 20
    
    # Monthly payment plan
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y_pos - 20, "Monthly Extra Payment: £__________")
    c.drawString(MARGIN, y_pos - 40, "Estimated Payoff Date: ___/___/____")

def create_bill_calendar_page(c):
    """Create bill payment calendar page"""
    draw_header(c, "Bill Payment Calendar")
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 40, "Mark due dates and check off when paid. Avoid late fees!")
    
    # Calendar grid (4 weeks)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    data = [["Week", "Bill", "Amount", "Due Date", "Paid ✓", "Notes"]]
    
    for week in range(4):
        for i in range(3):  # 3 bills per week max
            data.append([f"Week {week+1}", "__________", "£______", "___", "[ ]", "__________"])
    
    bill_table = Table(data, colWidths=[CONTENT_WIDTH * 0.12, CONTENT_WIDTH * 0.25, CONTENT_WIDTH * 0.15, CONTENT_WIDTH * 0.12, CONTENT_WIDTH * 0.12, CONTENT_WIDTH * 0.24])
    bill_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_SECONDARY),
        ('BACKGROUND', (0, 1), (-1, 4), COLOR_LIGHT),
        ('BACKGROUND', (0, 5), (-1, 8), colors.HexColor('#F8F8F8')),
        ('BACKGROUND', (0, 9), (-1, 12), COLOR_LIGHT),
    ]))
    
    bill_table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    bill_table.drawOn(c, MARGIN, PAGE_HEIGHT - MARGIN - 250)
    
    # Recurring subscriptions
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 320, "Recurring Subscriptions:")
    
    subs = ["Netflix", "Spotify", "Amazon Prime", "Gym", "Software", "Other"]
    y_pos = PAGE_HEIGHT - MARGIN - 340
    for i, sub in enumerate(subs):
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN + (i % 3) * 140, y_pos - (i // 3) * 20, f"{sub}: £__________/mo")

def create_financial_review_page(c):
    """Create monthly financial review page"""
    draw_header(c, "Monthly Financial Review")
    
    # Review questions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 40, "End-of-Month Reflection")
    
    questions = [
        "1. Did I stay within my budget this month? What went well?",
        "________________________________________________________________",
        "________________________________________________________________",
        "",
        "2. Where did I overspend? Why?",
        "________________________________________________________________",
        "________________________________________________________________",
        "",
        "3. What unexpected expenses came up?",
        "________________________________________________________________",
        "________________________________________________________________",
        "",
        "4. Did I meet my savings goals? If not, what prevented me?",
        "________________________________________________________________",
        "________________________________________________________________",
        "",
        "5. What will I do differently next month?",
        "________________________________________________________________",
        "________________________________________________________________"
    ]
    
    y_pos = PAGE_HEIGHT - MARGIN - 70
    for question in questions:
        if question.startswith("1.") or question.startswith("2.") or question.startswith("3.") or question.startswith("4.") or question.startswith("5."):
            c.setFont("Helvetica-Bold", 10)
        elif question == "":
            y_pos -= 10
            continue
        else:
            c.setFont("Helvetica", 9)
        
        c.drawString(MARGIN, y_pos, question)
        y_pos -= 15
    
    # Action items
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y_pos - 30, "Action Items for Next Month:")
    
    for i in range(4):
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN, y_pos - 50 - (i * 15), f"{i+1}. [ ] _________________________________________")

def create_net_worth_page(c):
    """Create net worth tracker page"""
    draw_header(c, "Net Worth Tracker")
    
    # Instructions
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 40, "Track your net worth quarterly. Assets minus liabilities.")
    
    # Assets section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 70, "Assets (What You Own)")
    
    assets = [
        ["Cash & Bank Accounts", "Q1", "Q2", "Q3", "Q4"],
        ["Savings Accounts", "£__________", "£__________", "£__________", "£__________"],
        ["Investment Accounts", "£__________", "£__________", "£__________", "£__________"],
        ["Retirement Funds", "£__________", "£__________", "£__________", "£__________"],
        ["Real Estate", "£__________", "£__________", "£__________", "£__________"],
        ["Vehicles", "£__________", "£__________", "£__________", "£__________"],
        ["Other Assets", "£__________", "£__________", "£__________", "£__________"],
        ["TOTAL ASSETS", "£__________", "£__________", "£__________", "£__________"]
    ]
    
    assets_table = Table(assets, colWidths=[CONTENT_WIDTH * 0.35] + [CONTENT_WIDTH * 0.16] * 4)
    assets_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 7), (-1, 7), COLOR_SECONDARY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 7), (-1, 7), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_SECONDARY),
    ]))
    
    assets_table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    assets_table.drawOn(c, MARGIN, PAGE_HEIGHT - MARGIN - 200)
    
    # Liabilities section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 280, "Liabilities (What You Owe)")
    
    liabilities = [
        ["Mortgage", "£__________", "£__________", "£__________", "£__________"],
        ["Car Loans", "£__________", "£__________", "£__________", "£__________"],
        ["Student Loans", "£__________", "£__________", "£__________", "£__________"],
        ["Credit Cards", "£__________", "£__________", "£__________", "£__________"],
        ["Personal Loans", "£__________", "£__________", "£__________", "£__________"],
        ["Other Debts", "£__________", "£__________", "£__________", "£__________"],
        ["TOTAL LIABILITIES", "£__________", "£__________", "£__________", "£__________"]
    ]
    
    liab_table = Table(liabilities, colWidths=[CONTENT_WIDTH * 0.35] + [CONTENT_WIDTH * 0.16] * 4)
    liab_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 6), (-1, 6), COLOR_SECONDARY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 6), (-1, 6), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_SECONDARY),
    ]))
    
    liab_table.wrapOn(c, CONTENT_WIDTH, PAGE_HEIGHT)
    liab_table.drawOn(c, MARGIN, PAGE_HEIGHT - MARGIN - 380)
    
    # Net worth calculation
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 420, "Net Worth Calculation:")
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN + 50, PAGE_HEIGHT - MARGIN - 440, "Q1: Assets £__________ - Liabilities £__________ = Net Worth £__________")
    c.drawString(MARGIN + 50, PAGE_HEIGHT - MARGIN - 455, "Q2: Assets £__________ - Liabilities £__________ = Net Worth £__________")
    c.drawString(MARGIN + 50, PAGE_HEIGHT - MARGIN - 470, "Q3: Assets £__________ - Liabilities £__________ = Net Worth £__________")
    c.drawString(MARGIN + 50, PAGE_HEIGHT - MARGIN - 485, "Q4: Assets £__________ - Liabilities £__________ = Net Worth £__________")

def main():
    """Main function to create the PDF"""
    output_path = "/root/shared-repository/artefacts/venture-eval-etsy/gate-4/monthly-budget-planner/product.pdf"
    
    # Create canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    
    # Set metadata
    c.setTitle("Monthly Budget Planner - RecoveriStudio")
    c.setAuthor("RecoveriStudio")
    c.setSubject("Personal Finance Tracker")
    
    # Create pages
    pages = [
        (create_title_page, "Title"),
        (create_annual_goals_page, "Annual Goals"),
        (lambda c: create_monthly_budget_page(c, "January"), "January Budget"),
        (lambda c: create_monthly_budget_page(c, "February"), "February Budget"),
        (create_expense_tracker_page, "Expense Tracker"),
        (create_savings_tracker_page, "Savings Tracker"),
        (create_debt_tracker_page, "Debt Payoff"),
        (create_bill_calendar_page, "Bill Calendar"),
        (create_financial_review_page, "Financial Review"),
        (create_net_worth_page, "Net Worth Tracker")
    ]
    
    # Generate each page
    for i, (page_func, title) in enumerate(pages):
        page_func(c)
        draw_footer(c, i + 1)
        c.showPage()
    
    # Save PDF
    c.save()
    print(f"PDF created successfully: {output_path}")
    print(f"Total pages: {len(pages)}")

if __name__ == "__main__":
    main()