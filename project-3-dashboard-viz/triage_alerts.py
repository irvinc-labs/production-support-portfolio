import os
import sys
import json
import urllib.request
import pandas as pd

# 1. Path & Configuration Calculation
CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_SCRIPT_DIR)
csv_path = os.path.join(BASE_DIR, "metrics_history.csv")

SLO_AVAILABILITY_MIN = 80.0
CRITICAL_P99_LATENCY_MAX = 800.0  # ms

# Fetch webhook from environment context
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

# SECURE FALLBACK LOGIC FOR WSL PORTFOLIO ENVIRONMENT
if not SLACK_WEBHOOK_URL and os.path.exists(os.path.join(BASE_DIR, ".env")):
    try:
        with open(os.path.join(BASE_DIR, ".env"), "r") as env_f:
            for line in env_f:
                if line.startswith("SLACK_WEBHOOK_URL"):
                    SLACK_WEBHOOK_URL = line.split("=")[1].replace('"', '').replace("'", "").strip()
    except Exception:
        pass

# 2. Safely read dataset matrix
try:
    df = pd.read_csv(csv_path)
    df.columns = [col.lower().strip() for col in df.columns]
except FileNotFoundError:
    print(f"[✗] Error: Missing telemetry file at {csv_path}")
    sys.exit(1)

if df.empty:
    print("[✗] Error: Telemetry matrix is empty.")
    sys.exit(1)

# 3. Inspect Latest Operational State
latest_state = df.iloc[-1]
interval_idx = len(df) - 1

avail_col = next((c for c in df.columns if 'avail' in c), None)
p99_col = next((c for c in df.columns if 'p99' in c), None)

current_avail = float(latest_state[avail_col]) if avail_col else 100.0
current_p99 = float(latest_state[p99_col]) if p99_col else 0.0

print(f"[*] Analysing Interval #{interval_idx} | Availability: {current_avail}% | p99: {current_p99}ms")

# 4. Evaluate SRE Threshold Breach Rules
breach_detected = False
incident_reasons = []

if current_avail < SLO_AVAILABILITY_MIN:
    breach_detected = True
    incident_reasons.append(f"• *CRITICAL:* Availability dropped to `{current_avail}%`, breaching the {SLO_AVAILABILITY_MIN}% SLO Baseline target.")

if current_p99 > CRITICAL_P99_LATENCY_MAX:
    breach_detected = True
    incident_reasons.append(f"• *WARNING:* Tail Latency (p99) spiked to `{current_p99}ms`, exceeding the maximum {CRITICAL_P99_LATENCY_MAX}ms limit.")

# 5. Dispatch Alerts
if breach_detected:
    print(f"[🚨] SLO Breach detected across {len(incident_reasons)} rule(s)!")
    
    if not SLACK_WEBHOOK_URL:
        print("[!] Slack notification skipped: SLACK_WEBHOOK_URL variable is not exported.")
        sys.exit(0)
        
    # Build clean, recruiter-grade Slack Block Kit payload
    breach_details_text = "\n".join(incident_reasons)
    slack_payload = {
        "attachments": [
            {
                "color": "#e01e5a", # SRE Incident Red
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"🚨 *[SRE PRODUCTION ALERT] Incident Triggered: INC-{interval_idx:05d}*"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Severity:*\nP2 - High Impact"},
                            {"type": "mrkdwn", "text": f"*Environment:*\nWSL-Monorepo Sim"},
                            {"type": "mrkdwn", "text": f"*Metric Frame:*\nInterval #{interval_idx}"},
                            {"type": "mrkdwn", "text": f"*Repository:*\n<https://github.com|production-support-portfolio>"}
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Breach Root Cause Log(s):*\n{breach_details_text}"
                        }
                    }
                ]
            }
        ]
    }
    
    # Fire the payload via native Python libraries to avoid curl dependency limits
    try:
        req = urllib.request.Request(
            SLACK_WEBHOOK_URL,
            data=json.dumps(slack_payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            if response.status == 200 or response.status == 204:
                print("[✓] Incident notification successfully dispatched to Slack workspace!")
            else:
                print(f"[✗] Slack API responded with non-ok status: {response.status}")
    except Exception as e:
        print(f"[✗] Network exception encountered dispatching to Slack: {e}")
else:
    print("[✓] System Healthy: Metric points are completely within compliance baselines.")
