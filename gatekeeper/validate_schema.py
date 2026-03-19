#!/usr/bin/env python3
"""
Gatekeeper Script 4: Schema Validator
Checks that output matches the structure required by the REQ —
required sections, headings, JSONL schema compliance.

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


def check_required_sections(output_path, required_sections):
    if not required_sections:
        return {"status": "PASS", "detail": "No required sections specified"}

    if not os.path.isfile(output_path):
        return {"status": "SKIP", "detail": "Output file does not exist"}

    try:
        with open(output_path, "r", errors="replace") as f:
            content = f.read().lower()

        found = []
        missing = []
        for section in required_sections:
            if section.lower() in content:
                found.append(section)
            else:
                missing.append(section)

        if not missing:
            return {"status": "PASS", "detail": f"All {len(required_sections)} required sections found", "found": found}
        else:
            ratio = len(found) / len(required_sections)
            status = "FAIL" if ratio < 0.5 else "WARN"
            result = {
                "status": status,
                "detail": f"{len(found)}/{len(required_sections)} required sections found",
                "found": found,
                "missing": missing
            }
            return result

    except Exception as e:
        return {"status": "FAIL", "detail": f"Error checking sections: {e}"}


def check_headings(output_path, min_headings, output_format):
    if output_format not in ("markdown", "md"):
        return {"status": "PASS", "detail": f"Heading check N/A for format: {output_format}"}

    if not os.path.isfile(output_path):
        return {"status": "SKIP", "detail": "Output file does not exist"}

    try:
        with open(output_path, "r", errors="replace") as f:
            lines = f.readlines()

        headings = [l.strip() for l in lines if l.strip().startswith("#")]
        count = len(headings)

        if count >= min_headings:
            return {"status": "PASS", "detail": f"{count} headings found (minimum: {min_headings})"}
        else:
            return {
                "status": "FAIL" if count == 0 else "WARN",
                "detail": f"{count} headings found (minimum: {min_headings})"
            }

    except Exception as e:
        return {"status": "FAIL", "detail": f"Error checking headings: {e}"}


def check_jsonl_schema(output_path, required_fields):
    if not required_fields:
        return {"status": "PASS", "detail": "No required fields specified"}

    if not os.path.isfile(output_path):
        return {"status": "SKIP", "detail": "Output file does not exist"}

    try:
        with open(output_path, "r", errors="replace") as f:
            lines = [l.strip() for l in f if l.strip()]

        if not lines:
            return {"status": "FAIL", "detail": "JSONL file is empty"}

        missing_fields = set()
        invalid_lines = 0

        for i, line in enumerate(lines):
            try:
                entry = json.loads(line)
                for field in required_fields:
                    if field not in entry:
                        missing_fields.add(field)
            except json.JSONDecodeError:
                invalid_lines += 1

        if invalid_lines > 0:
            return {"status": "FAIL", "detail": f"{invalid_lines}/{len(lines)} lines are invalid JSON"}
        elif missing_fields:
            return {
                "status": "WARN",
                "detail": f"Missing fields in some entries: {list(missing_fields)}"
            }
        else:
            return {"status": "PASS", "detail": f"All {len(lines)} entries have required fields"}

    except Exception as e:
        return {"status": "FAIL", "detail": f"Schema check error: {e}"}


def validate(input_data, config):
    req_id = input_data.get("req_id", "UNKNOWN")
    output_path = input_data.get("output_path", "")
    output_format = input_data.get("output_format", "text")
    required_sections = input_data.get("required_sections", [])
    required_headings_min = input_data.get("required_headings_min", 0)
    required_fields = input_data.get("required_fields", [])

    checks = {
        "required_sections": check_required_sections(output_path, required_sections),
        "headings_count": check_headings(output_path, required_headings_min, output_format),
    }

    if output_format in ("json", "jsonl"):
        checks["jsonl_schema"] = check_jsonl_schema(output_path, required_fields)

    failures = [k for k, v in checks.items() if v["status"] == "FAIL"]
    overall = "FAIL" if failures else "PASS"
    fail_reason = None
    if failures:
        reasons = [f"{k}: {checks[k]['detail']}" for k in failures]
        fail_reason = "; ".join(reasons)

    return {
        "validator": "schema",
        "req_id": req_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "overall": overall,
        "fail_reason": fail_reason
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gatekeeper: Schema Validator")
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
