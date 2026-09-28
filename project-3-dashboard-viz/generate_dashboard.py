import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# 1. Programmatically calculate paths
CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_SCRIPT_DIR)
csv_path = os.path.join(BASE_DIR, "metrics_history.csv")
output_chart_path = os.path.join(BASE_DIR, "docs", "assets", "sre_dashboard_metrics.png")

# 2. Safely read dataset matrix
try:
    df = pd.read_csv(csv_path)
    # Standardise column cases to simplify mapping conditions
    df.columns = [col.lower().strip() for col in df.columns]
except FileNotFoundError:
    print(f"[✗] Error: Target matrix file not found at: {csv_path}")
    sys.exit(1)

# 3. Compile High-Density SRE Dual-Axis Graph Architecture
try:
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Track plotting series handles for unified legend layout
    plot_handles = []
    plot_labels = []

    # --- PRIMARY AXIS: SYSTEM AVAILABILITY REGION ---
    avail_col = next((c for c in df.columns if 'avail' in c), None)
    if avail_col:
        h1, = ax1.plot(df[avail_col], color='#1f77b4', linewidth=2, label='Availability %')
        plot_handles.append(h1)
        plot_labels.append('System Availability %')
    
    # Establish strict 80% SLO Baseline threshold line
    h_slo = ax1.axhline(y=80, color='#d62728', linestyle='--', linewidth=1.5, label='80% SLO Target')
    plot_handles.append(h_slo)
    plot_labels.append('80% SLO Baseline Target')
    
    ax1.set_xlabel('Timeline Interval (Hours Overview)', fontweight='bold', labelpad=10)
    ax1.set_ylabel('Operational Availability (%)', color='#1f77b4', fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='#1f77b4')
    ax1.set_ylim(50, 105)

    # --- SECONDARY AXIS: TAIL LATENCY MATRIX (p50, p95, p99) ---
    ax2 = ax1.twinx()
    latency_colors = {'p50': '#2ca02c', 'p95': '#ff7f0e', 'p99': '#9467bd'}
    
    for metric_name, color_hex in latency_colors.items():
        lat_col = next((c for c in df.columns if metric_name in c), None)
        if lat_col:
            h_lat, = ax2.plot(df[lat_col], color=color_hex, linewidth=1.2, linestyle=':', label=f'{metric_name.upper()} Latency')
            if f'{metric_name.upper()} Latency' not in plot_labels:
                plot_handles.append(h_lat)
                plot_labels.append(f'{metric_name.upper()} Tail Latency')

    # If no specific columns matched, fall back to compiling whatever fields are available
    if len(plot_handles) <= 1:
        for idx in range(1, min(len(df.columns), 4)):
            h_fallback, = ax1.plot(df.iloc[:, idx], label=f'Stream: {df.columns[idx]}')
            plot_handles.append(h_fallback)
            plot_labels.append(df.columns[idx].upper())

    ax2.set_ylabel('Transaction Latency Processing Profile (ms)', color='#ff7f0e', fontweight='bold', labelpad=10)
    ax2.tick_params(axis='y', labelcolor='#ff7f0e')

    # Unified Layout Polish
    plt.title('E-Commerce Gateway Performance Metrics — 30-Day SRE Historical Analysis', fontsize=14, fontweight='bold', pad=15)
    ax1.grid(True, linestyle='--', alpha=0.4)
    ax1.legend(plot_handles, plot_labels, loc='upper left', framealpha=0.95)
    
    fig.tight_layout()
    os.makedirs(os.path.dirname(output_chart_path), exist_ok=True)
    plt.savefig(output_chart_path, dpi=300, bbox_inches='tight')
    print(f"[✓] Robust dual-axis dashboard compiled cleanly to: {output_chart_path}")

except Exception as e:
    print(f"[✗] Failure compiling telemetry graphic layers: {e}")
    sys.exit(1)
