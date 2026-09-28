import urllib.request
import urllib.error
import json
import os
import time
import sys

# Target environment endpoints based on your deployed checkout simulator
TARGET_URL = "https://onrender.com"
TEAMS_WEBHOOK = os.environ.get("ALERT_WEBHOOK_URL")

def send_teams_notification(status_code, error_message):
    """Dispatches a structured incident card to the support team channel."""
    if not TEAMS_WEBHOOK:
        print("[WARNING] Alert triggered but ALERT_WEBHOOK_URL environment variable is missing.")
        print(f"[LOCAL LOG] ALERT: {error_message} (HTTP {status_code})")
        return

    # Structured Adaptive Card payload matching enterprise notification frameworks
    payload = {
        "type": "message",
        "attachments": [{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "$schema": "http://adaptivecards.io",
                "version": "1.2",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "🚨 PRODUCTION INCIDENT ALERT",
                        "weight": "Bolder",
                        "size": "Medium",
                        "color": "Attention"
                    },
                    {
                        "type": "FactSet",
                        "facts": [
                            {"title": "System:", "value": "Checkout & Payment Gateway Simulator"},
                            {"title": "Target Vector:", "value": TARGET_URL},
                            {"title": "Status Code:", "value": f"HTTP {status_code}"},
                            {"title": "Impact:", "value": "Intermittent Checkout Disruptions Detected"}
                        ]
                    },
                    {
                        "type": "TextBlock",
                        "text": f"Raw Exception Data: {error_message}",
                        "wrap": True,
                        "fontType": "Monospace",
                        "size": "Small"
                    }
                ]
            }
        }]
    }

    try:
        req = urllib.request.Request(
            TEAMS_WEBHOOK,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("[SRE ALERT ENGINE] Incident card successfully dispatched to operations channel.")
    except Exception as e:
        print(f"[ERROR] Failed to send webhook payload: {e}")

def run_proactive_check():
    print(f"=== [AU/NZ SRE Monitor] Monitoring: {TARGET_URL} ===")
    print("Press Ctrl+C to terminate tracking loop.\n")
    
    while True:
        try:
            # Ping your live Render simulator cloud instance
            with urllib.request.urlopen(TARGET_URL, timeout=5) as response:
                if response.status == 200:
                    print(f"[{time.strftime('%H:%M:%S')}] HTTP 200 OK - Checkout channel stable.")
        except urllib.error.HTTPError as e:
            # Catches the deliberate 20% server failures (HTTP 500)
            print(f"[{time.strftime('%H:%M:%S')}] 🚨 ALERT: Transaction Failure detected (HTTP {e.code})")
            send_teams_notification(e.code, "Internal Server Error - Third Party Gateway Timeout simulation.")
        except urllib.error.URLError as e:
            # Catches systemic downtime (e.g. if Render is sleeping or network drops)
            print(f"[{time.strftime('%H:%M:%S')}] 🚨 ALERT: Target Host Unreachable")
            send_teams_notification("503", str(e.reason))
            
        # Run check every 10 seconds to catch transient errors quickly
        time.sleep(10)

if __name__ == "__main__":
    try:
        run_proactive_check()
    except KeyboardInterrupt:
        print("\nMonitoring suspended. Exiting gracefully...")
        sys.exit(0)
