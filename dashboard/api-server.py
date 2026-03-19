#!/usr/bin/env python3
"""Recoveri Dashboard API Server — pure stdlib, no pip dependencies.
v4.0 — Google Sign-In auth layer added."""

import http.server
import json
import glob
import os
import subprocess
import sys
import re
import secrets
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse, parse_qs, urlencode
import urllib.parse
from pathlib import Path
from http.cookies import SimpleCookie

PORT = 18803

# ---------------------------------------------------------------------------
# Data source paths — configurable via env vars (Golden Rule: never hardcode)
# ---------------------------------------------------------------------------
DATA_PATHS = {
    "approvals": os.environ.get("APPROVALS_PATH", "/root/shared-repository/governance/approvals.jsonl"),
    "backlog": os.environ.get("BACKLOG_PATH", "/root/shared-repository/governance/backlog.jsonl"),
    "incidents": os.environ.get("INCIDENTS_PATH", "/root/shared-repository/governance/incidents.jsonl"),
    "market_intel": os.environ.get("MARKET_INTEL_PATH", "/root/shared-repository/data/market-intel/raw/"),
    "swarm_feedback": os.environ.get("SWARM_FEEDBACK_PATH", "/root/shared-repository/data/swarm-feedback/feedback.jsonl"),
    "skill_evolution_routing": os.environ.get("SKILL_EVOLUTION_ROUTING_PATH", "/root/shared-repository/skills/skill-routing.jsonl"),
    "skill_evolution_patterns": os.environ.get("SKILL_EVOLUTION_PATTERNS_PATH", "/root/shared-repository/data/skill-evolution/patterns/"),
    "gatekeeper_log": os.environ.get("GATEKEEPER_LOG_PATH", "/root/gatekeeper/log/validations.jsonl"),
    "hardcode_scan": os.environ.get("HARDCODE_SCAN_PATH", "/root/gatekeeper/log/"),
    "cs_pipeline": os.environ.get("CS_PIPELINE_PATH", "/root/shared-repository/data/cs-pipeline/tickets.jsonl"),
    "agent_activity": os.environ.get("AGENT_ACTIVITY_PATH", "/root/shared-repository/governance/agent-activity.jsonl"),
    "research_etsy": os.environ.get("RESEARCH_ETSY_PATH", "/root/shared-repository/data/etsy-scanner/"),
    "research_trends": os.environ.get("RESEARCH_TRENDS_PATH", "/root/shared-repository/data/google-trends/"),
    "research_hn": os.environ.get("RESEARCH_HN_PATH", "/root/shared-repository/data/hackernews/"),
    "research_rss": os.environ.get("RESEARCH_RSS_PATH", "/root/shared-repository/data/rss-news/"),
    "research_ai": os.environ.get("RESEARCH_AI_PATH", "/root/shared-repository/data/ai-trends/"),
    "trading_loop": os.environ.get("TRADING_LOOP_PATH", "/root/loop-logs/"),
}
STATIC_DIR = "/root/dashboard/public"

# ---------------------------------------------------------------------------
# Auth config
# ---------------------------------------------------------------------------
GOOGLE_CLIENT_ID = "894077996747-ns8eb7p1numq4irbjhvhf96tnsb01k79.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = "https://board.craab.io/auth/callback"
ALLOWED_EMAILS = ["alfred@recoveri.io", "mike@recoveri.io"]
SESSION_MAX_AGE = 7 * 24 * 3600  # 7 days

# In-memory session store: token -> {"email": str, "created": float}
SESSIONS = {}

# Short-lived auth codes: code -> {"email": str, "created": float}
# Used to bridge POST verification → GET cookie-setting
AUTH_CODES = {}
AUTH_CODE_MAX_AGE = 60  # 60 seconds

AUTH_EXEMPT_PATHS = {"/login.html", "/auth/google", "/auth/logout", "/auth/callback"}


def generate_session_token():
    return secrets.token_urlsafe(48)


def create_session(email):
    token = generate_session_token()
    SESSIONS[token] = {"email": email, "created": time.time()}
    return token


def validate_session(token):
    if not token or token not in SESSIONS:
        return None
    session = SESSIONS[token]
    if time.time() - session["created"] > SESSION_MAX_AGE:
        del SESSIONS[token]
        return None
    return session


def purge_expired_sessions():
    now = time.time()
    expired = [t for t, s in SESSIONS.items() if now - s["created"] > SESSION_MAX_AGE]
    for t in expired:
        del SESSIONS[t]


def verify_google_token(id_token):
    """Verify Google ID token via Google's tokeninfo endpoint."""
    url = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data.get("aud") != GOOGLE_CLIENT_ID:
            return None, "Invalid audience"
        email = data.get("email", "")
        if email not in ALLOWED_EMAILS:
            return None, f"Email {email} not authorized"
        if data.get("email_verified") != "true":
            return None, "Email not verified"
        return data, None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return None, f"Token verification failed: {e.code} {body}"
    except Exception as e:
        return None, f"Token verification error: {str(e)}"


def get_session_cookie(handler):
    cookie_header = handler.headers.get("Cookie", "")
    if not cookie_header:
        return None
    cookie = SimpleCookie()
    try:
        cookie.load(cookie_header)
    except Exception:
        return None
    morsel = cookie.get("recoveri_session")
    if morsel:
        return morsel.value
    return None


def make_session_cookie(token):
    expires = datetime.now(timezone.utc) + timedelta(seconds=SESSION_MAX_AGE)
    expires_str = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return (
        f"recoveri_session={token}; "
        f"Path=/; "
        f"HttpOnly; "
        f"Secure; "
        f"SameSite=Lax; "
        f"Max-Age={SESSION_MAX_AGE}; "
        f"Expires={expires_str}"
    )


def clear_session_cookie():
    return (
        "recoveri_session=; "
        "Path=/; "
        "HttpOnly; "
        "Secure; "
        "SameSite=Lax; "
        "Max-Age=0; "
        "Expires=Thu, 01 Jan 1970 00:00:00 GMT"
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def now_iso():
    return datetime.now(timezone.utc).isoformat()


def ok_response(data, note=None):
    resp = {"status": "ok", "timestamp": now_iso(), "data": data}
    if note:
        resp["note"] = note
    return resp


def read_jsonl(path, limit=None):
    """Read a JSONL file and return list of parsed objects."""
    entries = []
    if not os.path.isfile(path):
        return entries
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    if limit and len(entries) > limit:
        entries = entries[-limit:]
    return entries


def read_json(path):
    """Read a JSON file and return parsed object."""
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return json.load(f)


def read_text(path):
    """Read a text/markdown file."""
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def latest_glob(pattern):
    """Return the latest file matching a glob pattern."""
    files = sorted(glob.glob(pattern))
    return files[-1] if files else None


def latest_glob_jsonl(pattern, limit=None):
    """Read the latest JSONL file matching a glob pattern."""
    path = latest_glob(pattern)
    if not path:
        return [], None
    return read_jsonl(path, limit=limit), path


# ---------------------------------------------------------------------------
# Endpoint handlers (unchanged from v3)
# ---------------------------------------------------------------------------

def handle_health():
    pattern = "/root/operations-logs/os-review-*.md"
    path = latest_glob(pattern)
    if not path:
        return ok_response({"health_score": None, "date": None, "content": None},
                           note="No OS review files found")
    content = read_text(path)
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(path))
    date_str = date_match.group(1) if date_match else None
    health_score = None
    if content:
        score_match = re.search(r"[Hh]ealth[\s_-]*[Ss]core[:\s]*(\d+)", content)
        if score_match:
            health_score = int(score_match.group(1))
        else:
            score_match = re.search(r"(\d+)\s*/\s*100", content)
            if score_match:
                health_score = int(score_match.group(1))
    return ok_response({
        "health_score": health_score,
        "date": date_str,
        "file": os.path.basename(path) if path else None,
        "content": content
    })


def handle_operations():
    path = "/root/operations-log/ops.jsonl"
    if not os.path.isfile(path):
        return ok_response({"entries": [], "total": 0, "today_count": 0},
                           note="ops.jsonl not found")
    entries = read_jsonl(path)
    total = len(entries)
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_count = 0
    for e in entries:
        ts = e.get("timestamp", "") or e.get("date", "") or e.get("time", "")
        if today_str in str(ts):
            today_count += 1
    last_50 = entries[-50:] if len(entries) > 50 else entries
    return ok_response({
        "entries": last_50,
        "total": total,
        "today_count": today_count
    })


def handle_requests():
    pattern = "/root/request-register/*.jsonl"
    entries, path = latest_glob_jsonl(pattern, limit=20)
    if not path:
        return ok_response({"entries": [], "file": None},
                           note="No request register files found")
    return ok_response({
        "entries": entries,
        "file": os.path.basename(path)
    })


def handle_errors():
    pattern = "/root/error-register/*.jsonl"
    files = sorted(glob.glob(pattern))
    if not files:
        return ok_response({"entries": [], "unresolved": [], "unresolved_count": 0},
                           note="No error register files found")
    all_entries = []
    for f in files:
        all_entries.extend(read_jsonl(f))
    unresolved = []
    for e in all_entries:
        resolved = e.get("resolved", None)
        if resolved is None or resolved is False or resolved == "false":
            unresolved.append(e)
    return ok_response({
        "entries": all_entries,
        "total": len(all_entries),
        "unresolved": unresolved,
        "unresolved_count": len(unresolved)
    })


def handle_skills():
    path = "/root/skill-registry/registry.jsonl"
    if not os.path.isfile(path):
        return ok_response({"skills": [], "total": 0},
                           note="registry.jsonl not found")
    entries = read_jsonl(path)
    return ok_response({"skills": entries, "total": len(entries)})


def handle_agents():
    config_path = "/root/.openclaw/openclaw.json"
    config = read_json(config_path)
    agents = []
    if config and "agents" in config:
        agent_list = config["agents"].get("list", config["agents"])
        if isinstance(agent_list, list):
            for a in agent_list:
                if isinstance(a, dict):
                    agents.append({
                        "name": a.get("name"),
                        "workspace": a.get("workspace"),
                        "model": a.get("model"),
                    })
                elif isinstance(a, str):
                    agents.append({"name": a, "workspace": None, "model": None})
    subagents = []
    sub_path = "/root/skill-registry/subagent-registry.jsonl"
    if os.path.isfile(sub_path):
        subagents = read_jsonl(sub_path)
    note = None if config else "openclaw.json not found"
    return ok_response({
        "agents": agents,
        "agent_count": len(agents),
        "subagents": subagents,
        "subagent_count": len(subagents)
    }, note=note)


def handle_costs():
    rates_path = "/root/cost-tracking/rates.json"
    rates = read_json(rates_path)
    daily_summaries = []
    daily_pattern = "/root/cost-tracking/daily-*.json"
    daily_files = sorted(glob.glob(daily_pattern))
    for f in daily_files[-7:]:
        d = read_json(f)
        if d:
            daily_summaries.append({"file": os.path.basename(f), "data": d})
    if not daily_summaries:
        daily_pattern2 = "/root/cost-tracking/daily-*.jsonl"
        daily_files2 = sorted(glob.glob(daily_pattern2))
        for f in daily_files2[-7:]:
            entries = read_jsonl(f)
            if entries:
                daily_summaries.append({"file": os.path.basename(f), "data": entries})
    note = None if rates else "rates.json not found"
    return ok_response({
        "rates": rates,
        "daily_summaries": daily_summaries
    }, note=note)


def handle_loop(loop_type):
    pattern = f"/root/loop-logs/{loop_type}-loop-*.jsonl"
    entries, path = latest_glob_jsonl(pattern)
    if not path:
        return ok_response({"entries": [], "count": 0, "latest_insight": None, "file": None},
                           note=f"No {loop_type} loop files found")
    latest_insight = None
    for e in reversed(entries):
        insight = e.get("insight") or e.get("summary") or e.get("result")
        if insight:
            latest_insight = insight
            break
    return ok_response({
        "entries": entries,
        "count": len(entries),
        "latest_insight": latest_insight,
        "file": os.path.basename(path)
    })


def handle_processes():
    base = "/root/shared-repository/artefacts"
    if not os.path.isdir(base):
        return ok_response({"ventures": []},
                           note="artefacts directory not found")
    ventures = []
    for item in sorted(os.listdir(base)):
        venture_path = os.path.join(base, item)
        if not os.path.isdir(venture_path):
            continue
        if item.startswith(".") or item in ("daily-research",):
            continue
        gates = []
        for entry in sorted(os.listdir(venture_path)):
            if re.match(r"gate-\d+", entry, re.IGNORECASE):
                gate_path = os.path.join(venture_path, entry)
                mtime = os.path.getmtime(gate_path)
                gates.append({
                    "name": entry,
                    "last_modified": datetime.fromtimestamp(mtime).isoformat()
                })
        ventures.append({
            "name": item,
            "gates": gates,
            "gate_count": len(gates),
            "latest_gate": gates[-1]["name"] if gates else None
        })
    return ok_response({"ventures": ventures, "venture_count": len(ventures)})


def handle_security():
    pattern = "/root/operations-logs/security-review-*.md"
    path = latest_glob(pattern)
    if not path:
        return ok_response({"content": None, "date": None},
                           note="No security review files found")
    content = read_text(path)
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(path))
    date_str = date_match.group(1) if date_match else None
    return ok_response({
        "content": content,
        "date": date_str,
        "file": os.path.basename(path)
    })


def handle_insights():
    lessons = []
    lessons_dir = "/root/shared-repository/lessons-learned/daily"
    if os.path.isdir(lessons_dir):
        files = sorted(glob.glob(os.path.join(lessons_dir, "*")))
        for f in files[-5:]:
            content = read_text(f)
            if content:
                lessons.append({"file": os.path.basename(f), "content": content})
    research = []
    research_dir = "/root/shared-repository/artefacts/daily-research"
    if os.path.isdir(research_dir):
        files = sorted(glob.glob(os.path.join(research_dir, "*")))
        for f in files[-5:]:
            content = read_text(f)
            if content:
                research.append({"file": os.path.basename(f), "content": content})
    note = None
    if not lessons and not research:
        note = "No insight files found"
    return ok_response({
        "lessons": lessons,
        "research": research
    }, note=note)


def handle_cron():
    """Read crontab and return structured job list."""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
        lines = result.stdout.strip().split("\n")
        jobs = []
        comment_buffer = ""
        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                # Store comment as name for next job
                comment_buffer = line.lstrip("# ").split("—")[0].strip()
                continue
            if not line:
                continue
            parts = line.split(None, 5)
            if len(parts) >= 6:
                schedule = " ".join(parts[:5])
                command = parts[5]
                # Extract script name
                script = command.split("/")[-1].split(" ")[0] if "/" in command else command
                name = comment_buffer if comment_buffer else script
                # Determine status by checking if output file exists for today
                status = "active"
                last_run = None
                jobs.append({
                    "name": name,
                    "schedule": schedule,
                    "command": command,
                    "script": script,
                    "status": status,
                    "last_run": last_run,
                })
                comment_buffer = ""
        return ok_response({"jobs": jobs, "total": len(jobs)})
    except Exception as e:
        return ok_response({"jobs": [], "total": 0}, note=f"cron error: {str(e)}")


def handle_agent_activity():
    """Agent activity tracker — reads from governance/agent-activity.jsonl."""
    activity_path = os.environ.get("AGENT_ACTIVITY_PATH",
                                    "/root/shared-repository/governance/agent-activity.jsonl")
    entries = []
    if os.path.isfile(activity_path):
        with open(activity_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

    # Get latest status per agent
    agent_latest = {}
    for e in entries:
        agent = e.get("agent", "Unknown")
        agent_latest[agent] = e

    # Classify agents by status
    now = datetime.now(timezone.utc)
    agents_summary = []
    for agent, entry in agent_latest.items():
        ts_str = entry.get("timestamp", "")
        try:
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            hours_ago = (now - ts).total_seconds() / 3600
        except Exception:
            hours_ago = 999

        status = entry.get("status", "UNKNOWN")
        color = "green"
        if status == "FAILED":
            color = "red"
        elif status == "IDLE" and hours_ago > 4:
            color = "red"
        elif status == "IDLE":
            color = "amber"
        elif status == "IN_PROGRESS":
            color = "blue"

        agents_summary.append({
            "agent": agent,
            "last_action": entry.get("action", "UNKNOWN"),
            "description": entry.get("description", ""),
            "task_id": entry.get("task_id", ""),
            "pillar": entry.get("pillar", ""),
            "status": status,
            "timestamp": ts_str,
            "hours_ago": round(hours_ago, 1),
            "color": color
        })

    agents_summary.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

    return ok_response({
        "agents": agents_summary,
        "total_entries": len(entries),
        "agents_tracked": len(agent_latest)
    })


def handle_research():
    """Aggregate research data from all cron-produced sources."""
    research_dirs = {
        "rss_news": "/root/shared-repository/data/rss-news/",
        "hackernews": "/root/shared-repository/data/hackernews/",
        "ai_trends": "/root/shared-repository/data/ai-trends/",
        "market_intel": "/root/shared-repository/data/market-intel/raw/",
        "etsy_scanner": "/root/shared-repository/data/etsy-scanner/",
        "google_trends": "/root/shared-repository/data/google-trends/"
    }

    result = {}
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for source, dirpath in research_dirs.items():
        if not os.path.isdir(dirpath):
            result[source] = {"status": "NO_DATA", "records": 0, "latest_file": None}
            continue

        files = sorted(glob.glob(os.path.join(dirpath, f"*{today}*")))
        if not files:
            files = sorted(glob.glob(os.path.join(dirpath, "*.jsonl")))

        if not files:
            result[source] = {"status": "NO_DATA", "records": 0, "latest_file": None}
            continue

        latest = files[-1]
        records = 0
        try:
            with open(latest) as f:
                for line in f:
                    if line.strip():
                        records += 1
        except Exception:
            pass

        result[source] = {
            "status": "ACTIVE",
            "records": records,
            "latest_file": os.path.basename(latest),
            "file_size": os.path.getsize(latest),
            "modified": datetime.fromtimestamp(
                os.path.getmtime(latest), tz=timezone.utc
            ).isoformat()
        }

    active = sum(1 for v in result.values() if v["status"] == "ACTIVE")
    return ok_response({
        "sources": result,
        "active_sources": active,
        "total_sources": len(result)
    })


def handle_overview():
    """Aggregate endpoint with RAG status badges."""
    now = datetime.now(timezone.utc)
    badges = {}
    summary = {}

    # Health
    try:
        health_resp = handle_health()
        health_data = health_resp["data"]
        score = health_data.get("health_score")
        summary["health_score"] = score
        if score is not None:
            if score < 60:
                badges["health"] = "RED"
            elif score < 70:
                badges["health"] = "AMBER"
            else:
                badges["health"] = "GREEN"
        else:
            badges["health"] = "AMBER"
    except Exception:
        badges["health"] = "AMBER"
        summary["health_score"] = None

    # Errors
    try:
        errors_resp = handle_errors()
        errors_data = errors_resp["data"]
        unresolved = errors_data.get("unresolved", [])
        summary["unresolved_errors"] = len(unresolved)
        has_critical = any(
            str(e.get("severity", "")).upper() == "CRITICAL" or
            str(e.get("level", "")).upper() == "CRITICAL"
            for e in unresolved
        )
        has_fabrication = any(
            "fabricat" in str(e.get("type", "")).lower() or
            "fabricat" in str(e.get("category", "")).lower() or
            "fabricat" in str(e.get("description", "")).lower()
            for e in unresolved
        )
        if has_critical or has_fabrication:
            badges["errors"] = "RED"
        elif len(unresolved) > 0:
            badges["errors"] = "AMBER"
        else:
            badges["errors"] = "GREEN"
        if has_fabrication:
            badges["fabrication"] = "RED"
        else:
            badges["fabrication"] = "GREEN"
    except Exception:
        badges["errors"] = "AMBER"
        badges["fabrication"] = "AMBER"
        summary["unresolved_errors"] = None

    # Cron / Agent activity
    try:
        cron_resp = handle_cron()
        cron_data = cron_resp["data"]
        jobs = cron_data.get("jobs", [])
        summary["cron_jobs"] = len(jobs)
        agent_badge = "GREEN"
        for job in jobs:
            last_run = job.get("last_run") or job.get("lastRun")
            if last_run:
                try:
                    if isinstance(last_run, str):
                        lr = datetime.fromisoformat(last_run.replace("Z", "+00:00"))
                    else:
                        lr = datetime.fromtimestamp(last_run, tz=timezone.utc)
                    delta = now - lr
                    hours = delta.total_seconds() / 3600
                    if hours > 12:
                        agent_badge = "RED"
                    elif hours > 4 and agent_badge != "RED":
                        agent_badge = "AMBER"
                except Exception:
                    pass
        badges["agent_activity"] = agent_badge
    except Exception:
        badges["agent_activity"] = "AMBER"
        summary["cron_jobs"] = None

    # Loops
    loop_summaries = {}
    for loop_type in ("social", "scrape", "trading"):
        try:
            loop_resp = handle_loop(loop_type)
            loop_data = loop_resp["data"]
            loop_summaries[loop_type] = {
                "count": loop_data.get("count", 0),
                "latest_insight": loop_data.get("latest_insight")
            }
        except Exception:
            loop_summaries[loop_type] = {"count": 0, "latest_insight": None}
    summary["loops"] = loop_summaries

    # Processes
    try:
        proc_resp = handle_processes()
        proc_data = proc_resp["data"]
        ventures = proc_data.get("ventures", [])
        summary["venture_count"] = len(ventures)
        process_badge = "GREEN"
        for v in ventures:
            gates = v.get("gates", [])
            if gates:
                last_gate = gates[-1]
                lm = last_gate.get("last_modified")
                if lm:
                    try:
                        lm_dt = datetime.fromisoformat(lm)
                        if lm_dt.tzinfo is None:
                            lm_dt = lm_dt.replace(tzinfo=timezone.utc)
                        delta = now - lm_dt
                        hours = delta.total_seconds() / 3600
                        if hours > 48:
                            process_badge = "RED"
                        elif hours > 24 and process_badge != "RED":
                            process_badge = "AMBER"
                    except Exception:
                        pass
        badges["processes"] = process_badge
    except Exception:
        badges["processes"] = "AMBER"
        summary["venture_count"] = None

    # Approvals pipeline
    try:
        apr_resp = handle_approvals()
        apr_data = apr_resp["data"]
        awaiting = apr_data.get("awaiting", 0)
        summary["approvals_awaiting"] = awaiting
        summary["approvals"] = {
            "total_pending": awaiting,
            "overdue": apr_data.get("overdue_count", 0),
            "oldest_hours": apr_data.get("oldest_unresolved_hours", 0)
        }
        critical_approvals = sum(1 for e in apr_data.get("awaiting_entries", [])
                                 if e.get("priority") == "CRITICAL")
        if critical_approvals > 0:
            badges["approvals"] = "RED"
        elif awaiting > 3:
            badges["approvals"] = "AMBER"
        else:
            badges["approvals"] = "GREEN"
    except Exception:
        badges["approvals"] = "AMBER"
        summary["approvals_awaiting"] = None

    # Backlog
    try:
        bl_resp = handle_backlog()
        bl_data = bl_resp["data"]
        summary["backlog"] = {
            "total": bl_data.get("total", 0),
            "critical": bl_data.get("by_priority", {}).get("CRITICAL", 0),
            "blocked": bl_data.get("by_status", {}).get("BLOCKED", 0)
        }
    except Exception:
        summary["backlog"] = {"total": 0, "critical": 0, "blocked": 0}

    # Incidents
    try:
        inc_resp = handle_incidents()
        inc_data = inc_resp["data"]
        open_inc = inc_data.get("open", 0)
        fab_count = inc_data.get("fabrication_count", 0)
        summary["open_incidents"] = open_inc
        summary["fabrication_count"] = fab_count
        summary["incidents"] = {
            "total": inc_data.get("total", 0),
            "open": open_inc,
            "fabrication_count": fab_count
        }
        if fab_count > 0:
            badges["fabrication"] = "RED"
        if open_inc > 0:
            badges["incidents"] = "RED"
        else:
            badges["incidents"] = "GREEN"
    except Exception:
        badges["incidents"] = "AMBER"

    # Market Intel
    try:
        mi_resp = handle_market_intel()
        mi_data = mi_resp["data"]
        summary["market_intel"] = {
            "sources_active": mi_data.get("sources_active", 0),
            "records_today": mi_data.get("total_records_today", 0),
            "status": mi_data.get("cron_status", "UNKNOWN")
        }
        if mi_data.get("sources_active", 0) > 0:
            badges["market_intel"] = "GREEN"
        else:
            badges["market_intel"] = "AMBER"
    except Exception:
        badges["market_intel"] = "AMBER"
        summary["market_intel"] = {"sources_active": 0, "records_today": 0, "status": "ERROR"}

    # Gatekeeper
    try:
        gk_resp = handle_gatekeeper()
        gk_data = gk_resp["data"]
        summary["gatekeeper"] = {
            "validations_today": gk_data.get("validations_today", 0),
            "status": gk_data.get("status", "UNKNOWN")
        }
        if gk_data.get("status") == "DEPLOYED":
            badges["gatekeeper"] = "GREEN"
        else:
            badges["gatekeeper"] = "AMBER"
    except Exception:
        badges["gatekeeper"] = "AMBER"
        summary["gatekeeper"] = {"validations_today": 0, "status": "ERROR"}

    # Swarm status
    summary["swarm_status"] = "PHASE_1_APPROVED"

    # Agent activity summary
    try:
        aa = handle_agent_activity()
        aa_data = aa.get("data", {})
        summary["agent_activity"] = {
            "total_agents": aa_data.get("total", 0),
            "active": aa_data.get("active", 0),
            "failed": aa_data.get("failed", 0),
            "idle_over_4h": aa_data.get("idle_over_4h", 0),
        }
    except Exception:
        summary["agent_activity"] = {"total_agents": 0, "active": 0, "failed": 0, "idle_over_4h": 0}

    # Compute overall
    if "RED" in badges.values():
        overall = "RED"
    elif "AMBER" in badges.values():
        overall = "AMBER"
    else:
        overall = "GREEN"

    return ok_response({
        "overall_status": overall,
        "badges": badges,
        "summary": summary
    })




# ---------------------------------------------------------------------------
# Governance data endpoints (approvals, backlog, incidents) — upgraded with
# query params, age calculation, auto-OVERDUE promotion
# ---------------------------------------------------------------------------

def _parse_query_params(handler=None):
    """Parse query string from the current request. Returns dict."""
    # This is called from handler context; for direct Python calls return empty
    return {}


def handle_approvals():
    path = DATA_PATHS["approvals"]
    if not os.path.isfile(path):
        return ok_response({"entries": [], "total": 0, "awaiting": 0, "decided": 0,
                            "by_stage": {}, "oldest_unresolved_hours": 0, "overdue_count": 0},
                           note="approvals.jsonl not found")
    entries = read_jsonl(path)
    now = datetime.now(timezone.utc)

    # Auto-calculate age_hours and auto-promote OVERDUE
    for e in entries:
        cd = e.get("created_date")
        if cd:
            try:
                created = datetime.fromisoformat(cd.replace("Z", "+00:00"))
                e["age_hours"] = int((now - created).total_seconds() / 3600)
            except Exception:
                e["age_hours"] = e.get("age_hours", 0)
        if e.get("stage") == "AWAITING_DECISION" and e.get("age_hours", 0) > 48:
            e["stage"] = "OVERDUE"

    awaiting = [e for e in entries if e.get("stage") in ("INCOMING", "IN_REVIEW", "AWAITING_DECISION", "OVERDUE")]
    decided = [e for e in entries if e.get("stage") == "DECIDED"]

    by_stage = {}
    for e in entries:
        s = e.get("stage", "UNKNOWN")
        by_stage[s] = by_stage.get(s, 0) + 1

    oldest = max((e.get("age_hours", 0) for e in awaiting), default=0)

    return ok_response({
        "entries": entries,
        "total": len(entries),
        "awaiting": len(awaiting),
        "awaiting_entries": awaiting,
        "decided": len(decided),
        "decided_entries": decided,
        "by_stage": by_stage,
        "oldest_unresolved_hours": oldest,
        "overdue_count": by_stage.get("OVERDUE", 0)
    })


def handle_backlog():
    path = DATA_PATHS["backlog"]
    if not os.path.isfile(path):
        return ok_response({"entries": [], "total": 0, "by_status": {}, "by_priority": {}, "by_sprint": {}},
                           note="backlog.jsonl not found")
    entries = read_jsonl(path)
    by_status = {}
    by_priority = {}
    by_sprint = {}
    for e in entries:
        s = e.get("status", "UNKNOWN")
        p = e.get("priority", "UNKNOWN")
        sp = str(e.get("sprint", "BACKLOG"))
        by_status[s] = by_status.get(s, 0) + 1
        by_priority[p] = by_priority.get(p, 0) + 1
        by_sprint[sp] = by_sprint.get(sp, 0) + 1
    return ok_response({
        "entries": entries,
        "total": len(entries),
        "by_status": by_status,
        "by_priority": by_priority,
        "by_sprint": by_sprint
    })


def handle_incidents():
    path = DATA_PATHS["incidents"]
    if not os.path.isfile(path):
        return ok_response({"entries": [], "total": 0, "open_count": 0, "fabrication_count": 0,
                            "by_severity": {}, "by_type": {}},
                           note="incidents.jsonl not found")
    entries = read_jsonl(path)
    open_incidents = [e for e in entries if e.get("status") not in ("RESOLVED", "CLOSED")]
    fabrication_count = sum(1 for e in entries if e.get("type") == "FABRICATION")
    by_severity = {}
    by_type = {}
    for e in entries:
        sev = e.get("severity", "UNKNOWN")
        typ = e.get("type", "UNKNOWN")
        by_severity[sev] = by_severity.get(sev, 0) + 1
        by_type[typ] = by_type.get(typ, 0) + 1
    return ok_response({
        "entries": entries,
        "total": len(entries),
        "open": len(open_incidents),
        "open_count": len(open_incidents),
        "fabrication_count": fabrication_count,
        "by_severity": by_severity,
        "by_type": by_type
    })


# ---------------------------------------------------------------------------
# Swarm mechanics endpoints (market-intel, swarm-feedback, skill-evolution,
# gatekeeper, hardcode-scan)
# ---------------------------------------------------------------------------

def handle_market_intel():
    raw_dir = DATA_PATHS["market_intel"]
    if not os.path.isdir(raw_dir):
        return ok_response({"sources": {}, "total_records_today": 0, "total_records_all_time": 0,
                            "latest_records": [], "cron_status": "UNKNOWN"},
                           note="market-intel directory not found")

    today_str = datetime.now().strftime("%Y-%m-%d")
    sources = {}
    all_latest = []
    total_today = 0
    total_all = 0

    for fname in sorted(glob.glob(os.path.join(raw_dir, "*.jsonl"))):
        entries = read_jsonl(fname)
        if not entries:
            continue
        source_name = os.path.basename(fname).split("-")[0]  # e.g., "coingecko"
        is_today = today_str in os.path.basename(fname)

        last_entry = entries[-1] if entries else {}
        records_in_file = sum(e.get("record_count", 0) for e in entries)
        total_all += records_in_file

        if is_today:
            total_today += records_in_file
            sources[source_name] = {
                "status": "LIVE",
                "last_fetch": last_entry.get("timestamp"),
                "records_today": records_in_file,
                "polls_today": len(entries),
                "data_type": last_entry.get("data_type")
            }
            # Extract latest data items for display
            if last_entry.get("data") and last_entry.get("data_type") == "crypto":
                for item in last_entry["data"][:5]:
                    all_latest.append({
                        "source": source_name,
                        "asset": item.get("symbol"),
                        "name": item.get("name"),
                        "price_usd": item.get("price_usd"),
                        "change_24h": item.get("change_24h_pct"),
                        "market_cap": item.get("market_cap"),
                        "timestamp": last_entry.get("timestamp")
                    })
            elif last_entry.get("data") and last_entry.get("data_type") == "stocks":
                for item in last_entry["data"][:5]:
                    all_latest.append({
                        "source": source_name,
                        "asset": item.get("ticker"),
                        "category": item.get("category"),
                        "price": item.get("price"),
                        "change_pct": item.get("change_pct"),
                        "volume": item.get("volume"),
                        "timestamp": last_entry.get("timestamp")
                    })
            elif last_entry.get("data") and last_entry.get("data_type") == "news":
                for item in last_entry["data"][:3]:
                    all_latest.append({
                        "source": source_name,
                        "headline": item.get("headline"),
                        "news_source": item.get("source"),
                        "category": item.get("category"),
                        "timestamp": last_entry.get("timestamp")
                    })

    # Check cron status
    cron_status = "ACTIVE" if sources else "INACTIVE"

    return ok_response({
        "sources": sources,
        "total_records_today": total_today,
        "total_records_all_time": total_all,
        "latest_records": all_latest[:15],
        "cron_status": cron_status,
        "sources_active": len(sources)
    })


def handle_swarm_feedback():
    path = DATA_PATHS["swarm_feedback"]
    if not os.path.isfile(path):
        return ok_response({
            "total_feedback_entries": 0,
            "by_swarm": {},
            "avg_quality": None,
            "idle_workers": [],
            "schema_compliance": None,
            "status": "AWAITING_DATA"
        }, note="Swarm 6 not yet live — feedback.jsonl not found")

    entries = read_jsonl(path)
    by_swarm = {}
    qualities = []
    for e in entries:
        sw = e.get("swarm", "unknown")
        by_swarm[sw] = by_swarm.get(sw, 0) + 1
        q = e.get("quality_score")
        if q is not None:
            qualities.append(q)

    return ok_response({
        "total_feedback_entries": len(entries),
        "by_swarm": by_swarm,
        "avg_quality": round(sum(qualities) / len(qualities), 2) if qualities else None,
        "idle_workers": [],
        "schema_compliance": None,
        "status": "ACTIVE" if entries else "AWAITING_DATA"
    })


def handle_skill_evolution():
    routing_path = DATA_PATHS["skill_evolution_routing"]
    patterns_dir = DATA_PATHS["skill_evolution_patterns"]

    proposals = []
    if os.path.isfile(routing_path):
        proposals = read_jsonl(routing_path)

    pattern_count = 0
    if os.path.isdir(patterns_dir):
        for fname in glob.glob(os.path.join(patterns_dir, "*.jsonl")):
            pattern_count += len(read_jsonl(fname))

    pending = [p for p in proposals if p.get("status") == "PENDING"]
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)
    this_week = []
    for p in proposals:
        ts = p.get("timestamp") or p.get("created")
        if ts:
            try:
                dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
                if dt >= week_ago:
                    this_week.append(p)
            except Exception:
                pass

    ab_tests = [p for p in proposals if p.get("status") == "AB_TEST"]

    return ok_response({
        "proposals_pending": len(pending),
        "proposals_this_week": len(this_week),
        "ab_tests_active": len(ab_tests),
        "skill_improvement_rate": None,
        "patterns_identified": pattern_count,
        "status": "AWAITING_SWARM_6" if not proposals and pattern_count == 0 else "ACTIVE"
    })


def handle_gatekeeper():
    path = DATA_PATHS["gatekeeper_log"]
    if not os.path.isfile(path):
        return ok_response({"validations_today": 0, "pass_rate": None, "fail_rate": None,
                            "by_validator": {}, "recent_failures": [], "status": "NOT_FOUND"},
                           note="validations.jsonl not found")
    entries = read_jsonl(path)
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_entries = [e for e in entries if today_str in str(e.get("timestamp", ""))]

    total = len(entries)
    passed = sum(1 for e in entries if e.get("overall") == "PASS")
    failed = sum(1 for e in entries if e.get("overall") == "FAIL")

    by_validator = {}
    for e in entries:
        validators = e.get("validators", {})
        for vname, vstatus in validators.items():
            if vname not in by_validator:
                by_validator[vname] = {"pass": 0, "fail": 0, "skip": 0}
            key = str(vstatus).lower()
            if key in by_validator[vname]:
                by_validator[vname][key] += 1

    failures = [e for e in entries if e.get("overall") == "FAIL"]
    recent_failures = []
    for f in failures[-5:]:
        recent_failures.append({
            "req_id": f.get("req_id"),
            "timestamp": f.get("timestamp"),
            "reason": f.get("overall_reason"),
            "summary": f.get("summary")
        })

    return ok_response({
        "validations_total": total,
        "validations_today": len(today_entries),
        "pass_count": passed,
        "fail_count": failed,
        "pass_rate": round(passed / total * 100, 1) if total > 0 else None,
        "fail_rate": round(failed / total * 100, 1) if total > 0 else None,
        "by_validator": by_validator,
        "recent_failures": recent_failures,
        "status": "DEPLOYED"
    })


def handle_hardcode_scan():
    scan_dir = DATA_PATHS["hardcode_scan"]
    pattern = os.path.join(scan_dir, "hardcode-scan-*.jsonl")
    files = sorted(glob.glob(pattern))
    if not files:
        return ok_response({"last_scan": None, "files_scanned": 0, "findings": {},
                            "critical_findings": [], "total_findings": 0, "status": "NO_SCAN"},
                           note="No hardcode scan files found")

    latest = files[-1]
    entries = read_jsonl(latest)

    by_severity = {}
    critical_findings = []
    files_set = set()
    for e in entries:
        sev = e.get("severity", "UNKNOWN")
        by_severity[sev] = by_severity.get(sev, 0) + 1
        files_set.add(e.get("file", ""))
        if sev == "CRITICAL":
            critical_findings.append({
                "file": e.get("file"),
                "line": e.get("line"),
                "pattern": e.get("pattern_matched"),
                "preview": e.get("value_preview"),
                "recommendation": e.get("recommendation")
            })

    last_ts = entries[0].get("timestamp") if entries else None
    status = "CLEAN" if by_severity.get("CRITICAL", 0) == 0 else "CRITICAL_FINDINGS"

    return ok_response({
        "last_scan": last_ts,
        "files_scanned": len(files_set),
        "findings": by_severity,
        "total_findings": len(entries),
        "critical_findings": critical_findings,
        "status": status
    })


# ---------------------------------------------------------------------------
# Pillar endpoints (studios, core, social, traders)
# ---------------------------------------------------------------------------

def handle_pillar_studios():
    # Gate progress from processes
    ventures = []
    try:
        proc_resp = handle_processes()
        all_ventures = proc_resp["data"].get("ventures", [])
        ventures = [v for v in all_ventures if "studio" in v.get("name", "").lower()
                    or "etsy" in v.get("name", "").lower()
                    or "recoveri" in v.get("name", "").lower()]
    except Exception:
        pass

    # CS pipeline
    cs_path = DATA_PATHS["cs_pipeline"]
    cs_data = {"tickets_today": 0, "by_bucket": {}, "avg_resolution_hours": None, "escalations_today": 0}
    if os.path.isfile(cs_path):
        tickets = read_jsonl(cs_path)
        today_str = datetime.now().strftime("%Y-%m-%d")
        today_tickets = [t for t in tickets if today_str in str(t.get("timestamp", ""))]
        cs_data["tickets_today"] = len(today_tickets)
        for t in tickets:
            b = t.get("bucket", "unknown")
            cs_data["by_bucket"][b] = cs_data["by_bucket"].get(b, 0) + 1
        cs_data["escalations_today"] = sum(1 for t in today_tickets if t.get("escalated"))

    venture_summaries = []
    for v in ventures:
        venture_summaries.append({
            "name": v.get("name"),
            "current_gate": v.get("gate_count", 0),
            "gate_status": "EXECUTING",
            "products_in_pipeline": 0,
            "products_listed": 0,
            "revenue": 0
        })

    return ok_response({
        "pillar": "STUDIOS",
        "status": "ACTIVE",
        "ventures": venture_summaries,
        "cs_pipeline": cs_data,
        "costs": {"token_spend_today": 0, "monthly_total": 0}
    })


def handle_pillar_core():
    scrape_count = 0
    try:
        scrape_resp = handle_loop("scrape")
        scrape_count = scrape_resp["data"].get("count", 0)
    except Exception:
        pass

    return ok_response({
        "pillar": "CORE",
        "status": "ACTIVE",
        "ventures": [],
        "opportunities": 0,
        "scraping_loop_cycles_today": scrape_count,
        "pipeline_value": 0,
        "status_detail": "Pre-revenue. Scraping loop building opportunity pipeline."
    })


def handle_pillar_social():
    social_count = 0
    try:
        social_resp = handle_loop("social")
        social_count = social_resp["data"].get("count", 0)
    except Exception:
        pass

    return ok_response({
        "pillar": "SOCIAL",
        "status": "ACTIVE",
        "ventures": [],
        "social_loop_cycles_today": social_count,
        "content_in_queue": 0,
        "channels_active": [],
        "status_detail": "Pre-posting. Social loop building engagement intelligence."
    })


def handle_pillar_traders():
    mi_data = {"sources_active": 0, "total_records_today": 0}
    try:
        mi_resp = handle_market_intel()
        mi_data["sources_active"] = mi_resp["data"].get("sources_active", 0)
        mi_data["total_records_today"] = mi_resp["data"].get("total_records_today", 0)
    except Exception:
        pass

    trading_count = 0
    try:
        trading_resp = handle_loop("trading")
        trading_count = trading_resp["data"].get("count", 0)
    except Exception:
        pass

    return ok_response({
        "pillar": "TRADERS",
        "status": "ACTIVE",
        "ventures": [],
        "signals_today": mi_data["total_records_today"],
        "sources_active": mi_data["sources_active"],
        "trading_loop_cycles_today": trading_count,
        "paper_trades": 0,
        "status_detail": f"Market data pipeline live. {mi_data['sources_active']} sources."
    })


# ---------------------------------------------------------------------------
# Route table
# ---------------------------------------------------------------------------


def handle_agent_activity():
    """Return agent activity tracker data."""
    path = DATA_PATHS["agent_activity"]
    entries = read_jsonl(path) if os.path.exists(path) else []
    now = datetime.now(timezone.utc)
    agents = {}
    for e in entries:
        agent = e.get("agent", "unknown")
        # Keep latest entry per agent
        if agent not in agents or e.get("timestamp", "") > agents[agent].get("timestamp", ""):
            agents[agent] = e
    # Calculate time since last action
    agent_list = []
    for name, data in sorted(agents.items()):
        ts = data.get("timestamp")
        hours_idle = None
        if ts:
            try:
                last = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                hours_idle = round((now - last).total_seconds() / 3600, 1)
            except Exception:
                pass
        rag = "GREEN"
        if data.get("status") == "FAILED":
            rag = "RED"
        elif hours_idle and hours_idle > 4:
            rag = "RED"
        elif hours_idle and hours_idle > 2:
            rag = "AMBER"
        agent_list.append({
            "agent": name,
            "last_action": data.get("action"),
            "description": data.get("description"),
            "status": data.get("status"),
            "timestamp": ts,
            "hours_since": hours_idle,
            "rag": rag,
            "pillar": data.get("pillar"),
        })
    failed = sum(1 for a in agent_list if a["status"] == "FAILED")
    idle_4h = sum(1 for a in agent_list if (a.get("hours_since") or 0) > 4)
    return ok_response({
        "agents": agent_list,
        "total": len(agent_list),
        "failed": failed,
        "idle_over_4h": idle_4h,
        "active": sum(1 for a in agent_list if a["status"] in ("ACTIVE", "COMPLETE", "IN_PROGRESS")),
    })

def handle_research(source):
    """Generic research data endpoint."""
    dir_map = {
        "etsy-scanner": DATA_PATHS.get("research_etsy", ""),
        "trends": DATA_PATHS.get("research_trends", ""),
        "news": None,  # Aggregate
    }
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    
    if source == "news":
        # Aggregate HN + RSS + AI
        results = {"sources": {}}
        for name, key in [("hackernews", "research_hn"), ("rss", "research_rss"), ("ai_trends", "research_ai")]:
            d = DATA_PATHS.get(key, "")
            files = sorted(glob.glob(os.path.join(d, f"*-{date_str}.jsonl"))) if d else []
            entries = []
            for fp in files:
                entries.extend(read_jsonl(fp))
            results["sources"][name] = {
                "records_today": len(entries),
                "latest": entries[-1] if entries else None,
            }
        results["total_sources"] = len(results["sources"])
        return ok_response(results)
    
    d = dir_map.get(source, "")
    if not d:
        return ok_response({"error": f"Unknown research source: {source}"})
    files = sorted(glob.glob(os.path.join(d, f"*-{date_str}.jsonl")))
    entries = []
    for fp in files:
        entries.extend(read_jsonl(fp))
    return ok_response({
        "source": source,
        "records_today": len(entries),
        "entries": entries[-10:],
    })

ROUTES = {
    "/api/health": handle_health,
    "/api/operations": handle_operations,
    "/api/requests": handle_requests,
    "/api/errors": handle_errors,
    "/api/skills": handle_skills,
    "/api/agents": handle_agents,
    "/api/costs": handle_costs,
    "/api/loops/social": lambda: handle_loop("social"),
    "/api/loops/scrape": lambda: handle_loop("scrape"),
    "/api/loops/trading": lambda: handle_loop("trading"),
    "/api/processes": handle_processes,
    "/api/security": handle_security,
    "/api/insights": handle_insights,
    "/api/cron": handle_cron,
    "/api/overview": handle_overview,
    "/api/approvals": handle_approvals,
    "/api/backlog": handle_backlog,
    "/api/incidents": handle_incidents,
    "/api/market-intel": handle_market_intel,
    "/api/swarm-feedback": handle_swarm_feedback,
    "/api/skill-evolution": handle_skill_evolution,
    "/api/gatekeeper": handle_gatekeeper,
    "/api/hardcode-scan": handle_hardcode_scan,
    "/api/pillars/studios": handle_pillar_studios,
    "/api/pillars/core": handle_pillar_core,
    "/api/pillars/social": handle_pillar_social,
    "/api/pillars/traders": handle_pillar_traders,
    "/api/agent-activity": handle_agent_activity,
    "/api/research/etsy-scanner": lambda: handle_research("etsy-scanner"),
    "/api/research/trends": lambda: handle_research("trends"),
    "/api/research/news": lambda: handle_research("news"),
}


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------

class DashboardHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def log_message(self, format, *args):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys.stdout.write(f"[{ts}] {self.address_string()} - {format % args}\n")
        sys.stdout.flush()

    def send_cors_headers(self):
        origin = self.headers.get("Origin", "https://board.craab.io")
        self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def send_json(self, data, status=200, extra_headers=None):
        body = json.dumps(data, indent=2, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_cors_headers()
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _check_auth(self):
        """Return True if session is valid."""
        token = get_session_cookie(self)
        return validate_session(token) is not None

    def _redirect_to_login(self):
        self.send_response(302)
        self.send_header("Location", "/login.html")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"

        # --- Auth-exempt paths ---
        if path == "/login.html":
            super().do_GET()
            return

        if path == "/auth/callback":
            # OAuth 2.0 callback — exchange authorization code for tokens
            parsed_qs = parse_qs(parsed.query)
            code = parsed_qs.get("code", [""])[0]
            error = parsed_qs.get("error", [""])[0]

            if error:
                self.log_message("AUTH CALLBACK ERROR: %s", error)
                self._auth_error(error)
                return

            if not code:
                self._auth_error("Missing authorization code")
                return

            try:
                # Exchange code for tokens
                token_data = urllib.parse.urlencode({
                    "code": code,
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "redirect_uri": GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code",
                }).encode("utf-8")

                req = urllib.request.Request(
                    "https://oauth2.googleapis.com/token",
                    data=token_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    tokens = json.loads(resp.read().decode("utf-8"))

                id_token = tokens.get("id_token", "")
                if not id_token:
                    self._auth_error("No ID token in response")
                    return

                # Verify the ID token
                token_info, err = verify_google_token(id_token)
                if err:
                    self.log_message("AUTH DENIED: %s", err)
                    self._auth_error(err)
                    return

                email = token_info["email"]
                self.log_message("AUTH OK: %s", email)

                # Create session and set cookie
                purge_expired_sessions()
                session_token = create_session(email)
                cookie_val = make_session_cookie(session_token)

                # Use 200 + meta refresh (not 302) — browsers reliably process
                # Set-Cookie on 200 responses but can skip them on 302s via HTTP/1.0
                body = b"<!DOCTYPE html><html><head><meta http-equiv='refresh' content='0;url=/'></head><body>Signing in...</body></html>"
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Set-Cookie", cookie_val)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)

            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", errors="replace")
                self.log_message("TOKEN EXCHANGE ERROR: %s %s", e.code, body)
                self._auth_error(f"Token exchange failed: {e.code}")
            except Exception as e:
                self.log_message("AUTH CALLBACK ERROR: %s", str(e))
                self._auth_error(str(e))
            return

        if path == "/auth/logout":
            token = get_session_cookie(self)
            if token and token in SESSIONS:
                del SESSIONS[token]
            self.send_response(302)
            self.send_header("Set-Cookie", clear_session_cookie())
            self.send_header("Location", "/login.html")
            self.end_headers()
            return

        # --- All other paths require auth ---
        if not self._check_auth():
            if path.startswith("/api/"):
                self.send_json({"status": "error", "message": "Not authenticated"}, status=401)
                return
            self._redirect_to_login()
            return

        # API routes
        if path in ROUTES:
            try:
                result = ROUTES[path]()
                self.send_json(result)
            except Exception as e:
                self.log_message("ERROR on %s: %s", path, str(e))
                self.send_json({
                    "status": "error",
                    "timestamp": now_iso(),
                    "error": str(e),
                    "data": None
                }, status=500)
            return

        # Unknown API path
        if path.startswith("/api/"):
            self.send_json({
                "status": "error",
                "timestamp": now_iso(),
                "error": f"Unknown endpoint: {path}",
                "data": None
            }, status=404)
            return

        # Static files — delegate to SimpleHTTPRequestHandler
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/auth/google":
            self._handle_google_auth()
            return

        self.send_json({"status": "error", "message": "Not found"}, status=404)

    def _handle_google_auth(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0 or content_length > 65536:
                self._auth_error("Invalid request body")
                return

            body = self.rfile.read(content_length)

            # Support both JSON and form-encoded POST
            content_type = self.headers.get("Content-Type", "")
            if "application/json" in content_type:
                payload = json.loads(body.decode("utf-8"))
                credential = payload.get("credential", "")
            else:
                # Form-encoded: credential=TOKEN
                from urllib.parse import parse_qs as _pqs
                params = _pqs(body.decode("utf-8"))
                credential = params.get("credential", [""])[0]

            if not credential:
                self._auth_error("Missing credential")
                return

            # Verify with Google
            token_info, err = verify_google_token(credential)
            if err:
                self.log_message("AUTH DENIED: %s", err)
                self._auth_error(err)
                return

            email = token_info["email"]
            self.log_message("AUTH OK: %s", email)

            # Create a short-lived auth code
            auth_code = secrets.token_urlsafe(32)
            AUTH_CODES[auth_code] = {"email": email, "created": time.time()}

            # Purge expired auth codes
            now = time.time()
            expired = [c for c, d in AUTH_CODES.items() if now - d["created"] > AUTH_CODE_MAX_AGE]
            for c in expired:
                del AUTH_CODES[c]

            # Return the code — login page will redirect to GET /auth/complete?code=XXX
            self.send_json({"status": "ok", "code": auth_code})
        except json.JSONDecodeError:
            self._auth_error("Invalid JSON")
        except Exception as e:
            self.log_message("AUTH ERROR: %s", str(e))
            self._auth_error(f"Auth error: {str(e)}")

    def _auth_error(self, message):
        """Redirect back to login with error message."""
        from urllib.parse import quote
        self.send_response(302)
        self.send_header("Location", f"/login.html?error={quote(message)}")
        self.send_header("Content-Length", "0")
        self.end_headers()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs(STATIC_DIR, exist_ok=True)

    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.isfile(index_path):
        with open(index_path, "w") as f:
            f.write("<!DOCTYPE html><html><head><title>Recoveri Dashboard</title></head>"
                    "<body><h1>Recoveri Dashboard</h1><p>API server running on port "
                    f"{PORT}.</p></body></html>\n")

    server = http.server.HTTPServer(("0.0.0.0", PORT), DashboardHandler)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
          f"Recoveri Dashboard API server v4.0 starting on port {PORT}")
    print(f"  Static files: {STATIC_DIR}")
    print(f"  Endpoints: {len(ROUTES)}")
    print(f"  Auth: Google Sign-In ({', '.join(ALLOWED_EMAILS)})")
    print(f"  Routes: {', '.join(sorted(ROUTES.keys()))}")
    sys.stdout.flush()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
