# Production Support SRE Portfolio

Production-grade sentinel monitoring and automated remediation system.

## Quick Start

```bash
git clone https://github.com/irvinc-labs/production-support-portfolio.git
cd production-support-portfolio
pip install python-dotenv --break-system-packages
cat > .env << EOF
RENDER_API_KEY=your_key
RENDER_SERVICE_ID=your_id
SLACK_ALERT_WEBHOOK_URL=your_webhook
EOF
python3 project-2-api-monitor/cache_killer_monitor.py
```

## Features

- Cache Killer Monitor: Real-time endpoint surveillance
- Automated Remediation: Render API restart on 3 consecutive failures
- Slack Integration: Real-time alerting
- Synthetic Testing: Daily uptime probes (p50, p95, p99)
- Cron Automation: Scheduled daily reports at 2 AM

## SRE Concepts

- Circuit Breaker pattern with cooldown
- Observability via metrics and logs
- Graceful degradation
- API-driven automation
- Incident detection and response

## Security

- Secrets in .env (never committed)
- Bearer token auth
- HTTPS only
- .gitignore protection

Status: ✅ Production Ready
