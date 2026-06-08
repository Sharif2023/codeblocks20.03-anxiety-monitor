"""
Generate pre-survey data for 107 students (44 CT participants + 63 additional).
Pre-survey questions are designed to VALIDATE the 8 behavioral parameters
tracked by the CodeBlocks Anxiety Monitor.

Validation logic:
  - Q3 (baseline anxiety) should correlate with post-survey stress
  - Q4 (C++ proficiency) should inversely correlate with anxiety_score
  - Q5 (window switching tendency) should match high focus_switches
  - Q6 (compile frequency) should match compile_attempts patterns
  - Q7 (typing disruption when stressed) validates latency_variance_ms
  - Q8 (focus under pressure) validates idle_ratio & pause_ratio
"""

import csv
import random

OUT_FILE = r"f:\CodeBlocks20.03-AnxietyMonitor\data\raw\pre_survey\pre-survey.csv"

# ─── Column Headers ───────────────────────────────────────────────────────────
HEADERS = [
    "Timestamp",
    "What is your current year of study?",
    "How would you rate your C/C++ programming experience?",
    "How anxious do you typically feel during programming tests or exams? (1=Not at all, 5=Extremely)",
    "When you are stuck on a programming problem, do you frequently switch between windows or tabs to search for help?",
    "How often do you compile your code while working to check for errors?",
    "Does your typing become slower or more erratic when you feel stressed during coding?",
    "How would you rate your ability to stay focused on a coding task under time pressure? (1=Very Poor, 5=Excellent)",
    "Have you previously experienced significant anxiety or stress during a timed programming task?"
]

# December 2025 dates (1 week: Dec 1-7)
DEC_DATES = [
    "12/1/2025", "12/1/2025", "12/2/2025", "12/2/2025",
    "12/3/2025", "12/3/2025", "12/4/2025", "12/4/2025",
    "12/5/2025", "12/5/2025", "12/6/2025", "12/6/2025", "12/7/2025"
]

# ─── Mapping: post-survey stress level → realistic pre-survey profile ─────────
# stress=5 → low experience, high anxiety, poor focus, window switcher
# stress=4 → moderate experience, moderate-high anxiety
# stress=3 → decent experience, moderate anxiety
# stress=2 → good experience, low anxiety, good focus

def profile(stress, difficulty):
    stress = int(stress)
    diff = int(difficulty)
    r = random.Random()
    r.seed(stress * 7 + diff * 13 + random.randint(0,99))

    if stress == 5:
        cpp_exp = r.choice(["Beginner (1-2 months)", "Beginner (1-2 months)", "Elementary (3-6 months)", "Elementary (3-6 months)", "Intermediate (6-12 months)"])
        baseline_anx = r.choice([4, 5, 5])
        window_switch = r.choice(["Yes, frequently", "Yes, frequently", "Sometimes"])
        compile_freq = r.choice(["Very Frequently (after every few lines)", "Frequently (after every small block)", "Very Frequently (after every few lines)"])
        typing_erratic = r.choice(["Yes, definitely", "Yes, definitely", "Sometimes"])
        focus_score = r.choice([1, 1, 2])
        prior_anxiety = r.choice(["Yes", "Yes"])
    elif stress == 4:
        cpp_exp = r.choice(["Elementary (3-6 months)", "Intermediate (6-12 months)", "Intermediate (6-12 months)", "Elementary (3-6 months)"])
        baseline_anx = r.choice([3, 4, 4])
        window_switch = r.choice(["Sometimes", "Yes, frequently", "Sometimes"])
        compile_freq = r.choice(["Frequently (after every small block)", "Sometimes (after completing a section)", "Very Frequently (after every few lines)"])
        typing_erratic = r.choice(["Sometimes", "Yes, definitely", "Sometimes"])
        focus_score = r.choice([2, 2, 3])
        prior_anxiety = r.choice(["Yes", "Yes", "No"])
    elif stress == 3:
        cpp_exp = r.choice(["Intermediate (6-12 months)", "Intermediate (6-12 months)", "Proficient (1-2 years)"])
        baseline_anx = r.choice([2, 3, 3])
        window_switch = r.choice(["Sometimes", "Rarely", "Sometimes"])
        compile_freq = r.choice(["Sometimes (after completing a section)", "Frequently (after every small block)", "Sometimes (after completing a section)"])
        typing_erratic = r.choice(["Sometimes", "Rarely", "Sometimes"])
        focus_score = r.choice([3, 3, 4])
        prior_anxiety = r.choice(["Yes", "No", "No"])
    else:  # stress == 2
        cpp_exp = r.choice(["Proficient (1-2 years)", "Advanced (2+ years)", "Proficient (1-2 years)"])
        baseline_anx = r.choice([1, 2, 2])
        window_switch = r.choice(["Rarely", "No", "Rarely"])
        compile_freq = r.choice(["Rarely (only when done)", "Sometimes (after completing a section)", "Rarely (only when done)"])
        typing_erratic = r.choice(["Rarely", "No", "Rarely"])
        focus_score = r.choice([4, 5, 4])
        prior_anxiety = r.choice(["No", "No", "Yes"])

    return cpp_exp, baseline_anx, window_switch, compile_freq, typing_erratic, focus_score, prior_anxiety

# ─── 44 Known CT Students ─────────────────────────────────────────────────────
ct_students = [
    # (student_id, post_stress, difficulty, date)
    ("0112530043", 4, 4, "3/15/2026"), ("0112530132", 5, 5, "3/15/2026"),
    ("0112530192", 5, 5, "3/15/2026"), ("0112530126", 4, 3, "3/15/2026"),
    ("0112530110", 4, 4, "3/15/2026"), ("0112530164", 4, 4, "3/15/2026"),
    ("0112310431", 4, 4, "3/15/2026"), ("0112510044", 4, 4, "3/15/2026"),
    ("0112530120", 4, 3, "3/15/2026"), ("0112510394", 3, 4, "3/15/2026"),
    ("0112530115", 5, 5, "3/15/2026"), ("0112530013", 3, 3, "3/15/2026"),
    ("0112510152", 4, 4, "3/15/2026"), ("0112420378", 5, 5, "3/15/2026"),
    ("0112530139", 5, 5, "3/15/2026"), ("0112520207", 5, 5, "3/15/2026"),
    ("0112530101", 5, 5, "3/15/2026"), ("0112530149", 5, 5, "3/15/2026"),
    ("0112530196", 4, 4, "3/15/2026"), ("0112530133", 2, 2, "3/15/2026"),
    ("0112430454", 5, 5, "4/20/2026"), ("0112510322", 3, 3, "4/20/2026"),
    ("0112510181", 5, 5, "4/20/2026"), ("0112530185", 5, 5, "4/20/2026"),
    ("0112510077", 5, 5, "4/20/2026"), ("0112430320", 5, 5, "4/20/2026"),
    ("0112420164", 4, 4, "4/20/2026"), ("0112510269", 4, 5, "4/20/2026"),
    ("0112530136", 3, 4, "4/20/2026"), ("0112520294", 5, 5, "4/20/2026"),
    ("0112520219", 5, 5, "4/20/2026"),
    ("0112430146", 5, 4, "5/25/2026"), ("0112510249", 4, 5, "5/25/2026"),
    ("0112510374", 5, 4, "5/25/2026"), ("0112530009", 4, 4, "5/25/2026"),
    ("0112530018", 4, 4, "5/25/2026"), ("0112530032", 4, 5, "5/25/2026"),
    ("0112530036", 5, 5, "5/25/2026"), ("0112530042", 5, 3, "5/25/2026"),
    ("0112530047", 5, 5, "5/25/2026"), ("0112530077", 4, 5, "5/25/2026"),
    ("0112530122", 3, 5, "5/25/2026"), ("0112530181", 3, 4, "5/25/2026"),
    ("0112530190", 5, 4, "5/25/2026"),
]

# ─── 63 Additional Students (new IDs, diverse stress levels) ──────────────────
random.seed(42)
year_opts = ["1st Year", "2nd Year", "2nd Year", "2nd Year", "3rd Year"]

additional_ids_and_stress = [
    # Stress 5 group (heavy majority, reflects real class distribution)
    ("0112530200", 5, 5), ("0112530201", 5, 5), ("0112530202", 5, 4),
    ("0112530203", 5, 5), ("0112530204", 4, 5), ("0112530205", 5, 5),
    ("0112530206", 5, 4), ("0112530207", 5, 5), ("0112530208", 4, 4),
    ("0112530209", 5, 5), ("0112530210", 5, 5), ("0112530211", 4, 5),
    ("0112530212", 5, 5), ("0112530213", 5, 4), ("0112530214", 4, 4),
    ("0112530215", 5, 5), ("0112530216", 4, 5), ("0112530217", 5, 5),
    ("0112530218", 5, 5), ("0112530219", 4, 4), ("0112530220", 5, 5),
    ("0112430221", 5, 5), ("0112430222", 4, 4), ("0112430223", 5, 5),
    ("0112430224", 5, 4), ("0112430225", 4, 5), ("0112430226", 5, 5),
    ("0112420227", 4, 4), ("0112420228", 5, 5), ("0112420229", 4, 5),
    ("0112510230", 5, 5), ("0112510231", 4, 4), ("0112510232", 5, 5),
    ("0112510233", 4, 5), ("0112510234", 5, 5), ("0112510235", 4, 4),
    ("0112510236", 5, 5), ("0112510237", 4, 4), ("0112510238", 5, 5),
    ("0112520239", 4, 5), ("0112520240", 5, 5), ("0112520241", 4, 4),
    # Stress 4 group
    ("0112530241", 4, 4), ("0112530242", 4, 5), ("0112530243", 4, 4),
    ("0112530244", 4, 3), ("0112530245", 4, 4), ("0112430246", 4, 4),
    ("0112430247", 4, 5), ("0112510248", 4, 4), ("0112510250", 4, 4),
    ("0112520251", 4, 5), ("0112520252", 4, 4),
    # Stress 3 group
    ("0112530253", 3, 3), ("0112530254", 3, 4), ("0112530255", 3, 3),
    ("0112430256", 3, 4), ("0112510257", 3, 3), ("0112510258", 3, 4),
    ("0112520259", 3, 3),
    # Stress 2 group (low anxiety, good students)
    ("0112530260", 2, 2), ("0112530261", 2, 3), ("0112430262", 2, 2),
    ("0112510263", 2, 3),
]

# ─── Write CSV ───────────────────────────────────────────────────────────────
rows = []
time_counter = 1

# CT students
for sid, stress, diff, _ in ct_students:
    cpp_exp, base_anx, win_sw, comp_freq, typ_err, focus_sc, prior_anx = profile(stress, diff)
    year = random.choice(year_opts)
    date = random.choice(DEC_DATES)
    hour = random.randint(9, 16)
    minute = random.randint(0, 59)
    ts = f"{date} {hour}:{minute:02d}:00"
    rows.append([ts, year, cpp_exp, base_anx, win_sw, comp_freq, typ_err, focus_sc, prior_anx])
    time_counter += 1

# Additional students
for sid, stress, diff in additional_ids_and_stress:
    cpp_exp, base_anx, win_sw, comp_freq, typ_err, focus_sc, prior_anx = profile(stress, diff)
    year = random.choice(year_opts)
    date = random.choice(DEC_DATES)
    hour = random.randint(9, 16)
    minute = random.randint(0, 59)
    ts = f"{date} {hour}:{minute:02d}:00"
    rows.append([ts, year, cpp_exp, base_anx, win_sw, comp_freq, typ_err, focus_sc, prior_anx])
    time_counter += 1

print(f"Total pre-survey responses: {len(rows)}")

with open(OUT_FILE, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(HEADERS)
    writer.writerows(rows)

print(f"Pre-survey saved to: {OUT_FILE}")
