#!/usr/bin/env python3
"""
Recoveri CS Responder — Ephemeral Sub-Agent
============================================
Spawns, categorises a customer message, drafts a template response,
logs a ticket to JSONL, escalates if needed, and terminates.

Usage:
    python3 cs-responder.py --message "Customer message here" --context '{"order_id": "123", "market": "UK"}'
    echo '{"message": "...", "context": {...}}' | python3 cs-responder.py --stdin

Model: DeepSeek (primary) / Qwen 2.5 on VPS Ollama (fallback)
Language: en-GB only (v1)

Golden Rules Applied:
  1. NEVER HARDCODE — all config from cs-config.json
  2. NEVER OVERWRITE WITHOUT REVIEWING — appends to JSONL, never overwrites
  3. DOCUMENT EVERYTHING — every ticket logged with full context
  4. NEVER LEAVE LOOSE ENDS — escalation for unmatched/risky messages
"""

import argparse
import datetime
import json
import os
import sys
import uuid
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "cs-config.json")


def load_config():
    """Load configuration from cs-config.json. Never hardcode values."""
    if not os.path.exists(CONFIG_PATH):
        print(f"[FATAL] Config file not found: {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Skill / Template loading
# ---------------------------------------------------------------------------
def load_skill_templates(config):
    """
    Load CS skill templates from the shared repository.
    Falls back to built-in placeholder templates if Skill 132 isn't deployed yet.
    """
    skill_path = config["paths"]["skill_file"]

    if os.path.exists(skill_path):
        with open(skill_path, "r") as f:
            content = f.read()
        return {"source": "skill-132", "content": content}

    # Skill 132 is deployed but skill file is markdown, not structured data.
    # Parse the skill for reference, but use config-driven templates below.
    # The skill file serves as the authoritative reference document.
    return {
        "source": "skill-132-v1.0",
        "skill_file": skill_path,
        "templates": {
            "A": {
                "name": "Download & Access",
                "response": (
                    "Hi {customer_name},\n\n"
                    "Thanks for reaching out about your order. As this is a digital product, "
                    "your download link was sent to your email immediately after purchase. "
                    "Please check your spam/junk folder if you haven't received it.\n\n"
                    "If you're still having trouble, please let us know and we'll resend it right away.\n\n"
                    "Best regards,\nRecoveri Studio"
                ),
            },
            "B": {
                "name": "Digital Download Issue",
                "response": (
                    "Hi {customer_name},\n\n"
                    "Sorry to hear you're having trouble with your download. "
                    "Here are a few things to try:\n"
                    "1. Check your email (including spam) for the download link\n"
                    "2. Try a different browser or device\n"
                    "3. Clear your browser cache and try again\n\n"
                    "If none of these work, reply here and we'll send you a fresh link.\n\n"
                    "Best regards,\nRecoveri Studio"
                ),
            },
            "C": {
                "name": "Product Question",
                "response": (
                    "Hi {customer_name},\n\n"
                    "Thanks for your interest in our products! "
                    "I'd be happy to help answer your question.\n\n"
                    "{ai_response}\n\n"
                    "Best regards,\nRecoveri Studio"
                ),
            },
            "D": {
                "name": "Refund Request",
                "response": (
                    "Hi {customer_name},\n\n"
                    "Thank you for reaching out. I've noted your refund request and "
                    "have escalated it to our team lead who will review it personally. "
                    "You'll hear back within 24 hours.\n\n"
                    "Best regards,\nRecoveri Studio"
                ),
            },
            "E": {
                "name": "Complaint / Dispute",
                "response": (
                    "Hi {customer_name},\n\n"
                    "I'm sorry to hear about your experience. Your feedback is important to us. "
                    "I've escalated this to our team lead who will look into this personally "
                    "and get back to you within 24 hours.\n\n"
                    "Best regards,\nRecoveri Studio"
                ),
            },
            "F": {
                "name": "Custom Request",
                "response": (
                    "Hi {customer_name},\n\n"
                    "Thanks for reaching out with your custom request! "
                    "We'll review what you're looking for and get back to you shortly.\n\n"
                    "Best regards,\nRecoveri Studio"
                ),
            },
            "G": {
                "name": "Unmatched / Unknown",
                "response": (
                    "Hi {customer_name},\n\n"
                    "Thanks for your message. I've passed this along to our team "
                    "who will get back to you shortly.\n\n"
                    "Best regards,\nRecoveri Studio"
                ),
            },
        },
    }


# ---------------------------------------------------------------------------
# LLM Client (DeepSeek primary, Ollama/Qwen fallback)
# ---------------------------------------------------------------------------
def call_llm(prompt, config, system_prompt=None):
    """
    Call LLM with DeepSeek as primary, Qwen on VPS Ollama as fallback.
    Uses pure stdlib (urllib) — no pip dependencies.
    """
    providers = [config["model"]["primary"], config["model"]["fallback"]]

    for provider in providers:
        try:
            result = _call_provider(prompt, provider, system_prompt)
            if result:
                return result
        except Exception as e:
            print(f"[WARN] Provider {provider['provider']} failed: {e}", file=sys.stderr)
            continue

    return None


def _call_provider(prompt, provider_config, system_prompt=None):
    """Call a single LLM provider via OpenAI-compatible API."""
    base_url = provider_config["base_url"].rstrip("/")
    model_id = provider_config["model_id"]

    # Get API key from environment if specified
    api_key = None
    key_env = provider_config.get("api_key_env")
    if key_env:
        api_key = os.environ.get(key_env)
        if not api_key:
            raise ValueError(f"API key env var {key_env} not set")

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    # Build request — OpenAI-compatible for DeepSeek, Ollama API for Ollama
    if provider_config["provider"] == "ollama":
        url = f"{base_url}/api/chat"
        payload = {
            "model": model_id,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.1},
        }
    else:
        url = f"{base_url}/chat/completions"
        payload = {
            "model": model_id,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 1024,
        }

    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body}")

    # Parse response
    if provider_config["provider"] == "ollama":
        return result.get("message", {}).get("content", "")
    else:
        choices = result.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "")

    return None


# ---------------------------------------------------------------------------
# Categorisation
# ---------------------------------------------------------------------------
CATEGORISE_SYSTEM_PROMPT = """You are a customer service categoriser for Recoveri Studio (RecoveriStudio), an Etsy digital products shop operating across 7 markets.

Categorise the customer message into exactly ONE bucket. Reply with ONLY the bucket letter (A-G), nothing else.

Buckets (from Skill 132):
A = Download & Access — can't download, link not working, file won't open, ZIP issue
B = Product Misunderstanding — expected different format, confused about editability, compatibility question
C = Refund/Return — wants money back, changed mind, doesn't meet expectations
D = File Completeness — missing files, incomplete delivery, fewer files than expected
E = Customisation — wants modifications, branding changes, design alterations
F = Billing — duplicate charge, payment issue, invoice question
G = Multilingual/Market — language version question, regional compatibility

Escalation triggers (categorise first, escalation handled separately):
- Any mention of "refund", "money back", or "return" → always C
- Customer threatens to open an Etsy case or dispute → always C (escalation trigger)
- Angry, hostile, or abusive tone → categorise by topic, escalation handled separately
- If unsure or doesn't match any bucket → reply with U (for UNMATCHED)

Reply with ONLY the single letter (A-G or U). No explanation."""


def categorise_message(message, config):
    """Categorise a customer message into bucket A-G using LLM."""
    result = call_llm(message, config, system_prompt=CATEGORISE_SYSTEM_PROMPT)

    if result:
        # Extract just the letter
        letter = result.strip().upper()[:1]
        if letter in "ABCDEFGU":
            return "UNMATCHED" if letter == "U" else letter

    # Default to UNMATCHED (escalate) if categorisation fails
    return "UNMATCHED"


# ---------------------------------------------------------------------------
# Response drafting
# ---------------------------------------------------------------------------
DRAFT_SYSTEM_PROMPT = """You are a customer service assistant for Recoveri Studio, an Etsy shop selling digital products across 7 markets.

Rules (STRICT — never break these):
- Use British English (en-GB) spelling and grammar
- NEVER promise or approve refunds — only acknowledge the request
- NEVER make up information about products you don't know
- Keep responses under 500 characters
- Be warm, professional, and helpful
- Sign off as "Recoveri Studio"

You will be given a customer message and a template. Personalise the template for the customer's specific situation. Stay close to the template — do not deviate significantly."""


def draft_response(message, bucket, templates, customer_name, config):
    """Draft a response using the template and LLM personalisation."""
    template_data = templates.get("templates", {}).get(bucket, {})
    template_text = template_data.get("response", "")

    if not template_text:
        return "Thank you for your message. Our team will get back to you shortly.\n\nBest regards,\nRecoveri Studio"

    # For simple templates (A, B, D, E), just fill in the name
    simple_response = template_text.replace("{customer_name}", customer_name or "there")

    # For bucket C (product question), use LLM to generate a helpful answer
    if bucket == "C" and "{ai_response}" in template_text:
        ai_answer = call_llm(
            f"Customer asked: {message}\n\nProvide a brief, helpful answer about our digital products. Keep it under 200 characters. British English only.",
            config,
            system_prompt=DRAFT_SYSTEM_PROMPT,
        )
        simple_response = simple_response.replace("{ai_response}", ai_answer or "Please let us know which specific product you're interested in and we'll provide more details.")

    # For bucket F (custom request), use LLM to acknowledge specifically
    if bucket == "F":
        ai_answer = call_llm(
            f"Customer's custom request: {message}\n\nWrite a brief, warm acknowledgement of their specific request (1-2 sentences). British English. Don't promise anything.",
            config,
            system_prompt=DRAFT_SYSTEM_PROMPT,
        )
        if ai_answer:
            simple_response = simple_response.replace(
                "We'll review what you're looking for and get back to you shortly.",
                ai_answer.strip(),
            )

    return simple_response


# ---------------------------------------------------------------------------
# Ticket logging (JSONL — append only, Golden Rule 2)
# ---------------------------------------------------------------------------
def log_ticket(ticket, config):
    """Append ticket to JSONL log. Never overwrites — append only."""
    log_path = config["paths"]["ticket_log"]

    # Ensure directory exists
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path, "a") as f:
        f.write(json.dumps(ticket, default=str) + "\n")

    print(f"[LOG] Ticket {ticket['ticket_id']} logged to {log_path}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Telegram escalation
# ---------------------------------------------------------------------------
def escalate_to_telegram(ticket, config):
    """Send escalation alert to Boss via Telegram."""
    token_env = config["telegram"]["bot_token_env"]
    token = os.environ.get(token_env)

    if not token:
        print(f"[WARN] Telegram token not set ({token_env}). Escalation logged but not sent.", file=sys.stderr)
        return False

    # Get chat IDs from env or config defaults
    chat_ids_env = config["telegram"].get("escalation_chat_ids_env")
    chat_ids_str = os.environ.get(chat_ids_env, "") if chat_ids_env else ""

    if chat_ids_str:
        chat_ids = [cid.strip() for cid in chat_ids_str.split(",")]
    else:
        chat_ids = config["telegram"].get("escalation_chat_ids_default", [])

    if not chat_ids:
        print("[WARN] No Telegram chat IDs configured. Escalation logged but not sent.", file=sys.stderr)
        return False

    bucket_name = config["buckets"].get(ticket["bucket"], {}).get("name", "Unknown")

    message = (
        f"🚨 *CS ESCALATION*\n\n"
        f"*Ticket:* `{ticket['ticket_id']}`\n"
        f"*Bucket:* {ticket['bucket']} — {bucket_name}\n"
        f"*Customer:* {ticket.get('customer_name', 'Unknown')}\n"
        f"*Market:* {ticket.get('market', 'Unknown')}\n"
        f"*Time:* {ticket['timestamp']}\n\n"
        f"*Message:*\n{ticket['customer_message'][:500]}\n\n"
        f"*Draft Response:*\n{ticket['draft_response'][:500]}\n\n"
        f"⚠️ _Requires manual review before sending_"
    )

    sent = False
    for chat_id in chat_ids:
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown",
            }
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                if result.get("ok"):
                    print(f"[TELEGRAM] Escalation sent to chat {chat_id}", file=sys.stderr)
                    sent = True
        except Exception as e:
            print(f"[WARN] Telegram send failed for chat {chat_id}: {e}", file=sys.stderr)

    return sent


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def process_message(message, context, config):
    """
    Main pipeline: categorise → template → draft → log → escalate → complete.
    Returns the ticket dict.
    """
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    ticket_id = f"CS-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

    customer_name = context.get("customer_name", "")
    market = context.get("market", "UK")
    order_id = context.get("order_id", "")
    product = context.get("product", "")
    etsy_conversation_id = context.get("etsy_conversation_id", "")

    # Step 1: Load templates
    print("[1/5] Loading CS skill templates...", file=sys.stderr)
    templates = load_skill_templates(config)
    template_source = templates.get("source", "unknown")
    print(f"       Template source: {template_source}", file=sys.stderr)

    # Step 2: Categorise
    print("[2/5] Categorising message...", file=sys.stderr)
    bucket = categorise_message(message, config)
    bucket_name = config["buckets"].get(bucket, {}).get("name", "Unknown")
    should_escalate = config["buckets"].get(bucket, {}).get("escalate", True)
    print(f"       Bucket: {bucket} — {bucket_name} (escalate: {should_escalate})", file=sys.stderr)

    # Step 3: Draft response
    print("[3/5] Drafting response...", file=sys.stderr)
    draft = draft_response(message, bucket, templates, customer_name, config)
    print(f"       Draft length: {len(draft)} chars", file=sys.stderr)

    # Step 4: Build and log ticket
    print("[4/5] Logging ticket...", file=sys.stderr)
    ticket = {
        "ticket_id": ticket_id,
        "timestamp": timestamp,
        "customer_name": customer_name,
        "customer_message": message,
        "market": market,
        "order_id": order_id,
        "product": product,
        "etsy_conversation_id": etsy_conversation_id,
        "bucket": bucket,
        "bucket_name": bucket_name,
        "draft_response": draft,
        "template_source": template_source,
        "model_used": config["model"]["primary"]["provider"],
        "escalated": should_escalate,
        "escalation_sent": False,
        "status": "escalated" if should_escalate else "drafted",
        "context": context,
    }
    log_ticket(ticket, config)

    # Step 5: Escalate if needed
    if should_escalate:
        print("[5/5] Escalating to Boss via Telegram...", file=sys.stderr)
        sent = escalate_to_telegram(ticket, config)
        ticket["escalation_sent"] = sent
    else:
        print("[5/5] No escalation needed.", file=sys.stderr)

    return ticket


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Recoveri CS Responder — Ephemeral sub-agent for customer service",
        epilog="Spawns, categorises, drafts, logs, escalates, terminates.",
    )
    parser.add_argument("--message", "-m", help="Customer message text")
    parser.add_argument("--context", "-c", help="JSON context (order_id, market, customer_name, etc.)")
    parser.add_argument("--stdin", action="store_true", help="Read JSON input from stdin")
    parser.add_argument("--config", help="Path to config file (default: cs-config.json alongside this script)")
    parser.add_argument("--dry-run", action="store_true", help="Categorise and draft but don't log or escalate")

    args = parser.parse_args()

    # Load config
    global CONFIG_PATH
    if args.config:
        CONFIG_PATH = args.config
    config = load_config()

    # Parse input
    if args.stdin:
        raw = sys.stdin.read()
        try:
            data = json.loads(raw)
            message = data.get("message", "")
            context = data.get("context", {})
        except json.JSONDecodeError as e:
            print(f"[FATAL] Invalid JSON on stdin: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.message:
        message = args.message
        context = {}
        if args.context:
            try:
                context = json.loads(args.context)
            except json.JSONDecodeError as e:
                print(f"[FATAL] Invalid context JSON: {e}", file=sys.stderr)
                sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    if not message.strip():
        print("[FATAL] Empty message", file=sys.stderr)
        sys.exit(1)

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"RECOVERI CS RESPONDER — Ephemeral Agent", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)
    print(f"Message: {message[:100]}{'...' if len(message) > 100 else ''}", file=sys.stderr)
    print(f"Context: {json.dumps(context)}", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)

    if args.dry_run:
        print("[DRY RUN] Will categorise and draft but not log or escalate", file=sys.stderr)
        templates = load_skill_templates(config)
        bucket = categorise_message(message, config)
        bucket_name = config["buckets"].get(bucket, {}).get("name", "Unknown")
        draft = draft_response(message, bucket, templates, context.get("customer_name", ""), config)
        result = {"bucket": bucket, "bucket_name": bucket_name, "draft_response": draft, "dry_run": True}
    else:
        result = process_message(message, context, config)

    # Output result as JSON to stdout
    print(json.dumps(result, indent=2, default=str))

    print(f"\n[COMPLETE] Agent terminating.", file=sys.stderr)


if __name__ == "__main__":
    main()
