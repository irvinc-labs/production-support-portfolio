# 🛡️ Automated SRE Observability & Self-Healing Pipeline
An enterprise-grade production support implementation that pairs dynamic application monitoring with an automated self-healing remediation loop.

## 🏗️ Architectural Topology
* **Target Environment:** Containerised Python HTTP Microservice on Render Web Infrastructure.
* **Telemetry Core:** External Python Engine bypassing edge caching using explicit entropy injects.
* **ChatOps Engine:** Asynchronous Slack Event Stream Handler.
* **Automation Scheduler:** Linux System Daemon (cron).

## 🚀 Key SRE Accomplishments

### 1. Automated Circuit Breaking & Rate Limits
* Engineered a **3-strike sliding failure window** to detect persistent backend error spikes (HTTP 500 triggers).
* Implemented a **90-second validation cooldown freeze** that effectively mitigates "remediation storms" and prevents container thrashing.

### 2. Deep Edge Traffic Visibility
* Designed and deployed a `synthetic_reporter.py` engine running on daily off-peak schedules via Linux cron.
* Calculates precise system-level latencies (**p50, p95, and p99 percentiles**) utilizing pure Python mathematical distribution models over 50 continuous requests.
* Fully bypassed regional edge proxy caches by generating dynamic runtime entropy queries (`?run=cache_buster_X`).

### 3. Edge-Case Resolution & Infrastructure Stability
* Patched systemic host resolution faults (`<urlopen error [Errno -2]>`) by enforcing rigid URL pointer synchronization to the upstream API Gateway.
* Isolated operational boundaries: Resolved system routing degradations (stripping active request queries before routing execution) without modifying a single line of core developer codebase.
