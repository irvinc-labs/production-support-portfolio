import urllib.request
import urllib.error
import json
import os
import time
import sys

TARGET_URL = "https://onrender.com"
SLACK_WEBHOOK = os.environ.get("SLACK_ALERT_WEBHOOK_URL")

def send_slack_notification(status_code, error_message):
    if not SLACK_WEBHOOK:
        print("[WARNING] Alert triggered but SLACK_ALERT_WEBHOOK_URL environment variable is missing.")
        print(f"[LOCAL LOG] ALERT: {error_message} (HTTP {status_code})")
        return

    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 PRODUCTION INCIDENT ALERT",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*System:*\nCheckout Simulator"},
                    {"type": "mrkdwn", "text": f"*Target Vector:*\n`{TARGET_URL}`"},
                    {"type": "mrkdwn", "text": f"*Status Code:*\n`HTTP {status_code}`"},
                    {"type": "mrkdwn", "text": f"*Impact:*\nIntermittent Disruptions"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Raw Exception Data:*\n```{error_message}```"
                }
            }
        ]
    }

    try:
        req = urllib.request.Request(
            SLACK_WEBHOOK,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("[SRE ALERT ENGINE] Incident card successfully dispatched to Slack channel.")
    except Exception as e:
        print(f"[ERROR] Failed to send Slack webhook payload: {e}")

def run_proactive_check():
    print(f"=== [AU/NZ SRE Slack Monitor] Monitoring: {TARGET_URL} ===")
    print("Press Ctrl+C to terminate tracking loop.\n")
    
    while True:
        try:
            with urllib.request.urlopen(TARGET_URL, timeout=5) as response:
                if response.status == 200:
                    print(f"[{time.strftime('%H:%M:%S')}] HTTP 200 OK - Checkout stable.")
        except urllib.error.HTTPError as e:
            print(f"[{time.strftime('%H:%M:%S')}] 🚨 ALERT: Transaction Failure (HTTP {e.code})")
            send_slack_notification(e.code, "Internal Server Error - Third Party Gateway Timeout simulation.")
        except urllib.error.URLError as e:
            print(f"[{time.strftime('%H:%M:%S')}] 🚨 ALERT: Target Host Unreachable")
            send_slack_notification("503", str(e.reason))
            
        time.sleep(10)

if __name__ == "__main__":
    try:
        run_proactive_check()
    except KeyboardInterrupt:
        print("\nMonitoring suspended. Exiting gracefully...")
        sys.exit(0)
