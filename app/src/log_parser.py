import sys

def scan_production_logs():
    log_file = "app_production.log"
    critical_errors = []
    
    print("=== [AU/NZ Support Automation] Starting Log Scan... ===")
    
    try:
        # Open and read our digital notebook line by line
        with open(log_file, "r") as file:
            for line in file:
                # If the line contains our target incident keyword, save it
                if "CRITICAL" in line:
                    critical_errors.append(line.strip())
                    
    except FileNotFoundError:
        print(f"Error: Could not find {log_file}. Make sure the app has run first!")
        return

    # Output a clean Incident Summary Report for the support team
    print("\n--- SRE INCIDENT TRIAGE REPORT ---")
    print(f"Total Critical Outages Found: {len(critical_errors)}")
    
    if len(critical_errors) > 3:
        print("Recommended Priority: P1 - HIGH SEVERITY INCIDENT (SLA Breach Risk)")
    else:
        print("Recommended Priority: P3 - Minor Intermittent Alert")
    print("----------------------------------\n")
    
    print("--- TIMELINE OF CRITICAL EVENTS ---")
    for error in critical_errors:
        print(f"[ALERT] {error}")
    print("-----------------------------------")

if __name__ == "__main__":
    scan_production_logs()
