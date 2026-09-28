import urllib.request
import urllib.error
import json
import os
import time
import sys

# TARGET FIXED: Pointing straight to your unique uncollided cloud route!
TARGET_URL = "https://onrender.com"
SLACK_WEBHOOK = os.environ.get("SLACK_ALERT_WEBHOOK_URL")

def send_slack_notification(status_code):
    if not SLACK_WEBHOOK:
        return
    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "🚨 PRODUCTION EXCEPTION DETECTED", "emoji": True}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*System:*\nCheckout Simulator"},
                    {"type": "mrkdwn", "text": f"*Status Code:*\n`HTTP {status_code}`"},
                    {"type": "mrkdwn", "text": f"*Impact Vector:*\n`{TARGET_URL}`"}
                ]
            }
        ]
    }
    try:
        req = urllib.request.Request(SLACK_WEBHOOK, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
        print("   ↳ 📬 [SLACK ALERT] Incident card dropped into channel!")
    except Exception as e:
        print(f"   ↳ ❌ [SLACK] Webhook failed: {e}")

def run_force_reset_test():
    print(f"🚀 === [STARTING ZERO-CACHE NETWORK STRESS TEST] ===")
    print(f"🎯 Target Vector: {TARGET_URL}")
    print("⚡ Profile: Killing network connections after every single hit...")
    print("Press Ctrl+C to stop testing.\n")
    
    request_count = 1
    success_count = 0
    failure_count = 0
    
    while True:
        try:
            url_with_cache_bust = f"{TARGET_URL}?nocache={time.time_ns()}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 SRE-Socket-Force-Tester',
                'Connection': 'close',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache'
            }
            
            req = urllib.request.Request(url_with_cache_bust, headers=headers)
            
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    success_count += 1
                    print(f"[{time.strftime('%H:%M:%S')}] Hit #{request_count}: HTTP 200 OK ✅")
        except urllib.error.HTTPError as e:
            failure_count += 1
            print(f"[{time.strftime('%H:%M:%S')}] Hit #{request_count}: 🚨 OUTAGE CAUGHT! (HTTP {e.code})")
            send_slack_notification(e.code)
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Hit #{request_count}: Network Disruption -> {e}")
        
        request_count += 1
        time.sleep(0.7)

if __name__ == "__main__":
    try:
        run_force_reset_test()
    except KeyboardInterrupt:
        print("\n🛑 Diagnostic tracking suspended by engineer.")
