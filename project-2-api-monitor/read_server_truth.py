import urllib.request
import urllib.error
import time

TARGET_URL = "https://onrender.com"

print(f"🕵️‍♂️ === [SRE DIRECT CONTENT INSPECTION] ===")
print(f"🎯 Target: {TARGET_URL}\n")

for i in range(15):
    try:
        url_with_cache_bust = f"{TARGET_URL}?check={time.time_ns()}"
        req = urllib.request.Request(
            url_with_cache_bust, 
            headers={
                'User-Agent': 'SRE-Truth-Finder',
                'Connection': 'close'
            }
        )
        with urllib.request.urlopen(req, timeout=4) as response:
            body = response.read().decode('utf-8')
            print(f"[{i+1}] HTTP {response.status} -> Raw Body payload: {body}")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(f"[{i+1}] 🚨 CAUGHT ERROR HTTP {e.code} -> Raw Body payload: {body}")
    except Exception as e:
        print(f"[{i+1}] Exception: {e}")
    time.sleep(0.5)
