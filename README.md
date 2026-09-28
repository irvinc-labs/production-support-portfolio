# 🛡️ Enterprise Automated SRE Observability & Self-Healing Pipeline
A production-grade support automation pipeline featuring real-time endpoint surveillance, an automated self-healing remediation loop, and off-peak synthetic metrics collection.

---

### 🌐 Live Infrastructure Matrix
* **Live Web Application:** [Deployed on Render Web Service](https://render.com) 
* **Operational Telemetry Core:** Deployed in Linux WSL App Engine Environment
* **ChatOps Incident Hub:** Integrated Private Slack Event Stream

---

### 🏗️ Directory Architecture Links
To dive directly into the engineering components, navigate the source code here:
* [📁 Core Web Service (`project-1-log-analyzer`)](./project-1-log-analyzer) — Python HTTP application container running under a strict `USER appuser` security standard.
* [📁 Sentinel Telemetry Engine (`project-2-api-monitor`)](./project-2-api-monitor) — Real-time loop driving incident capturing and automated container remediation.
* [📄 Synthetic Uptime Suite (`synthetic_reporter.py`)](./synthetic_reporter.py) — Daily automated off-peak probe matrix calculating p50/p95/p99 tail latencies.

---

### 🚀 High-Impact SRE Accomplishments

#### 1. Automated Circuit Breaking & Rate Limiting
* Engineered a strict **3-strike sliding failure window** to detect persistent backend degradations (HTTP 500 triggers).
* Implemented a stateful **90-second validation cooldown freeze** that effectively mitigates "remediation storms" and prevents infinite container thrashing loops.

#### 2. Advanced Cache-Busting Visibility
* Fully bypassed regional edge proxy layers and CDN caching by building dynamic, per-request **runtime entropy query values** (`?run=cache_buster_X`).
* Enforced explicit cache-control headers (`no-cache, no-store, must-revalidate`) to guarantee un-cached telemetry testing results.

#### 3. Zero-Intervention Linux Cron Automation
* Integrated the daily reporting suite into the **Linux System Daemon (cron)** to execute daily at 2:00 AM off-peak.
* Calculates precise system latencies using mathematical distribution arrays to extract the **Median (p50)**, **Tail (p95)**, and **Outlier (p99)** request performance bounds.

#### 4. Isolated Boundary Debugging
* Patched systemic host resolution exceptions (`<urlopen error [Errno -2]>`) by synchronising tracking rules directly to Render's upstream API gateway.
* Maintained clean separation of operational concerns: Resolved critical pathing limitations (stripping query string mutations before matching application paths) without changing a single line of the developer's core business code.

---

### 📊 Daily ChatOps Operational Summary Schema
The automated reporting pipeline ships an executive digest directly to Slack every 24 hours:

```text
📅 DAILY SYSTEM PERFORMANCE DIGEST
======================================
📈 SERVICE AVAILABILITY & BUDGETS
• Target SLO: 99.50%
• Actual Availability: 100.00%
• Error Budget Status: ✅ HEALTHY (0.50%)

⏱️ LATENCY PERFORMANCE MATRIX
• Total Synthetic Probes: 50 requests
• Median Latency (p50): 265.8ms
• Tail Latency (p95): 439.5ms
• Outlier Latency (p99): 750.9ms
```

---

### 🛡️ Security & Token Hardening
* **Local Sandboxing:** All critical operational infrastructure tokens (`SLACK_ALERT_WEBHOOK_URL`, `RENDER_API_KEY`) are stored natively in the host's Linux environment block.
* **Leak Protection:** Armed with a rigid `.gitignore` layer ensuring raw operational execution logs (`*.log`) and variable baselines are structurally blocked from pushing to public repositories.
