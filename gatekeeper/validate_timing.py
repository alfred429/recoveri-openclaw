#!/usr/bin/env python3
"""
Gatekeeper Script 2: Timing Validator
Flags suspiciously fast task completions that may indicate fabrication.
A task completing in <10% of expected time is FAIL, <30% is WARN.

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


def parse_timestamp(ts):
    ts = ts.replace("Z", "+00:00")
    return datetime.fromisoformat(ts)


def validate(input_data, config):
    req_id = input_data.get("req_id", "UNKNOWN")
    task_type = input_data.get("task_type", "default")
    spawn_time = input_data["spawn_time"]
    completion_time = input_data["completion_time"]

    spawn_dt = parse_timestamp(spawn_time)
    completion_dt = parse_timestamp(completion_time)
    actual_seconds = (completion_dt - spawn_dt).total_seconds()

    thresholds = config.get("timing_thresholds", {})
    expected_minutes = thresholds.get(task_type, thresholds.get("default", 10))
    expected_seconds = expected_minutes * 60

    if expected_seconds > 0:
        ratio = actual_seconds / expected_seconds
    else:
        ratio = 1.0

    if ratio < 0.1:
        verdict = "FAIL"
        detail = (f"Completed in {actual_seconds:.0f}s, expected minimum {expected_seconds:.0f}s "
                  f"({ratio*100:.1f}% of expected time). Likely fabrication.")
    elif ratio < 0.3:
        verdict = "WARN"
        detail = (f"Completed in {actual_seconds:.0f}s, expected minimum {expected_seconds:.0f}s "
                  f"({ratio*100:.1f}% of expected time). Unusually fast.")
    else:
        verdict = "PASS"
        detail = (f"Completed in {actual_seconds:.0f}s, expected minimum {expected_seconds:.0f}s "
                  f"({ratio*100:.1f}% of expected time). Within acceptable range.")

    checks = {
        "actual_duration_seconds": actual_seconds,
        "expected_minimum_seconds": expected_seconds,
        "ratio": round(ratio, 4),
        "task_type": task_type,
        "verdict": verdict,
        "detail": detail
    }

    overall = verdict
    fail_reason = detail if verdict == "FAIL" else None

    return {
        "validator": "timing",
        "req_id": req_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "overall": overall,
        "fail_reason": fail_reason
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gatekeeper: Timing Validator")
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
