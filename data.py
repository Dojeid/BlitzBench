import csv
import statistics
import subprocess
import os

# --- CORE UTILITIES ---

def get_ps_measure(command):
    """Runs a command via PowerShell and returns (ticks, ms)."""
    # Forcing PS to output 'ticks,ms' directly
    ps_cmd = f"$m = Measure-Command {{ {command} }}; Write-Host ($m.Ticks.ToString() + ',' + $m.TotalMilliseconds.ToString())"
    
    result = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
    output = result.stdout.strip()
    
    if not output or ',' not in output:
        return 0, 0.0
    try:
        ticks_str, ms_str = output.split(',')
        return int(ticks_str), float(ms_str)
    except:
        return 0, 0.0

def run_report(filename, label):
    """Analyzes a specific CSV file and prints a comprehensive report including Ticks."""
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        print(f"[-] No data found for {label}.")
        return

    c_ticks, c_times = [], []
    p_ticks, p_times = [], []
    
    with open(filename, 'r') as f:
        reader = list(csv.reader(f))
        for row in reader[1:]: # Skip header
            if len(row) >= 5:
                c_ticks.append(float(row[1]))
                c_times.append(float(row[2]))
                p_ticks.append(float(row[3]))
                p_times.append(float(row[4]))

    if not c_times: return

    # Using Median for all metrics
    c_med_t, c_med_ms = statistics.median(c_ticks), statistics.median(c_times)
    p_med_t, p_med_ms = statistics.median(p_ticks), statistics.median(p_times)
    
    # Calculate % difference based on time
    diff = ((p_med_ms - c_med_ms) / p_med_ms) * 100

    print(f"\n--- {label.upper()} REPORT ({len(c_times)} Samples) ---")
    print(f"{'Metric':<18} | {'Your Lang':<15} | {'Python':<15}")
    print("-" * 55)
    print(f"{'Median Ticks':<18} | {c_med_t:<15.0f} | {p_med_t:<15.0f}")
    print(f"{'Median Time (ms)':<18} | {c_med_ms:<15.4f} | {p_med_ms:<15.4f}")
    print("-" * 55)
    
    res = "faster 🔥" if diff > 0 else "slower 🛠️"
    print(f"RESULT: Your language is {abs(diff):.2f}% {res}")

# --- TEST ORCHESTRATOR ---

def execute_test(test_id, runs):
    configs = {
        "1": {"name": "Loop (Startup)", "csv": "data_loop.csv", "c": "./class.exe", "p": "python class_test.py"},
        "2": {"name": "Stress (Math)", "csv": "data_stress.csv", "c": "./stress.exe", "p": "python stress_test.py"}
    }
    
    cfg = configs.get(test_id)
    if not cfg: return

    print(f"\n🚀 Warming up {cfg['name']}...")
    get_ps_measure(cfg['c'])
    get_ps_measure(cfg['p'])

    print(f"📊 Collecting {runs} samples for {cfg['name']}...")
    
    file_exists = os.path.exists(cfg['csv'])
    with open(cfg['csv'], 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists or os.stat(cfg['csv']).st_size == 0:
            writer.writerow(['sno', 'c_ticks', 'c_time', 'p_ticks', 'p_time'])
        
        for i in range(1, runs + 1):
            print(f"   Progress: [{i}/{runs}]", end="\r")
            ct, cm = get_ps_measure(cfg['c'])
            pt, pm = get_ps_measure(p_cmd := cfg['p']) # Using internal var
            writer.writerow([i, ct, cm, pt, pm])
    
    print(f"\n✅ Data saved to {cfg['csv']}")
    run_report(cfg['csv'], cfg['name'])

# --- MAIN MENU ---

def main():
    while True:
        print("\n⚡ BlitzBench Master Dashboard ⚡")
        print("1. [LITE] Run Loop/Class Test (Startup performance)")
        print("2. [HEAVY] Run Stress Test (Calculation performance)")
        print("3. [VIEW] See All Saved Reports")
        print("4. [CLEAN] Wipe All CSV Data")
        print("Q. Exit")
        
        choice = input("\nChoice: ").strip().lower()
        
        if choice in ['1', '2']:
            try:
                num = int(input("Enter number of runs: "))
                execute_test(choice, num)
            except ValueError:
                print("Invalid number.")
        
        elif choice == '3':
            run_report("data_loop.csv", "Loop (Startup)")
            run_report("data_stress.csv", "Stress (Math)")
            
        elif choice == '4':
            confirm = input("Are you sure? This wipes all CSVs! (y/n): ")
            if confirm.lower() == 'y':
                for f in ["data_loop.csv", "data_stress.csv"]:
                    if os.path.exists(f): os.remove(f)
                print("🧹 Data wiped.")
                
        elif choice == 'q':
            print("Closing BlitzBench. Happy coding!")
            break

if __name__ == "__main__":
    main()