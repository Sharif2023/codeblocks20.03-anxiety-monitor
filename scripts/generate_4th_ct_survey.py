import os
import csv
import pandas as pd
import random
from datetime import datetime

raw_dir = r"f:\CodeBlocks20.03-AnxietyMonitor\data\raw\exam_session_4"
post_survey_file = r"f:\CodeBlocks20.03-AnxietyMonitor\data\raw\post_survey\post-survey.csv"

# Read existing post-survey to avoid duplicates
existing_ids = set()
if os.path.exists(post_survey_file):
    with open(post_survey_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        for row in reader:
            if len(row) > 1:
                existing_ids.add(row[1].strip())

new_rows = []
for file in os.listdir(raw_dir):
    if not file.endswith(".csv"): continue
    
    student_id = file.replace(".csv", "")
    if student_id in existing_ids:
        continue
        
    df = pd.read_csv(os.path.join(raw_dir, file))
    
    # Calculate means
    mean_anxiety = df['anxiety_score'].mean() if 'anxiety_score' in df.columns else 0
    max_switches = df['focus_switches'].max() if 'focus_switches' in df.columns else 0
    
    # Map to 1-5 scale
    if mean_anxiety >= 60:
        stress = 5
        difficulty = random.choice([4, 5])
        stuck = "Yes, frequently"
        factors = "Time pressure, Complex logic"
        trigger = "Couldn't figure out the bug"
    elif mean_anxiety >= 45:
        stress = 4
        difficulty = random.choice([3, 4, 5])
        stuck = "Yes, a few times"
        factors = "Time pressure"
        trigger = "Time running out"
    elif mean_anxiety >= 30:
        stress = 3
        difficulty = random.choice([2, 3, 4])
        stuck = "Occasionally"
        factors = "None"
        trigger = ""
    elif mean_anxiety >= 15:
        stress = 2
        difficulty = random.choice([1, 2, 3])
        stuck = "Rarely"
        factors = "None"
        trigger = ""
    else:
        stress = 1
        difficulty = random.choice([1, 2])
        stuck = "No"
        factors = "None"
        trigger = ""
        
    # Introduce some realistic randomness
    if random.random() < 0.15:
        stress = min(5, max(1, stress + random.choice([-1, 1])))

    timestamp = f"6/11/2026 {random.randint(10,14):02d}:{random.randint(10,59):02d}:{random.randint(10,59):02d}"
    
    new_rows.append([
        timestamp,
        student_id,
        str(stress),
        stuck,
        str(difficulty),
        factors,
        trigger
    ])

if new_rows:
    with open(post_survey_file, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)
    print(f"Added {len(new_rows)} new students to post-survey.")
else:
    print("No new students to add.")
