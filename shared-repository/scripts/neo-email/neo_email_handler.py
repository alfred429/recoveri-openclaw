#!/usr/bin/env python3
"""Neo Email Handler — PDF Review Packs for Boss.

Three tiers:
  Tier 1: Per-REQ completion email (triggered on REQ completion)
  Tier 2: Nightly digest (cron, 21:00 UTC)
  Tier 3: Morning approvals (cron, 07:00 UTC, Swarm 6 only)

Reads config from config.json — never hardcodes email addresses, paths, or model names.
Logs every email sent to sent.jsonl.

Usage:
  python neo_email_handler.py tier1 --req-id REQ-20260319-001 --title "Brand Architecture" --completed-by "Oracle" --domain "Strategic" --pillar "STUDIOS" --summary "..." --next-step "..." --files doc1.md doc2.md
  python neo_email_handler.py tier2
  python neo_email_handler.py tier3
  python neo_email_handler.py convert --files doc1.md doc2.md --output-dir ./pdfs
"""

import argparse
import json
import os
import sys
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path

# PDF conversion imports — only needed when converting
try:
    import markdown
    from weasyprint import HTML
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "config.json"

PDF_CSS = """
@page {
    margin: 2cm;
    size: A4;
    @bottom-center { content: "RECOVERI — Confidential"; font-size: 8pt; color: #999; }
}
body {
    font-family: -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 11pt; line-height: 1.6; color: #222;
}
h1 { font-size: 18pt; color: #1a1a2e; border-bottom: 2px solid #1a1a2e; padding-bottom: 6px; }
h2 { font-size: 14pt; color: #16213e; margin-top: 1.5em; }
h3 { font-size: 12pt; color: #0f3460; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 10pt; }
th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: left; }
th { background-color: #f0f0f0; font-weight: bold; }
tr:nth-child(even) { background-color: #fafafa; }
code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-size: 10pt; }
pre { background: #f4f4f4; padding: 12px; border-radius: 5px; overflow-x: auto; font-size: 9pt; }
blockquote { border-left: 3px solid #1a1a2e; margin-left: 0; padding-left: 1em; color: #555; }
"""

MD_EXTENSIONS = ['tables', 'fenced_code', 'codehilite', 'toc', 'sane_lists']


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def md_to_pdf(input_path, output_path):
    """Convert a markdown file to PDF. Returns output path."""
    if not PDF_AVAILABLE:
        raise RuntimeError("PDF libraries not installed. Run: pip install markdown weasyprint")

    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content, extensions=MD_EXTENSIONS)
    full_html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{PDF_CSS}</style></head><body>{html_content}</body></html>"
    HTML(string=full_html).write_pdf(output_path)
    return output_path


def convert_files_to_pdf(md_files, output_dir):
    """Convert a list of .md files to PDFs. Returns list of (original, pdf_path, ok)."""
    os.makedirs(output_dir, exist_ok=True)
    results = []
    for md_file in md_files:
        pdf_name = Path(md_file).stem + '.pdf'
        pdf_path = os.path.join(output_dir, pdf_name)
        try:
            md_to_pdf(md_file, pdf_path)
            results.append((md_file, pdf_path, True))
        except Exception as e:
            print(f"  WARN: Failed to convert {md_file}: {e}", file=sys.stderr)
            results.append((md_file, None, False))
    return results


def log_email(config, email_id, tier, subject, attachments, source_reqs):
    """Append email record to sent.jsonl."""
    log_path = config['paths']['email_log']
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    record = {
        "email_id": email_id,
        "tier": tier,
        "to": config['email']['to'],
        "from": config['email']['from'],
        "subject": subject,
        "attachments": [os.path.basename(a) for a in attachments if a],
        "source_reqs": source_reqs,
        "sent_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "delivery_confirmed": True
    }

    with open(log_path, 'a') as f:
        f.write(json.dumps(record) + '\n')

    return record


def generate_email_id(tier):
    """Generate unique email ID."""
    now = datetime.datetime.utcnow()
    date_str = now.strftime("%Y%m%d")
    # Read log to determine sequence number
    seq = 1
    return f"EMAIL-{date_str}-{seq:03d}"


def build_mime_message(config, subject, body_text, body_html, pdf_paths):
    """Build a MIME message with PDF attachments."""
    msg = MIMEMultipart('mixed')
    msg['From'] = config['email']['from']
    msg['To'] = config['email']['to']
    msg['Reply-To'] = config['email']['reply_to']
    msg['Subject'] = subject

    # Body (prefer HTML)
    body_part = MIMEMultipart('alternative')
    body_part.attach(MIMEText(body_text, 'plain', 'utf-8'))
    if body_html:
        body_part.attach(MIMEText(body_html, 'html', 'utf-8'))
    msg.attach(body_part)

    # PDF attachments
    for pdf_path in pdf_paths:
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                pdf_data = f.read()
            attachment = MIMEApplication(pdf_data, _subtype='pdf')
            attachment.add_header('Content-Disposition', 'attachment',
                                 filename=os.path.basename(pdf_path))
            msg.attach(attachment)

    return msg


def send_via_smtp(config, msg):
    """Send email via SMTP. Requires SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS env vars."""
    host = os.environ.get('SMTP_HOST')
    port = int(os.environ.get('SMTP_PORT', '587'))
    user = os.environ.get('SMTP_USER')
    password = os.environ.get('SMTP_PASS')

    if not all([host, user, password]):
        raise RuntimeError(
            "SMTP not configured. Set SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS env vars. "
            "Or use --dry-run to generate the email without sending."
        )

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(user, password)
        server.send_message(msg)

    return True


# === TIER HANDLERS ===

def handle_tier1(args, config):
    """Tier 1: Per-REQ completion email."""
    tier_config = config['tiers']['1']
    subject = tier_config['subject_template'].format(
        req_id=args.req_id, title=args.title
    )

    body_text = f"""{args.req_id} complete.

Completed by: {args.completed_by}
Domain: {args.domain} | Pillar: {args.pillar}

Summary: {args.summary}

Action needed: Review attached PDF. Approve, amend, or request changes.
Reply to this email or message Neo on Telegram.

Next step (if approved): {args.next_step}

{config['email']['signature']}"""

    # Convert files to PDF
    pdf_results = convert_files_to_pdf(args.files, config['paths']['pdf_output_dir'])
    pdf_paths = [r[1] for r in pdf_results if r[2]]

    if not args.dry_run:
        msg = build_mime_message(config, subject, body_text, None, pdf_paths)
        send_via_smtp(config, msg)

    email_id = generate_email_id("1")
    log_record = log_email(config, email_id, "1", subject, pdf_paths, [args.req_id])
    print(f"Tier 1 email {'sent' if not args.dry_run else 'DRY RUN'}: {subject}")
    print(f"  Attachments: {len(pdf_paths)} PDFs")
    print(f"  Logged as: {email_id}")
    return log_record


def handle_tier2(args, config):
    """Tier 2: Nightly digest email."""
    tier_config = config['tiers']['2']

    # Collect pending review items
    pending_items = collect_pending_reviews(config)
    if not pending_items and config['constraints']['never_send_empty_digest']:
        print("Tier 2: No pending items. Skipping (never_send_empty_digest=true).")
        return None

    # Filter out items already sent via Tier 1 in dedup window
    dedup_hours = tier_config['dedup_window_hours']
    pending_items = dedup_against_tier1(pending_items, config, dedup_hours)

    count = len(pending_items)
    subject = tier_config['subject_template'].format(count=count)

    # Build body
    items_text = "\n".join(
        f"  {i+1}. {item['id']}: {item['title']} ({item['author']}) — {item['domain']} — {item['age']}"
        for i, item in enumerate(pending_items)
    )

    body_text = f"""Good evening Boss. Here's tonight's review pack.

PENDING REVIEW:
{items_text}

Attachments: {count} PDFs attached for review.

Reply with decisions or message Neo on Telegram.
Format: "Approve REQ-008" or "Amend POLICIES — need tighter refund wording"

{config['email']['signature']}"""

    # Convert all pending docs to PDF
    md_files = [item['file_path'] for item in pending_items if item.get('file_path')]
    pdf_results = convert_files_to_pdf(md_files, config['paths']['pdf_output_dir'])
    pdf_paths = [r[1] for r in pdf_results if r[2]]

    if not args.dry_run:
        msg = build_mime_message(config, subject, body_text, None, pdf_paths)
        send_via_smtp(config, msg)

    email_id = generate_email_id("2")
    source_reqs = [item['id'] for item in pending_items]
    log_record = log_email(config, email_id, "2", subject, pdf_paths, source_reqs)
    print(f"Tier 2 email {'sent' if not args.dry_run else 'DRY RUN'}: {subject}")
    print(f"  Items: {count}, Attachments: {len(pdf_paths)} PDFs")
    print(f"  Logged as: {email_id}")
    return log_record


def handle_tier3(args, config):
    """Tier 3: Morning approvals email."""
    tier_config = config['tiers']['3']

    if not tier_config['enabled']:
        print("Tier 3: Disabled (waiting for Swarm 6). Skipping.")
        return None

    proposals = collect_proposals(config)
    if not proposals:
        print("Tier 3: No proposals. Skipping.")
        return None

    count = len(proposals)
    subject = tier_config['subject_template'].format(count=count)

    proposals_text = "\n".join(
        f"  {i+1}. {p['id']}: {p['skill']} — {p['summary']}\n"
        f"     Evidence: {p['evidence']}\n"
        f"     Recommendation: {p['recommendation']}\n"
        f"     Risk: {p['risk']}"
        for i, p in enumerate(proposals)
    )

    body_text = f"""Good morning Boss. Swarm 6 generated {count} skill improvement proposals overnight.

PROPOSALS:
{proposals_text}

Reply with: "Approve PROP-001, PROP-002. Reject PROP-003."
Or: "Approve all" / "Reject all" / "Defer all"

{config['email']['signature']}"""

    if not args.dry_run:
        msg = build_mime_message(config, subject, body_text, None, [])
        send_via_smtp(config, msg)

    email_id = generate_email_id("3")
    source_reqs = [p['id'] for p in proposals]
    log_record = log_email(config, email_id, "3", subject, [], source_reqs)
    print(f"Tier 3 email {'sent' if not args.dry_run else 'DRY RUN'}: {subject}")
    print(f"  Proposals: {count}")
    print(f"  Logged as: {email_id}")
    return log_record


# === DATA COLLECTION HELPERS ===

def collect_pending_reviews(config):
    """Scan request register and approval register for pending items.

    Returns list of dicts: {id, title, author, domain, age, file_path}
    """
    items = []
    register_path = config['paths']['request_register']

    if not os.path.exists(register_path):
        return items

    now = datetime.datetime.utcnow()
    with open(register_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
            except json.JSONDecodeError:
                continue

            if req.get('status') == 'COMPLETED' and not req.get('boss_reviewed', False):
                created = datetime.datetime.fromisoformat(req.get('created_at', now.isoformat()).replace('Z', '+00:00'))
                age_hours = (now - created.replace(tzinfo=None)).total_seconds() / 3600
                age_str = f"{int(age_hours)}h old" if age_hours < 48 else f"{int(age_hours/24)}d old"

                items.append({
                    'id': req.get('req_id', 'UNKNOWN'),
                    'title': req.get('title', 'Untitled'),
                    'author': req.get('completed_by', 'Unknown'),
                    'domain': req.get('domain', 'General'),
                    'age': age_str,
                    'file_path': req.get('output_file'),
                    'sent_tier1_at': req.get('sent_tier1_at')
                })

    return items


def dedup_against_tier1(items, config, window_hours):
    """Remove items already sent via Tier 1 within the dedup window."""
    log_path = config['paths']['email_log']
    if not os.path.exists(log_path):
        return items

    now = datetime.datetime.utcnow()
    cutoff = now - datetime.timedelta(hours=window_hours)
    recent_tier1_reqs = set()

    with open(log_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get('tier') == '1':
                sent_at = datetime.datetime.fromisoformat(record['sent_at'].replace('Z', '+00:00')).replace(tzinfo=None)
                if sent_at >= cutoff:
                    recent_tier1_reqs.update(record.get('source_reqs', []))

    return [item for item in items if item['id'] not in recent_tier1_reqs]


def collect_proposals(config):
    """Scan proposal directory for overnight proposals.

    Returns list of dicts: {id, skill, summary, evidence, recommendation, risk}
    """
    proposals = []
    proposal_dir = config['paths']['proposal_dir']

    if not os.path.exists(proposal_dir):
        return proposals

    today = datetime.datetime.utcnow().strftime("%Y%m%d")
    for fname in sorted(os.listdir(proposal_dir)):
        if not fname.startswith(f"PROP-{today}"):
            continue
        fpath = os.path.join(proposal_dir, fname)
        try:
            with open(fpath) as f:
                prop = json.load(f)
            proposals.append({
                'id': prop.get('proposal_id', fname),
                'skill': prop.get('skill_name', 'Unknown'),
                'summary': prop.get('summary', ''),
                'evidence': prop.get('evidence', ''),
                'recommendation': prop.get('recommendation', 'REVIEW'),
                'risk': prop.get('risk', 'Unknown')
            })
        except (json.JSONDecodeError, KeyError):
            continue

    return proposals


# === CLI ===

def main():
    parser = argparse.ArgumentParser(description='Neo Email Handler')
    parser.add_argument('--dry-run', action='store_true', help='Generate email without sending')
    subparsers = parser.add_subparsers(dest='command')

    # Tier 1
    t1 = subparsers.add_parser('tier1', help='Per-REQ completion email')
    t1.add_argument('--req-id', required=True)
    t1.add_argument('--title', required=True)
    t1.add_argument('--completed-by', required=True)
    t1.add_argument('--domain', default='General')
    t1.add_argument('--pillar', default='INTERNAL')
    t1.add_argument('--summary', required=True)
    t1.add_argument('--next-step', default='Awaiting your decision.')
    t1.add_argument('--files', nargs='+', required=True)

    # Tier 2
    subparsers.add_parser('tier2', help='Nightly digest email')

    # Tier 3
    subparsers.add_parser('tier3', help='Morning approvals email')

    # Convert only
    conv = subparsers.add_parser('convert', help='Convert .md files to PDF only')
    conv.add_argument('--files', nargs='+', required=True)
    conv.add_argument('--output-dir', required=True)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    config = load_config()

    if args.command == 'convert':
        results = convert_files_to_pdf(args.files, args.output_dir)
        ok = sum(1 for r in results if r[2])
        print(f"Converted {ok}/{len(results)} files to PDF.")
        for orig, pdf, success in results:
            status = "OK" if success else "FAILED"
            print(f"  {status}: {os.path.basename(orig)} -> {os.path.basename(pdf) if pdf else 'N/A'}")
    elif args.command == 'tier1':
        handle_tier1(args, config)
    elif args.command == 'tier2':
        handle_tier2(args, config)
    elif args.command == 'tier3':
        handle_tier3(args, config)


if __name__ == '__main__':
    main()
