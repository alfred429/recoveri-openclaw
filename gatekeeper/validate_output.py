#!/usr/bin/env python3
"""
Gatekeeper Script 1: Output Validator
Checks that output files exist, are non-empty, contain real content,
and are not duplicates of previous outputs.

Part of the Recoveri Gatekeeper validation pipeline.
Sprint 9 | Session 12 | 19 March 2026
"""

import json
import hashlib
import os
import sys
from datetime import datetime, timezone


def load_config(config_path):
    with open(config_path) as f:
        return json.load(f)


def check_file_exists(path):
    exists = os.path.isfile(path)
    return {
        "status": "PASS" if exists else "FAIL",
        "detail": f"File found at {path}" if exists else f"File not found at {path}"
    }


def check_non_empty(path):
    if not os.path.isfile(path):
        return {"status": "SKIP", "detail": "File does not exist"}
    size = os.path.getsize(path)
    return {
        "status": "PASS" if size > 0 else "FAIL",
        "detail": f"File size: {size} bytes" if size > 0 else "File is empty (0 bytes)"
    }


def check_word_count(path, min_words):
    if not os.path.isfile(path):
        return {"status": "SKIP", "detail": "File does not exist"}
    try:
        with open(path, "r", errors="replace") as f:
            text = f.read()
        words = len(text.split())
        passed = words >= min_words
        return {
            "status": "PASS" if passed else "FAIL",
            "detail": f"Word count: {words} (minimum: {min_words})",
            "word_count": words
        }
    except Exception as e:
        return {"status": "FAIL", "detail": f"Error reading file: {e}"}


def check_not_duplicate(path, log_dir):
    if not os.path.isfile(path):
        return {"status": "SKIP", "detail": "File does not exist"}
    try:
        with open(path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        hash_log = os.path.join(log_dir, "output_hashes.jsonl")
        if os.path.isfile(hash_log):
            with open(hash_log) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        if entry.get("hash") == file_hash and entry.get("path") != path:
                            return {
                                "status": "WARN",
                                "detail": f"Duplicate of {entry['path']} (hash: {file_hash[:16]}...)"
                            }
                    except json.JSONDecodeError:
                        continue

        # Log this hash
        os.makedirs(os.path.dirname(hash_log), exist_ok=True)
        with open(hash_log, "a") as f:
            f.write(json.dumps({
                "path": path,
                "hash": file_hash,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }) + "\n")

        return {"status": "PASS", "detail": f"No duplicate found (hash: {file_hash[:16]}...)"}
    except Exception as e:
        return {"status": "WARN", "detail": f"Duplicate check failed: {e}"}


def check_valid_format(path, output_type):
    if not os.path.isfile(path):
        return {"status": "SKIP", "detail": "File does not exist"}
    try:
        with open(path, "r", errors="replace") as f:
            content = f.read()

        if output_type in ("json", "jsonl"):
            if output_type == "jsonl":
                lines = [l for l in content.strip().split("\n") if l.strip()]
                for i, line in enumerate(lines):
                    json.loads(line)
                return {"status": "PASS", "detail": f"Valid JSONL ({len(lines)} entries)"}
            else:
                json.loads(content)
                return {"status": "PASS", "detail": "Valid JSON"}

        elif output_type == "markdown":
            has_headings = any(line.strip().startswith("#") for line in content.split("\n"))
            has_content = len(content.strip()) > 0
            if has_headings and has_content:
                return {"status": "PASS", "detail": "Valid markdown with headings"}
            elif has_content:
                return {"status": "WARN", "detail": "Content present but no markdown headings found"}
            else:
                return {"status": "FAIL", "detail": "No meaningful content"}

        else:
            if len(content.strip()) > 0:
                return {"status": "PASS", "detail": f"File has content ({len(content)} chars)"}
            return {"status": "FAIL", "detail": "File appears empty"}

    except json.JSONDecodeError as e:
        return {"status": "FAIL", "detail": f"Invalid {output_type}: {e}"}
    except Exception as e:
        return {"status": "FAIL", "detail": f"Format check failed: {e}"}


def validate(input_data, config):
    req_id = input_data.get("req_id", "UNKNOWN")
    output_path = input_data["output_path"]
    output_type = input_data.get("output_type", "text")
    log_dir = config["paths"]["log_dir"]

    if output_type in ("json", "jsonl"):
        min_words = input_data.get("min_word_count", config["output_validation"]["min_word_count_jsonl"])
    else:
        min_words = input_data.get("min_word_count", config["output_validation"]["min_word_count_document"])

    checks = {
        "file_exists": check_file_exists(output_path),
        "non_empty": check_non_empty(output_path),
        "word_count": check_word_count(output_path, min_words),
        "not_duplicate": check_not_duplicate(output_path, log_dir),
        "valid_format": check_valid_format(output_path, output_type),
    }

    failures = [k for k, v in checks.items() if v["status"] == "FAIL"]
    overall = "FAIL" if failures else "PASS"
    fail_reason = None
    if failures:
        reasons = [f"{k}: {checks[k]['detail']}" for k in failures]
        fail_reason = "; ".join(reasons)

    return {
        "validator": "output",
        "req_id": req_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "overall": overall,
        "fail_reason": fail_reason
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gatekeeper: Output Validator")
    parser.add_argument("--input", required=True, help="JSON string or file path with validation input")
    parser.add_argument("--config", default="/root/gatekeeper/config.json", help="Config file path")
    args = parser.parse_args()

    config = load_config(args.config)

    if os.path.isfile(args.input):
        with open(args.input) as f:
            input_data = json.load(f)
    else:
        input_data = json.loads(args.input)

    result = validate(input_data, config)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["overall"] == "PASS" else 1)
