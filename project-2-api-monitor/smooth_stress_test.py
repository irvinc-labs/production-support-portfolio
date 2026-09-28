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
        return
    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "🚨 SRE ALERT: PRODUCTION OUTAGE", "emoji": True}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*System:*\nCheckout Simulator"},
                    {"type": "mrkdwn", "text": f"*Impact Vector:*\n`{TARGET_URL}`"},
                    {"type": "mrkdwn", "text": f"*Status Code:*\n`HTTP {status_code}`"},
                    {"type": "mrkdwn", "text": f"*Monitoring Engine:*\nSmooth Traffic Simulator"}
                ]
            }
        ]
    }
    try:
        req = urllib.request.Request(SLACK_WEBHOOK, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
        print("   ↳ 📬 [SLACK] Real-time incident alert card dispatched!")
    except Exception as e:
        print(f"   ↳ ❌ [SLACK] Webhook failed: {e}")

def run_smooth_stress():
    print(f"🚀 === [STARTING SMOOTH OPERATIONS LOAD TEST] ===")
    print(f"🎯 Target: {TARGET_URL}")
    print("📈 Profile: Polling with a secure 0.5s firewall-bypass delay...")
    print("Press Ctrl+C to terminate operational tracking loop.\n")
    
    request_count = 1
    success_count = 0
    failure_count = 0
    
    while True:
        try:
            # Force cache-busting unique string per request
            url_with_cache_bust = f"{TARGET_URL}?request_id={time.time_ns()}"
            
            # Mimic a clean browser user-agent to stay compliant with platform routing filters
            req = urllib.request.Request(
                url_with_cache_bust, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) SRE-Lab-Monitor'}
            )
            
            with urllib.request.urlopen(req, timeout=4) as response:
                if response.status == 200:
                    success_count += 1
                    print(f"[{time.strftime('%H:%M:%S')}] Request #{request_count}: HTTP 200 OK ✅ (Total Successes: {success_count})")
        except urllib.error.HTTPError as e:
            failure_count += 1
            print(f"[{time.strftime('%H:%M:%S')}] Request #{request_count}: 🚨 ALERT! Caught HTTP {e.code} Outage (Total Failures: {failure_count})")
            send_slack_notification(e.code, "Internal Server Error Simulation")
        except Exception as e:
            failure_count += 1
            print(f"[{time.strftime('%H:%M:%S')}] Request #{request_count}: Network/Timeout Exception -> {e}")
        
        request_count += 1
        # The magic key: a steady half-second pulse that complies with the cloud gateway limits
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        run_smooth_stress();
    except KeyboardInterrupt:
        print("\n🛑 Stress testing suspended by on-call engineer.")
