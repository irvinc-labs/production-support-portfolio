import urllib.request
import urllib.error
import json
import os
import time
import sys

TARGET_URL = "https://onrender.com"
SLACK_WEBHOOK = os.environ.get("SLACK_ALERT_WEBHOOK_URL")

def send_slack_notification(status_label, raw_payload):
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
                    {"type": "mrkdwn", "text": f"*System:*\nCheckout Simulator Backend"},
                    {"type": "mrkdwn", "text": f"*State captured:*\n`{status_label}`"},
                    {"type": "mrkdwn", "text": f"*Payload Matrix:*\n`{raw_payload}`"}
                ]
            }
        ]
    }
    try:
        req = urllib.request.Request(SLACK_WEBHOOK, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
        print("   ↳ 📬 [SLACK ENGINE] Alert card successfully pushed to channel!")
    except Exception as e:
        print(f"   ↳ ❌ [SLACK] Webhook failed: {e}")

def run_true_monitor():
    print(f"🚀 === [STARTING TRUE TEXT-INSPECTION MONITOR] ===")
    print(f"🎯 Target Vector: {TARGET_URL}\n")
    
    request_count = 1
    
    while True:
        try:
            # Force cache busting query string parameter
            url_with_cache_bust = f"{TARGET_URL}?nocache={time.time_ns()}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 SRE-Text-Inspector-Bot',
                'Connection': 'close'
            }
            
            req = urllib.request.Request(url_with_cache_bust, headers=headers)
            
            with urllib.request.urlopen(req, timeout=5) as response:
                body_text = response.read().decode('utf-8')
                
                # FIX: Check if the text inside the payload body contains our error marker
                if "error" in body_text or "Internal Server Error" in body_text:
                    print(f"[{time.strftime('%H:%M:%S')}] Hit #{request_count}: 🚨 FAILURE CAPTURED INSIDE BODY! -> {body_text}")
                    send_slack_notification("CRITICAL FAULT", body_text)
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] Hit #{request_count}: HTTP 200 OK ✅ (Clean Transaction)")
                    
        except urllib.error.HTTPError as e:
            # Fallback wrapper if the proxy lets the raw 500 error pass through
            error_body = e.read().decode('utf-8')
            print(f"[{time.strftime('%H:%M:%S')}] Hit #{request_count}: 🚨 OUTAGE TRIPPED VIA NETWORK (HTTP {e.code}) -> {error_body}")
            send_slack_notification(f"HTTP {e.code}", error_body)
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Hit #{request_count}: Path Disruption -> {e}")
        
        request_count += 1
        time.sleep(1.0)

if __name__ == "__main__":
    try:
        run_true_monitor()
    except KeyboardInterrupt:
        print("\n🛑 Monitor loop suspended.")
        sys.exit(0)
