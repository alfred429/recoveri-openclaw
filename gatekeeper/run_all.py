#!/usr/bin/env python3
"""
Gatekeeper Master Runner
Orchestrates all 5 validators for a given REQ.
Logs results to JSONL. Returns structured result for Neo.

Usage:
  python run_all.py --req-id REQ-20260319-004 --output-path /path/to/output.md \\
    --output-type markdown --task-type brand_design \\
    --spawn-time 2026-03-19T14:29:30Z --completion-time 2026-03-19T14:30:00Z

  Or with a JSON input file:
  python run_all.py --input /path/to/validation_input.json

Part of the Recoveri Gatekeeper validation pipeline.
Sprint 9 | Session 12 | 19 March 2026
"""

import json
import sys
import os
from datetime import datetime, timezone

# Import validators
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_output import validate as validate_output
from validate_timing import validate as validate_timing
from validate_source import validate as validate_source
from validate_schema import validate as validate_schema
from validate_quality import validate as validate_quality


def load_config(config_path):
    with open(config_path) as f:
        return json.load(f)


def log_result(result, log_dir):
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "validations.jsonl")
    with open(log_file, "a") as f:
        f.write(json.dumps(result, default=str) + "\n")


def run_all(input_data, config):
    req_id = input_data.get("req_id", "UNKNOWN")
    results = {}
    warnings = []

    # 1. Output Validator
    output_input = {
        "req_id": req_id,
        "output_path": input_data.get("output_path", ""),
        "output_type": input_data.get("output_type", "text"),
        "min_word_count": input_data.get("min_word_count", None),
    }
    # Remove None values
    output_input = {k: v for k, v in output_input.items() if v is not None}
    results["output"] = validate_output(output_input, config)

    # 2. Timing Validator
    if input_data.get("spawn_time") and input_data.get("completion_time"):
        timing_input = {
            "req_id": req_id,
            "task_type": input_data.get("task_type", "default"),
            "spawn_time": input_data["spawn_time"],
            "completion_time": input_data["completion_time"],
        }
        results["timing"] = validate_timing(timing_input, config)
    else:
        results["timing"] = {
            "validator": "timing",
            "req_id": req_id,
            "overall": "SKIP",
            "fail_reason": None,
            "checks": {"detail": "No spawn/completion times provided"}
        }

    # 3. Source Validator
    if input_data.get("source_files") or input_data.get("source_keywords"):
        source_input = {
            "req_id": req_id,
            "source_files": input_data.get("source_files", []),
            "source_keywords": input_data.get("source_keywords", []),
            "output_path": input_data.get("output_path", ""),
        }
        results["source"] = validate_source(source_input, config)
    else:
        results["source"] = {
            "validator": "source",
            "req_id": req_id,
            "overall": "SKIP",
            "fail_reason": None,
            "checks": {"detail": "No source files or keywords specified"}
        }

    # 4. Schema Validator
    schema_input = {
        "req_id": req_id,
        "output_path": input_data.get("output_path", ""),
        "output_format": input_data.get("output_type", "text"),
        "required_sections": input_data.get("required_sections", []),
        "required_headings_min": input_data.get("required_headings_min", 0),
        "required_fields": input_data.get("required_fields", []),
    }
    results["schema"] = validate_schema(schema_input, config)

    # 5. Quality Validator
    quality_input = {
        "req_id": req_id,
        "output_path": input_data.get("output_path", ""),
    }
    results["quality"] = validate_quality(quality_input, config)

    # Aggregate
    failures = []
    for name, result in results.items():
        status = result.get("overall", "SKIP")
        if status == "FAIL":
            failures.append(f"{name}: {result.get('fail_reason', 'unknown')}")
        elif status == "WARN":
            warnings.append(f"{name}: {result.get('fail_reason', result.get('checks', {}).get('detail', 'warning'))}")

    if failures:
        overall = "FAIL"
        overall_reason = "; ".join(failures)
    elif warnings:
        overall = "PASS_WITH_WARNINGS"
        overall_reason = "; ".join(warnings)
    else:
        overall = "PASS"
        overall_reason = None

    master_result = {
        "gatekeeper": "run_all",
        "version": config.get("version", "1.0"),
        "req_id": req_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "overall": overall,
        "overall_reason": overall_reason,
        "validators": {name: result["overall"] for name, result in results.items()},
        "details": results,
        "summary": {
            "total_validators": len(results),
            "passed": sum(1 for r in results.values() if r["overall"] == "PASS"),
            "failed": sum(1 for r in results.values() if r["overall"] == "FAIL"),
            "warned": sum(1 for r in results.values() if r["overall"] in ("WARN", "PASS_WITH_WARNINGS")),
            "skipped": sum(1 for r in results.values() if r["overall"] == "SKIP"),
        }
    }

    # Log
    log_dir = config["paths"]["log_dir"]
    log_result(master_result, log_dir)

    return master_result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gatekeeper: Master Runner")
    parser.add_argument("--input", help="JSON file with all validation parameters")
    parser.add_argument("--req-id", help="Request ID")
    parser.add_argument("--output-path", help="Path to output file")
    parser.add_argument("--output-type", default="markdown", help="Output type (markdown, json, jsonl, text)")
    parser.add_argument("--task-type", default="default", help="Task type for timing validation")
    parser.add_argument("--spawn-time", help="ISO timestamp when task was spawned")
    parser.add_argument("--completion-time", help="ISO timestamp when task completed")
    parser.add_argument("--config", default="/root/gatekeeper/config.json", help="Config file path")
    args = parser.parse_args()

    config = load_config(args.config)

    if args.input and os.path.isfile(args.input):
        with open(args.input) as f:
            input_data = json.load(f)
    else:
        input_data = {
            "req_id": args.req_id or "UNKNOWN",
            "output_path": args.output_path or "",
            "output_type": args.output_type,
            "task_type": args.task_type,
        }
        if args.spawn_time:
            input_data["spawn_time"] = args.spawn_time
        if args.completion_time:
            input_data["completion_time"] = args.completion_time

    result = run_all(input_data, config)

    # Print summary for Neo
    print(json.dumps(result, indent=2))

    if result["overall"] == "FAIL":
        sys.exit(1)
    else:
        sys.exit(0)
