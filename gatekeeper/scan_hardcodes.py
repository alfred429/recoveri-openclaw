#!/usr/bin/env python3
"""
Gatekeeper: Hardcode Scanner
Scans the Recoveri system for hardcoded credentials, URLs, chat IDs,
file paths, magic numbers, and agent identities.

Golden Rule 1 enforcement at scale.

Usage:
  python3 scan_hardcodes.py [--output /path/to/report.jsonl] [--fix-mode]

Sprint 9 | Session 12 | 19 March 2026
"""

import json
import os
import re
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path

# ============================================================
# CONFIGURATION — all scan parameters in one place
# ============================================================

SCAN_DIRS = [
    "/root/.openclaw/agents",
    "/root/.openclaw/workspace",
    "/root/.openclaw/workspaces",
    "/root/.openclaw/skills",
    "/root/shared-repository",
    "/root/operations-logs",
    "/root/skill-registry",
    "/root/dashboard",
    "/root/gatekeeper",
    "/root/cron-triggers",
    "/root/loop-logs",
    "/root/request-register",
]

SCAN_EXTENSIONS = {
    ".py", ".sh", ".json", ".jsonl", ".md", ".yml", ".yaml",
    ".toml", ".cfg", ".conf", ".ini", ".html", ".js", ".css", ".txt",
}

SKIP_DIRS = {
    "node_modules", ".git", "__pycache__", ".npm", "venv",
    "backups", "_archive", "_model_backup_2026-03-09",
    "sessions",  # skip session transcripts
}

SKIP_FILES = {
    ".env",  # secrets SHOULD be here
    "scan_hardcodes.py",  # don't scan ourselves
}

SKIP_PATH_PATTERNS = [
    r"/backups/",
    r"\.bak",
    r"\.deleted\.",
    r"\.reset\.",
    r"/quarantine/",
    r"sessions\.json$",
]

# ============================================================
# PATTERN DEFINITIONS
# ============================================================

PATTERNS = {
    "CREDENTIAL": {
        "severity": "CRITICAL",
        "patterns": [
            (r'sk-[a-zA-Z0-9]{20,}', "DeepSeek/OpenAI API key"),
            (r'xai-[a-zA-Z0-9]{20,}', "xAI API key"),
            (r'sk-ant-[a-zA-Z0-9]{20,}', "Anthropic API key"),
            (r'AIza[a-zA-Z0-9_-]{35}', "Google API key"),
            (r'ghp_[a-zA-Z0-9]{36}', "GitHub personal access token"),
            (r'GOCSPX-[a-zA-Z0-9_-]{20,}', "Google OAuth client secret"),
            (r'"password"\s*:\s*"[^"]{4,}"', "Hardcoded password in JSON"),
            (r"password\s*=\s*['\"][^'\"]{4,}['\"]", "Hardcoded password in code"),
            (r'Bearer\s+[a-zA-Z0-9._-]{20,}', "Hardcoded Bearer token"),
        ],
    },
    "TELEGRAM_TOKEN": {
        "severity": "CRITICAL",
        "patterns": [
            (r'\b\d{9,10}:[A-Za-z0-9_-]{35}\b', "Telegram bot token"),
        ],
    },
    "URL_ENDPOINT": {
        "severity": "HIGH",
        "patterns": [
            (r'178\.104\.2\.237', "Hardcoded VPS IP address"),
            (r'board\.craab\.io', "Hardcoded dashboard domain"),
            (r'recoveri\.io', "Hardcoded recoveri.io domain"),
            (r'api\.deepseek\.com', "Hardcoded DeepSeek API URL"),
            (r'api\.x\.ai', "Hardcoded xAI API URL"),
            (r'localhost:\d{4,5}', "Hardcoded localhost port"),
            (r'127\.0\.0\.1:\d{4,5}', "Hardcoded loopback port"),
        ],
    },
    "CHAT_ID": {
        "severity": "HIGH",
        "patterns": [
            (r'\b8295330880\b', "Hardcoded Boss Telegram chat ID"),
            (r'\b1279816695\b', "Hardcoded user Telegram ID"),
        ],
    },
    "EMAIL": {
        "severity": "HIGH",
        "patterns": [
            (r'alfred@recoveri\.io', "Hardcoded email address"),
            (r'mike@recoveri\.io', "Hardcoded email address"),
        ],
    },
    "FILE_PATH": {
        "severity": "MEDIUM",
        "patterns": [
            (r'/root/shared-repository/', "Hardcoded shared-repository path"),
            (r'/root/operations-logs/', "Hardcoded operations-logs path"),
            (r'/root/skill-registry/', "Hardcoded skill-registry path"),
            (r'/root/dashboard/', "Hardcoded dashboard path"),
            (r'/root/gatekeeper/', "Hardcoded gatekeeper path"),
            (r'/root/request-register/', "Hardcoded request-register path"),
            (r'/root/loop-logs/', "Hardcoded loop-logs path"),
            (r'/root/cron-triggers/', "Hardcoded cron-triggers path"),
        ],
    },
    "MAGIC_NUMBER": {
        "severity": "MEDIUM",
        "patterns": [
            (r'\b1000000\b', "Hardcoded token limit (1M)"),
            (r'max_tokens["\s:=]+\d{4,}', "Hardcoded max_tokens value"),
            (r'timeout["\s:=]+\d{3,}', "Hardcoded timeout value"),
            (r'retry["\s:=]+\d+', "Hardcoded retry count"),
        ],
    },
    "AGENT_IDENTITY": {
        "severity": "LOW",
        "patterns": [
            (r'grok-4-1-fast', "Hardcoded model name"),
            (r'grok-4\b', "Hardcoded model name"),
            (r'deepseek-chat', "Hardcoded model name"),
            (r'qwen2\.5:3b', "Hardcoded model name"),
            (r'qwen3\.5-122b', "Hardcoded model name"),
        ],
    },
}

# Files where certain patterns are EXPECTED (reduce false positives)
ALLOWLIST = {
    # Config files where paths/URLs are expected
    "config.json": {"FILE_PATH", "URL_ENDPOINT", "MAGIC_NUMBER"},
    "cs-config.json": {"FILE_PATH", "URL_ENDPOINT", "MAGIC_NUMBER"},
    "Caddyfile": {"URL_ENDPOINT"},
    "openclaw.json": {"CHAT_ID", "EMAIL", "URL_ENDPOINT", "AGENT_IDENTITY", "TELEGRAM_TOKEN"},
    ".env": {"CREDENTIAL", "TELEGRAM_TOKEN"},
    "models.json": {"URL_ENDPOINT", "AGENT_IDENTITY"},
    "auth-profiles.json": {"URL_ENDPOINT"},
    "agent.json": {"AGENT_IDENTITY"},
    "SOUL.md": {"AGENT_IDENTITY", "EMAIL"},
    "IDENTITY.md": {"AGENT_IDENTITY"},
    "USER.md": {"EMAIL"},
    "ENTERPRISE_SOUL.md": {"AGENT_IDENTITY"},
    # Governance/doc files
    "recoveri-dashboard-implementation.md": {"URL_ENDPOINT", "EMAIL", "FILE_PATH"},
    "README.md": {"URL_ENDPOINT", "FILE_PATH"},
    "SKILL.md": {"FILE_PATH", "EMAIL"},
    "SKILL_132.md": {"FILE_PATH", "EMAIL"},
    # Service files
    "recoveri-dashboard.service": {"FILE_PATH"},
    "gmail-watcher.service": {"URL_ENDPOINT", "TELEGRAM_TOKEN"},
    "openclaw-gateway.service": {"CREDENTIAL"},
    # Scanner config section (self)
    "scan_hardcodes.py": {"CHAT_ID", "EMAIL", "FILE_PATH", "URL_ENDPOINT", "CREDENTIAL", "TELEGRAM_TOKEN", "MAGIC_NUMBER", "AGENT_IDENTITY"},
}


def mask_value(val, keep=4):
    """Mask sensitive values for safe logging."""
    s = str(val)
    if len(s) <= keep * 2:
        return "****"
    return s[:keep] + "****" + s[-keep:]


def is_binary(filepath):
    """Quick binary file check."""
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(512)
        return b"\x00" in chunk
    except (OSError, PermissionError):
        return True


def should_skip(filepath):
    """Check if file should be skipped."""
    p = Path(filepath)

    # Skip by directory
    for part in p.parts:
        if part in SKIP_DIRS:
            return True

    # Skip by filename
    if p.name in SKIP_FILES:
        return True

    # Skip by path pattern
    for pat in SKIP_PATH_PATTERNS:
        if re.search(pat, str(filepath)):
            return True

    # Skip by extension
    if p.suffix and p.suffix.lower() not in SCAN_EXTENSIONS:
        return True

    return False


def get_category_for_file(filename):
    """Get allowlisted categories for a filename."""
    return ALLOWLIST.get(filename, set())


def scan_file(filepath, scan_id):
    """Scan a single file for hardcode violations."""
    findings = []
    filename = os.path.basename(filepath)
    allowed = get_category_for_file(filename)

    try:
        with open(filepath, "r", errors="replace") as f:
            lines = f.readlines()
    except (OSError, PermissionError):
        return findings

    for line_num, line in enumerate(lines, 1):
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith("#") and not any(
            re.search(p[0], line_stripped) for cat in PATTERNS.values() for p in cat["patterns"]
        ):
            continue

        for category, config in PATTERNS.items():
            # Skip allowlisted categories for this file
            if category in allowed:
                continue

            for pattern, description in config["patterns"]:
                matches = re.finditer(pattern, line)
                for match in matches:
                    val = match.group(0)
                    # Mask credentials
                    if config["severity"] == "CRITICAL":
                        preview = mask_value(val)
                    else:
                        preview = val[:50] + ("..." if len(val) > 50 else "")

                    findings.append({
                        "scan_id": scan_id,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "file": filepath,
                        "line": line_num,
                        "category": category,
                        "severity": config["severity"],
                        "pattern_matched": description,
                        "value_preview": preview,
                        "recommendation": get_recommendation(category, description),
                    })

    return findings


def get_recommendation(category, description):
    """Generate fix recommendation based on category."""
    recs = {
        "CREDENTIAL": "Move to /root/.env and reference via environment variable",
        "TELEGRAM_TOKEN": "Move to /root/.env as TELEGRAM_BOT_TOKEN",
        "URL_ENDPOINT": "Move to config.json or reference via environment variable",
        "CHAT_ID": "Move to config.json under telegram.chat_ids",
        "EMAIL": "Move to config.json under allowed_emails or reference via config",
        "FILE_PATH": "Use config.json paths section or environment variables",
        "MAGIC_NUMBER": "Move to config.json thresholds section",
        "AGENT_IDENTITY": "Reference from agent registry or model-router-governance",
    }
    return recs.get(category, "Review and move to appropriate config file")


def scan_all(directories, output_path=None):
    """Run full scan across all directories."""
    scan_id = f"SCAN-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    all_findings = []
    files_scanned = 0
    files_skipped = 0

    for scan_dir in directories:
        if not os.path.isdir(scan_dir):
            continue

        for root, dirs, files in os.walk(scan_dir):
            # Skip entire directories
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

            for filename in files:
                filepath = os.path.join(root, filename)

                if should_skip(filepath):
                    files_skipped += 1
                    continue

                if is_binary(filepath):
                    files_skipped += 1
                    continue

                files_scanned += 1
                findings = scan_file(filepath, scan_id)
                all_findings.extend(findings)

    # Deduplicate (same file+line+category)
    seen = set()
    unique_findings = []
    for f in all_findings:
        key = (f["file"], f["line"], f["category"], f["pattern_matched"])
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    # Sort by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    unique_findings.sort(key=lambda x: (severity_order.get(x["severity"], 9), x["file"]))

    # Write report
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            for finding in unique_findings:
                f.write(json.dumps(finding) + "\n")

    # Summary
    by_severity = {}
    for f in unique_findings:
        sev = f["severity"]
        by_severity[sev] = by_severity.get(sev, 0) + 1

    by_category = {}
    for f in unique_findings:
        cat = f["category"]
        by_category[cat] = by_category.get(cat, 0) + 1

    summary = {
        "scan_id": scan_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "files_scanned": files_scanned,
        "files_skipped": files_skipped,
        "total_findings": len(unique_findings),
        "by_severity": {
            "CRITICAL": by_severity.get("CRITICAL", 0),
            "HIGH": by_severity.get("HIGH", 0),
            "MEDIUM": by_severity.get("MEDIUM", 0),
            "LOW": by_severity.get("LOW", 0),
        },
        "by_category": by_category,
        "output_file": output_path,
    }

    return summary, unique_findings


def print_summary(summary, findings):
    """Print human-readable summary."""
    print()
    print("HARDCODE SCAN COMPLETE")
    print("=" * 50)
    print(f"Scan ID:        {summary['scan_id']}")
    print(f"Files scanned:  {summary['files_scanned']}")
    print(f"Files skipped:  {summary['files_skipped']}")
    print(f"Total findings: {summary['total_findings']}")
    print()
    sev = summary["by_severity"]
    print(f"  CRITICAL: {sev['CRITICAL']}  (credentials)")
    print(f"  HIGH:     {sev['HIGH']}  (URLs, chat IDs, emails)")
    print(f"  MEDIUM:   {sev['MEDIUM']}  (file paths, magic numbers)")
    print(f"  LOW:      {sev['LOW']}  (agent identities)")
    print()

    if summary.get("by_category"):
        print("By category:")
        for cat, count in sorted(summary["by_category"].items()):
            print(f"  {cat}: {count}")
        print()

    if summary["output_file"]:
        print(f"Report: {summary['output_file']}")
    print()

    # Top findings
    if findings:
        print("TOP FINDINGS:")
        print("-" * 50)
        shown = 0
        for f in findings:
            if shown >= 15:
                remaining = len(findings) - shown
                if remaining > 0:
                    print(f"  ... and {remaining} more findings")
                break
            sev_icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵"}.get(f["severity"], "⚪")
            rel_path = f["file"].replace("/root/", "~/")
            print(f"  {sev_icon} [{f['severity']}] {rel_path}:{f['line']}")
            print(f"     {f['pattern_matched']}: {f['value_preview']}")
            shown += 1
        print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gatekeeper: Hardcode Scanner")
    parser.add_argument("--output", default=None, help="JSONL output file path")
    parser.add_argument("--fix-mode", action="store_true", help="(Future) Apply automated fixes")
    parser.add_argument("--dirs", nargs="*", help="Override scan directories")
    parser.add_argument("--quiet", action="store_true", help="Only output JSON summary")
    args = parser.parse_args()

    if args.fix_mode:
        print("Fix mode is not yet implemented. Running in scan-only mode.")

    dirs = args.dirs if args.dirs else SCAN_DIRS

    if not args.output:
        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
        args.output = f"/root/gatekeeper/log/hardcode-scan-{date_str}.jsonl"

    summary, findings = scan_all(dirs, args.output)

    if args.quiet:
        print(json.dumps(summary, indent=2))
    else:
        print_summary(summary, findings)

    sys.exit(1 if summary["total_findings"] > 0 else 0)
