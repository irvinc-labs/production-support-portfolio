import urllib.request
import urllib.error
import json
import os
import time
import sys

# TARGET FIXED: Pointing straight to your live verified Render cloud engine
TARGET_URL = "https://onrender.com"
SLACK_WEBHOOK = os.environ.get("SLACK_ALERT_WEBHOOK_URL")

def send_slack_notification(status_code, error_message):
    if not SLACK_WEBHOOK:
        return
    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "🚨 REGRESSION TEST: OUTAGE DETECTED", "emoji": True}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Test Vector:*\n`{TARGET_URL}`"},
                    {"type": "mrkdwn", "text": f"*Status Code:*\n`HTTP {status_code}`"}
                ]
            }
        ]
    }
    try:
        req = urllib.request.Request(SLACK_WEBHOOK, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
    except Exception:
        pass

def run_regression_load():
    print(f"🚀 === [STARTING REGRESSION TEST] ===")
    print(f"🎯 Target: {TARGET_URL}")
    print("📈 Volume Profile: Firing 10 rapid bursts every 5 seconds...")
    print("Press Ctrl+C to terminate test.\n")
    
    batch_count = 1
    while True:
        print(f"👉 Sending Batch #{batch_count} (10 Requests)...")
        successes = 0
        failures = 0
        
        for i in range(10):
            try:
                # Cache-busting trick: append a timestamp so Render is forced to calculate the 20% rule every time
                url_with_cache_bust = f"{TARGET_URL}?t={time.time_ns()}"
                req = urllib.request.Request(url_with_cache_bust, headers={'User-Agent': 'SRE-Load-Tester'})
                
                with urllib.request.urlopen(req, timeout=3) as response:
                    if response.status == 200:
                        successes += 1
            except urllib.error.HTTPError as e:
                failures += 1
                send_slack_notification(e.code, "Regression test triggered failure.")
            except Exception:
                failures += 1
            
            time.sleep(0.05)
            
        print(f"📊 Batch #{batch_count} Complete: {successes} Passed | {failures} Failed & Alerted.")
        batch_count += 1
        
        print("⏳ Waiting 5 seconds before next burst...\n")
        time.sleep(5)

if __name__ == "__main__":
    try:
        run_regression_load()
    except KeyboardInterrupt:
        print("\n🛑 Regression test terminated by engineer.")
