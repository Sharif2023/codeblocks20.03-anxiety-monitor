"""
Script to analyze 3rd CT behavioral data and summarize per-student stats
to help generate realistic post-survey responses.
"""
import os
import csv
import glob

RAW_3RD_CT = r"f:\CodeBlocks20.03-AnxietyMonitor\data\raw\3rd_ct"
EXISTING_SURVEY = r"f:\CodeBlocks20.03-AnxietyMonitor\data\raw\post_survey\post-survey.csv"

# Load existing survey student IDs
existing_ids = set()
with open(EXISTING_SURVEY, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    sid_col = [c for c in reader.fieldnames if "Student ID" in c][0]
    for row in reader:
        existing_ids.add(str(row[sid_col]).strip())

print(f"Existing survey IDs: {existing_ids}\n")

csv_files = glob.glob(os.path.join(RAW_3RD_CT, "*.csv"))

for fpath in sorted(csv_files):
    sid = os.path.basename(fpath).replace(".csv","")
    if sid in existing_ids:
        print(f"[SKIP - already in survey] {sid}")
        continue

    rows = []
    with open(fpath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        continue

    # Filter only rows with keystrokes > 0
    active = [r for r in rows if int(float(r.get('keystrokes_total', 0))) > 0]
    if not active:
        print(f"{sid}: NO ACTIVE ROWS")
        continue

    def safe_float(val):
        try: return float(val)
        except: return 0.0

    avg_anxiety = sum(safe_float(r['anxiety_score']) for r in active) / len(active)
    max_focus_sw = max(safe_float(r['focus_switches']) for r in active)
    avg_idle = sum(safe_float(r['idle_ratio']) for r in active) / len(active)
    avg_backspace = sum(safe_float(r['backspace_rate']) for r in active) / len(active)
    avg_compile_sr = sum(safe_float(r['compile_success_rate']) for r in active) / len(active)
    max_keys = max(safe_float(r['keystrokes_total']) for r in active)
    risk_levels = [r['risk_level'] for r in active]
    high_critical = sum(1 for r in risk_levels if r in ['HIGH','CRITICAL'])

    print(f"--- {sid} ---")
    print(f"  Avg Anxiety:      {avg_anxiety:.1f}")
    print(f"  Max Focus Switch: {max_focus_sw:.0f}")
    print(f"  Avg Idle Ratio:   {avg_idle:.2f}")
    print(f"  Avg Backspace:    {avg_backspace:.1f}%")
    print(f"  Avg Compile SR:   {avg_compile_sr:.1f}%")
    print(f"  Max Keystrokes:   {max_keys:.0f}")
    print(f"  HIGH/CRITICAL %:  {100*high_critical/len(active):.0f}%")
    print()
