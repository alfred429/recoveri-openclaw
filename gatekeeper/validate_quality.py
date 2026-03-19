#!/usr/bin/env python3
"""
Gatekeeper Script 5: Quality Validator
Basic quality checks: readability, placeholder detection, uniqueness.
No AI judgment required — pure algorithmic checks.

Part of the Recoveri Gatekeeper validation pipeline.
Sprint 9 | Session 12 | 19 March 2026
"""

import json
import re
import sys
import os
from datetime import datetime, timezone


def load_config(config_path):
    with open(config_path) as f:
        return json.load(f)


def check_no_placeholders(output_path, patterns):
    if not os.path.isfile(output_path):
        return {"status": "SKIP", "detail": "Output file does not exist"}

    try:
        with open(output_path, "r", errors="replace") as f:
            content = f.read()

        found = []
        content_lower = content.lower()
        for pattern in patterns:
            if pattern.lower() in content_lower:
                # Find the line for context
                for i, line in enumerate(content.split("\n"), 1):
                    if pattern.lower() in line.lower():
                        found.append({"pattern": pattern, "line": i, "context": line.strip()[:80]})
                        break

        if found:
            return {
                "status": "FAIL",
                "detail": f"{len(found)} placeholder(s) found: {[f['pattern'] for f in found]}",
                "placeholders": found
            }
        return {"status": "PASS", "detail": "No placeholder text found"}

    except Exception as e:
        return {"status": "WARN", "detail": f"Placeholder check error: {e}"}


def check_readability(output_path, max_avg_sentence_length, min_paragraph_breaks):
    if not os.path.isfile(output_path):
        return {"status": "SKIP", "detail": "Output file does not exist"}

    try:
        with open(output_path, "r", errors="replace") as f:
            content = f.read()

        # Strip markdown headings and code blocks for analysis
        text = re.sub(r'```[\s\S]*?```', '', content)
        text = re.sub(r'^#+\s.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'\|[^\n]+\|', '', text)  # Remove table rows

        # Count sentences (rough)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]

        if not sentences:
            return {"status": "WARN", "detail": "Could not parse sentences"}

        avg_length = sum(len(s.split()) for s in sentences) / len(sentences)

        # Count paragraph breaks
        words = len(text.split())
        paragraphs = len(re.findall(r'\n\s*\n', content))
        breaks_per_1000 = (paragraphs / max(words, 1)) * 1000

        issues = []
        if avg_length > max_avg_sentence_length:
            issues.append(f"Average sentence length {avg_length:.0f} words (max: {max_avg_sentence_length})")
        if words > 200 and breaks_per_1000 < min_paragraph_breaks:
            issues.append(f"Only {breaks_per_1000:.1f} paragraph breaks per 1000 words (min: {min_paragraph_breaks})")

        if issues:
            return {"status": "WARN", "detail": "; ".join(issues)}
        return {
            "status": "PASS",
            "detail": f"Avg sentence: {avg_length:.0f} words, {paragraphs} paragraph breaks, {words} total words"
        }

    except Exception as e:
        return {"status": "WARN", "detail": f"Readability check error: {e}"}


def check_empty_sections(output_path):
    if not os.path.isfile(output_path):
        return {"status": "SKIP", "detail": "Output file does not exist"}

    try:
        with open(output_path, "r", errors="replace") as f:
            content = f.read()

        # Find headings followed by another heading with nothing between
        lines = content.split("\n")
        empty_sections = []
        for i, line in enumerate(lines):
            if line.strip().startswith("#"):
                # Look ahead: is the next non-empty line also a heading?
                for j in range(i + 1, min(i + 5, len(lines))):
                    stripped = lines[j].strip()
                    if stripped.startswith("#"):
                        empty_sections.append(line.strip())
                        break
                    elif stripped:
                        break

        if empty_sections:
            return {
                "status": "WARN",
                "detail": f"{len(empty_sections)} potentially empty section(s)",
                "sections": empty_sections[:5]
            }
        return {"status": "PASS", "detail": "All sections have content"}

    except Exception as e:
        return {"status": "WARN", "detail": f"Section check error: {e}"}


def validate(input_data, config):
    req_id = input_data.get("req_id", "UNKNOWN")
    output_path = input_data.get("output_path", "")

    quality_config = config.get("quality_validation", {})
    schema_config = config.get("schema_validation", {})

    placeholder_patterns = schema_config.get("placeholder_patterns",
        ["TBD", "TODO", "INSERT", "PLACEHOLDER", "Lorem ipsum"])
    max_avg_sentence = quality_config.get("max_avg_sentence_length", 60)
    min_para_breaks = quality_config.get("min_paragraph_breaks_per_1000_words", 3)

    checks = {
        "no_placeholders": check_no_placeholders(output_path, placeholder_patterns),
        "readability": check_readability(output_path, max_avg_sentence, min_para_breaks),
        "no_empty_sections": check_empty_sections(output_path),
    }

    failures = [k for k, v in checks.items() if v["status"] == "FAIL"]
    overall = "FAIL" if failures else "PASS"
    fail_reason = None
    if failures:
        reasons = [f"{k}: {checks[k]['detail']}" for k in failures]
        fail_reason = "; ".join(reasons)

    return {
        "validator": "quality",
        "req_id": req_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "overall": overall,
        "fail_reason": fail_reason
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gatekeeper: Quality Validator")
    parser.add_argument("--input", required=True, help="JSON string or file path")
    parser.add_argument("--config", default="/root/gatekeeper/config.json")
    args = parser.parse_args()

    config = load_config(args.config)
    if os.path.isfile(args.input):
        with open(args.input) as f:
            input_data = json.load(f)
    else:
        input_data = json.loads(args.input)

    result = validate(input_data, config)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["overall"] in ("PASS", "WARN") else 1)
