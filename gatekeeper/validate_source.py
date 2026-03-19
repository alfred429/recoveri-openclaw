#!/usr/bin/env python3
"""
Gatekeeper Script 3: Source Validator
Verifies the agent actually accessed required source material
and that the output references it.

Part of the Recoveri Gatekeeper validation pipeline.
Sprint 9 | Session 12 | 19 March 2026
"""

import json
import sys
import os
from datetime import datetime, timezone


def load_config(config_path):
    with open(config_path) as f:
        return json.load(f)


def check_source_files_exist(source_files):
    results = {}
    found = 0
    for sf in source_files:
        exists = os.path.isfile(sf)
        results[sf] = exists
        if exists:
            found += 1

    total = len(source_files)
    if total == 0:
        return {"status": "PASS", "detail": "No source files specified", "files": results}

    all_found = found == total
    return {
        "status": "PASS" if all_found else "WARN",
        "detail": f"{found}/{total} source files found",
        "files": results
    }


def check_keywords_in_output(output_path, keywords):
    if not keywords:
        return {"status": "PASS", "detail": "No keywords specified"}

    if not os.path.isfile(output_path):
        return {"status": "SKIP", "detail": "Output file does not exist"}

    try:
        with open(output_path, "r", errors="replace") as f:
            content = f.read().lower()

        found = []
        missing = []
        for kw in keywords:
            if kw.lower() in content:
                found.append(kw)
            else:
                missing.append(kw)

        ratio = len(found) / len(keywords) if keywords else 1.0

        if ratio == 0:
            status = "FAIL"
            detail = f"0/{len(keywords)} keywords found in output"
        elif ratio < 0.3:
            status = "FAIL"
            detail = f"{len(found)}/{len(keywords)} keywords found (below 30% threshold)"
        elif ratio < 0.6:
            status = "WARN"
            detail = f"{len(found)}/{len(keywords)} keywords found"
        else:
            status = "PASS"
            detail = f"{len(found)}/{len(keywords)} keywords found"

        result = {"status": status, "detail": detail, "found": found}
        if missing:
            result["missing"] = missing
        return result

    except Exception as e:
        return {"status": "FAIL", "detail": f"Error reading output: {e}"}


def check_output_references_source(output_path, source_files):
    if not os.path.isfile(output_path):
        return {"status": "SKIP", "detail": "Output file does not exist"}

    if not source_files:
        return {"status": "PASS", "detail": "No source files to reference"}

    try:
        with open(output_path, "r", errors="replace") as f:
            content = f.read().lower()

        referenced = 0
        for sf in source_files:
            basename = os.path.basename(sf).lower().replace("_", " ").replace("-", " ").replace(".md", "")
            if basename in content or os.path.basename(sf).lower() in content:
                referenced += 1

        if referenced > 0:
            return {"status": "PASS", "detail": f"Output references {referenced}/{len(source_files)} source files"}
        else:
            return {"status": "WARN", "detail": "Output does not explicitly reference source files by name"}

    except Exception as e:
        return {"status": "WARN", "detail": f"Reference check error: {e}"}


def validate(input_data, config):
    req_id = input_data.get("req_id", "UNKNOWN")
    source_files = input_data.get("source_files", [])
    source_keywords = input_data.get("source_keywords", [])
    output_path = input_data.get("output_path", "")

    checks = {
        "source_files_exist": check_source_files_exist(source_files),
        "source_keywords_in_output": check_keywords_in_output(output_path, source_keywords),
        "output_references_source": check_output_references_source(output_path, source_files),
    }

    failures = [k for k, v in checks.items() if v["status"] == "FAIL"]
    overall = "FAIL" if failures else "PASS"
    fail_reason = None
    if failures:
        reasons = [f"{k}: {checks[k]['detail']}" for k in failures]
        fail_reason = "; ".join(reasons)

    return {
        "validator": "source",
        "req_id": req_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "overall": overall,
        "fail_reason": fail_reason
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gatekeeper: Source Validator")
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
