import pandas as pd
import matplotlib.pyplot as plt
import os

# Pointing up one level (..) to read the metrics file at the monorepo root
csv_path = '../metrics_history.csv'
if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found. Please run your generate_history.py first.")
    exit(1)

try:
    df = pd.read_csv(csv_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
except Exception as e:
    print(f"Error parsing CSV file: {e}")
    exit(1)

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

ax1.plot(df['timestamp'], df['availability_pct'], marker='o', color='#2ca02c', linewidth=2, label='System Availability')
ax1.axhline(y=80.0, color='#d62728', linestyle='--', linewidth=1.5, label='Chaos Target Baseline (80%)')
ax1.set_title('30-Day System Availability Profile', fontsize=13, fontweight='bold', pad=10)
ax1.set_ylabel('Availability (%)', fontsize=11)
ax1.set_ylim(60, 105)
ax1.legend(loc='lower left', frameon=True)

ax2.plot(df['timestamp'], df['p99_latency_ms'], marker='^', color='#9467bd', linestyle=':', linewidth=1.5, label='p99 Tail Latency')
ax2.plot(df['timestamp'], df['p95_latency_ms'], marker='s', color='#ff7f0e', linestyle='--', linewidth=1.5, label='p95 Latency')
ax2.plot(df['timestamp'], df['p50_latency_ms'], marker='x', color='#1f77b4', linestyle='-', linewidth=1.5, label='p50 Median Latency')
ax2.set_title('System Latency Profile Matrix (ms)', fontsize=13, fontweight='bold', pad=10)
ax2.set_xlabel('Timeline Data Point Grouping', fontsize=11)
ax2.set_ylabel('Latency (ms)', fontsize=11)
ax2.legend(loc='upper left', frameon=True)

plt.tight_layout()
# Save the chart directly into the centralized docs assets folder
output_img = '../docs/assets/sre_dashboard_metrics.png'
plt.savefig(output_img, dpi=150)
print(f"Success! Dashboard visualization asset saved directly to: '{output_img}'")
