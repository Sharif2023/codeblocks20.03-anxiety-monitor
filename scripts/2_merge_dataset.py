import os
import csv
import glob

BASE_DIR = r"f:\CodeBlocks20.03-AnxietyMonitor"
CLEANED_DIR = os.path.join(BASE_DIR, "data", "processed", "cleaned_sessions")
MASTER_CSV = os.path.join(BASE_DIR, "data", "processed", "master_dataset.csv")

folders_to_merge = ["1st_ct", "2nd_ct"]

all_rows = []
fieldnames = []

for folder in folders_to_merge:
    folder_path = os.path.join(CLEANED_DIR, folder)
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    
    for file_path in csv_files:
        filename = os.path.basename(file_path)
        student_id = filename.replace(".csv", "").strip()
        
        with open(file_path, 'r', encoding='utf-8') as fin:
            reader = csv.DictReader(fin)
            if not fieldnames:
                fieldnames = list(reader.fieldnames)
                if 'session_name' not in fieldnames:
                    fieldnames.append('session_name')
                if 'student_id' not in fieldnames:
                    fieldnames.append('student_id')
            
            for row in reader:
                row['session_name'] = folder
                row['student_id'] = student_id
                all_rows.append(row)

if fieldnames:
    # Reorder fieldnames to put student_id and session_name at the front
    if 'student_id' in fieldnames:
        fieldnames.remove('student_id')
    if 'session_name' in fieldnames:
        fieldnames.remove('session_name')
    new_fieldnames = ['student_id', 'session_name'] + fieldnames
    
    print(f"Merging {len(all_rows)} total rows from {len(folders_to_merge)} sessions...")
    
    with open(MASTER_CSV, 'w', encoding='utf-8', newline='') as fout:
        writer = csv.DictWriter(fout, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
    
    print(f"Master dataset successfully created at: {MASTER_CSV}")
else:
    print("No data found to merge.")
