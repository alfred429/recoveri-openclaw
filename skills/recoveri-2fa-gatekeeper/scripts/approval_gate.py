#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import random
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

STATE = "/root/.openclaw/workspaces/main/shared/approval-state.json"
AUDIT = "/root/.openclaw/workspaces/main/shared/APPROVAL_EVENTS.jsonl"
PATTERN = re.compile(r"^007-([A-Z0-9]+)-([0-9]{4})$")

TELEGRAM_TARGET = "1279816695"
EMAIL_TARGET = "mike@recoveri.io"


def now():
    return datetime.now(timezone.utc)


def iso(dt):
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def load_state():
    if not os.path.exists(STATE):
        return {"active": None}
    with open(STATE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    ensure(STATE)
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def audit(event):
    ensure(AUDIT)
    with open(AUDIT, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def ahash(summary, channel, session, agent):
    raw = f"{summary}|{channel}|{session}|{agent}"
    return hashlib.sha256(raw.encode()).hexdigest()[:12]


def build_delivery_message(active):
    return (
        "Recoveri Security Approval Required\n\n"
        f"Action: {active['action_summary']}\n"
        f"Challenge: {active['challenge_id']}\n"
        f"Code: {active['code']}\n"
        "Expires: 5 minutes\n\n"
        "Approve in webchat using:\n"
        f"007-{active['challenge_id']}-{active['code']}"
    )



def send_email_message(message_text, cid):
    cmd = [
        "gog","gmail","send",
        "--account","alfred@recoveri.io",
        "--to","mike@recoveri.io",
        "--subject",f"Recoveri approval {cid}",
        "--body",message_text
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "command": cmd
    }


def send_telegram_message(message_text):
    cmd = [
        "openclaw",
        "message",
        "send",
        "--channel",
        "telegram",
        "--target",
        TELEGRAM_TARGET,
        "--message",
        message_text,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "command": cmd,
    }


def expire_if_needed(state):
    active = state.get("active")
    if not active:
        return state
    exp = datetime.fromisoformat(active["expires_at"].replace("Z", "+00:00"))
    if now() <= exp:
        return state
    audit({
        "timestamp": iso(now()),
        "event_type": "expire",
        "challenge_id": active["challenge_id"],
        "action_summary": active["action_summary"],
        "action_hash": active["action_hash"],
        "requester_channel": active["requester_channel"],
        "requester_session": active["requester_session"],
        "requester_agent": active["requester_agent"],
        "delivery_channels": active["delivery_channels"],
        "result": "expired",
        "retry_count": active["retry_count"],
    })
    state["active"] = None
    save_state(state)
    return state


def create(args):
    state = expire_if_needed(load_state())
    if state.get("active"):
        print(json.dumps({
            "status": "blocked",
            "reason": "pending_approval_exists",
            "challenge_id": state["active"]["challenge_id"]
        }, indent=2))
        return 1

    cid = "".join(random.choice("ABCDEFGHJKLMNPQRSTUVWXYZ23456789") for _ in range(2))
    code = f"{random.randint(0, 9999):04d}"
    created = now()

    active = {
        "challenge_id": cid,
        "code": code,
        "action_summary": args.action_summary,
        "action_hash": ahash(
            args.action_summary,
            args.requester_channel,
            args.requester_session,
            args.requester_agent,
        ),
        "requester_channel": args.requester_channel,
        "requester_session": args.requester_session,
        "requester_agent": args.requester_agent,
        "delivery_channels": ["telegram", "email"],
        "created_at": iso(created),
        "expires_at": iso(created + timedelta(minutes=5)),
        "retry_count": 0,
        "max_retries": 3,
        "status": "pending",
    }

    state["active"] = active
    save_state(state)

    delivery_message = build_delivery_message(active)
    telegram = send_telegram_message(delivery_message)
    email = send_email_message(delivery_message, cid)

    audit({
        "timestamp": iso(now()),
        "event_type": "create",
        "challenge_id": cid,
        "action_summary": active["action_summary"],
        "action_hash": active["action_hash"],
        "requester_channel": active["requester_channel"],
        "requester_session": active["requester_session"],
        "requester_agent": active["requester_agent"],
        "delivery_channels": active["delivery_channels"],
        "result": "pending",
        "retry_count": 0
    })

    print(json.dumps({
        "status": "challenge_created",
        "challenge_id": cid,
        "code": code,
        "expires_at": active["expires_at"],
        "approval_format": f"007-{cid}-{code}",
        "telegram_delivery": telegram,
        "email_delivery": email
    }, indent=2))
    return 0


def verify(args):
    state = expire_if_needed(load_state())
    active = state.get("active")
    if not active:
        print(json.dumps({"status": "denied", "reason": "no_active_challenge"}, indent=2))
        return 1

    if args.requester_channel != "webchat":
        print(json.dumps({"status": "denied", "reason": "approval_channel_must_be_webchat"}, indent=2))
        return 1

    m = PATTERN.match(args.approval_text.strip())
    if not m:
        print(json.dumps({"status": "denied", "reason": "invalid_approval_format"}, indent=2))
        return 1

    cid, code = m.groups()

    if cid != active["challenge_id"] or code != active["code"]:
        active["retry_count"] += 1
        result = "challenge_or_code_mismatch"
        if active["retry_count"] >= active["max_retries"]:
            result = "retry_limit_reached"
            state["active"] = None
        save_state(state)
        audit({
            "timestamp": iso(now()),
            "event_type": "verify-fail",
            "challenge_id": active["challenge_id"],
            "action_summary": active["action_summary"],
            "action_hash": active["action_hash"],
            "requester_channel": active["requester_channel"],
            "requester_session": active["requester_session"],
            "requester_agent": active["requester_agent"],
            "delivery_channels": active["delivery_channels"],
            "result": result,
            "retry_count": active["retry_count"]
        })
        print(json.dumps({"status": "denied", "reason": result}, indent=2))
        return 1

    audit({
        "timestamp": iso(now()),
        "event_type": "verify-success",
        "challenge_id": active["challenge_id"],
        "action_summary": active["action_summary"],
        "action_hash": active["action_hash"],
        "requester_channel": active["requester_channel"],
        "requester_session": active["requester_session"],
        "requester_agent": active["requester_agent"],
        "delivery_channels": active["delivery_channels"],
        "result": "approved",
        "retry_count": active["retry_count"]
    })

    out = {
        "status": "approved",
        "challenge_id": active["challenge_id"],
        "action_summary": active["action_summary"],
        "action_hash": active["action_hash"]
    }
    state["active"] = None
    save_state(state)
    print(json.dumps(out, indent=2))
    return 0


def status_cmd(_args):
    print(json.dumps(expire_if_needed(load_state()), indent=2))
    return 0


def cancel(_args):
    state = expire_if_needed(load_state())
    active = state.get("active")
    if not active:
        print(json.dumps({"status": "no_active_challenge"}, indent=2))
        return 0

    audit({
        "timestamp": iso(now()),
        "event_type": "cancel",
        "challenge_id": active["challenge_id"],
        "action_summary": active["action_summary"],
        "action_hash": active["action_hash"],
        "requester_channel": active["requester_channel"],
        "requester_session": active["requester_session"],
        "requester_agent": active["requester_agent"],
        "delivery_channels": active["delivery_channels"],
        "result": "cancelled",
        "retry_count": active["retry_count"]
    })
    state["active"] = None
    save_state(state)
    print(json.dumps({"status": "cancelled"}, indent=2))
    return 0


p = argparse.ArgumentParser()
sub = p.add_subparsers(dest="cmd", required=True)

c = sub.add_parser("create")
c.add_argument("--action-summary", required=True)
c.add_argument("--requester-channel", required=True)
c.add_argument("--requester-session", required=True)
c.add_argument("--requester-agent", required=True)
c.set_defaults(func=create)

v = sub.add_parser("verify")
v.add_argument("--approval-text", required=True)
v.add_argument("--requester-channel", required=True)
v.set_defaults(func=verify)

s = sub.add_parser("status")
s.set_defaults(func=status_cmd)

x = sub.add_parser("cancel")
x.set_defaults(func=cancel)

args = p.parse_args()
sys.exit(args.func(args))
