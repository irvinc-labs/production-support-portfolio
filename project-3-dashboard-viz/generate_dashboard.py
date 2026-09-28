import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# 1. Programmatically calculate the absolute path to the monorepo root folder
CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_SCRIPT_DIR)

csv_path = os.path.join(BASE_DIR, "metrics_history.csv")
output_chart_path = os.path.join(BASE_DIR, "docs", "assets", "sre_dashboard_metrics.png")

print(f"[*] Base Directory resolved to: {BASE_DIR}")
print(f"[*] Looking for metrics matrix at: {csv_path}")

# 2. Safely read the metrics CSV data matrix
try:
    df = pd.read_csv(csv_path)
    print(f"[✓] Successfully loaded telemetry matrix data! Total records: {len(df)}")
except FileNotFoundError:
    print(f"[✗] Error: Target file not found at calculated absolute path: {csv_path}")
    sys.exit(1)

# 3. Simple high-density compilation layer (Customized for your SRE portfolio metrics)
try:
    plt.figure(figsize=(10, 5))
    
    # Check if expected availability metrics exist in your CSV layout
    if 'availability' in df.columns:
        plt.plot(df['availability'], label='System Availability %', color='blue')
        plt.axhline(y=80, color='red', linestyle='--', label='80% SLO Baseline')
    else:
        # Fallback to plotting the first column if exact names differ
        plt.plot(df.iloc[:, 1], label='Telemetry Data Stream', color='purple')
        
    plt.title('Production System Performance - 30-Day Historical Trend')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    
    # Ensure the target asset directory exists
    os.makedirs(os.path.dirname(output_chart_path), exist_ok=True)
    
    # Save high-density dashboard graphic cleanly
    plt.savefig(output_chart_path, dpi=300, bbox_inches='tight')
    print(f"[✓] Dashboard graphic successfully compiled to: {output_chart_path}")
except Exception as e:
    print(f"[✗] Render Error: Failed to compile visual dashboard layout: {e}")
    sys.exit(1)
