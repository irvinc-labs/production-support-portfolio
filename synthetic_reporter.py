import urllib.request
import os
import json
import time
import random
from dotenv import load_dotenv

load_dotenv()

# ==============================================================================
# SRE CONFIGURATION MANAGEMENT
# ==============================================================================
# TODO: Replace this string with your live active Slack Webhook URL token
SLACK_WEBHOOK_URL = os.environ.get("SLACK_ALERT_WEBHOOK_URL")
TARGET_ENDPOINT = "https://render.com"  # Aligned to your Milestone 2 routing rule
TOTAL_SYNTHETIC_PROBES = 50

def run_synthetic_suite():
    latencies = []
    success_count = 0
    failure_count = 0
    
    print(f"[SRE] Starting Daily Synthetic Check Matrix against {TARGET_ENDPOINT}...")
    
    for i in range(TOTAL_SYNTHETIC_PROBES):
        # Inject dynamic cache-busting headers and entropy query values to bypass proxy layers
        entropy_key = f"cache_buster_{int(time.time())}_{random.randint(1000, 9999)}"
        url_with_entropy = f"{TARGET_ENDPOINT}?run={entropy_key}"
        
        req = urllib.request.Request(
            url_with_entropy,
            headers={
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'User-Agent': 'SRE-Synthetic-Suite-V1'
            }
        )
        
        start_time = time.time()
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.getcode()
                # Track response timings in milliseconds
                elapsed = (time.time() - start_time) * 1000
                
                # Check for standard success boundaries
                if status == 200:
                    success_count += 1
                    latencies.append(elapsed)
                else:
                    failure_count += 1
        except Exception:
            failure_count += 1
        
        # Brief pacing delay between synthetic requests to prevent traffic spikes
        time.sleep(0.05)
        
    # Calculate SRE Performance Percentiles using pure math calculations
    total_runs = success_count + failure_count
    availability_pct = (success_count / total_runs) * 100 if total_runs > 0 else 0
    error_budget = availability_pct - 99.50 # Target SLO baseline
    
    if latencies:
        latencies.sort()
        n = len(latencies)
        p50 = latencies[int(n * 0.50)]
        p95 = latencies[int(n * 0.95)]
        p99 = latencies[int(n * 0.99)]
    else:
        p50, p95, p99 = 0, 0, 0

    # Build the structured, readable Markdown summary payload
    report_markdown = (
        f"📅 *DAILY SYSTEM PERFORMANCE DIGEST*\n"
        f"======================================\n\n"
        f"📈 *SERVICE AVAILABILITY & BUDGETS*\n"
        f"--------------------------------------\n"
        f"• Target SLO: 99.50%\n"
        f"• Actual Availability: {availability_pct:.2f}%\n"
        f"• Error Budget Status: {'✅ HEALTHY' if error_budget >= 0 else '❌ EXHAUSTED'} ({error_budget:.2f}%)\n\n"
        f"⏱️ *LATENCY PERFORMANCE MATRIX*\n"
        f"--------------------------------------\n"
        f"• Total Synthetic Probes: {total_runs} requests\n"
        f"• Median Latency (p50): {p50:.1f}ms\n"
        f"• Tail Latency (p95): {p95:.1f}ms\n"
        f"• Outlier Latency (p99): {p99:.1f}ms\n\n"
        f"📝 *METRIC LOG COLLECTION STAMP*\n"
        f"• Successes: {success_count} | Dropouts: {failure_count}\n"
    )
    
    # Ship the payload directly to your live Slack room channel
    send_slack_digest(report_markdown)

def send_slack_digest(text_payload):
    try:
        payload_bytes = json.dumps({"text": text_payload}).encode('utf-8')
        req = urllib.request.Request(
            SLACK_WEBHOOK_URL,
            data=payload_bytes,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            if response.getcode() == 200:
                print("[SRE] Daily Summary successfully transmitted to Slack.")
    except Exception as e:
        print(f"[!] Alert Pipeline Dropped Message: {e}")

if __name__ == "__main__":
    run_synthetic_suite()
