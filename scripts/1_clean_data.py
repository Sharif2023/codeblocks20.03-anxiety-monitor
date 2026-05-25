import os
import csv
import glob

# Paths
BASE_DIR = r"f:\CodeBlocks20.03-AnxietyMonitor"
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
SURVEY_FILE = os.path.join(RAW_DIR, "post_survey", "post-survey.csv")
CLEANED_DIR = os.path.join(BASE_DIR, "data", "processed", "cleaned_sessions")

# Ensure output directories exist
os.makedirs(os.path.join(CLEANED_DIR, "1st_ct"), exist_ok=True)
os.makedirs(os.path.join(CLEANED_DIR, "2nd_ct"), exist_ok=True)

def load_survey_data():
    survey_dict = {}
    try:
        with open(SURVEY_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Find the exact column names
            student_id_col = [c for c in reader.fieldnames if "Student ID" in c][0]
            stress_col = [c for c in reader.fieldnames if "how anxious or stressed" in c][0]
            difficulty_col = [c for c in reader.fieldnames if "How difficult" in c][0]
            
            for row in reader:
                sid = str(row[student_id_col]).strip()
                if sid:
                    survey_dict[sid] = {
                        'reported_stress': row[stress_col],
                        'reported_difficulty': row[difficulty_col]
                    }
        return survey_dict
    except Exception as e:
        print(f"Error loading survey data: {e}")
        return {}

def process_ct_folder(folder_name, survey_dict):
    input_folder = os.path.join(RAW_DIR, folder_name)
    output_folder = os.path.join(CLEANED_DIR, folder_name)
    
    csv_files = glob.glob(os.path.join(input_folder, "*.csv"))
    print(f"Processing {len(csv_files)} files in {folder_name}...")
    
    for file_path in csv_files:
        filename = os.path.basename(file_path)
        student_id = filename.replace(".csv", "").strip()
        
        out_path = os.path.join(output_folder, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as fin, open(out_path, 'w', encoding='utf-8', newline='') as fout:
                reader = csv.DictReader(fin)
                
                # Setup output headers
                fieldnames = list(reader.fieldnames)
                if 'survey_reported_stress' not in fieldnames:
                    fieldnames.append('survey_reported_stress')
                if 'survey_reported_difficulty' not in fieldnames:
                    fieldnames.append('survey_reported_difficulty')
                    
                writer = csv.DictWriter(fout, fieldnames=fieldnames)
                writer.writeheader()
                
                survey_stress = survey_dict.get(student_id, {}).get('reported_stress', '')
                survey_diff = survey_dict.get(student_id, {}).get('reported_difficulty', '')
                
                has_started_typing = False
                
                for row in reader:
                    # Check for warm-up period
                    if not has_started_typing:
                        try:
                            keys = int(row.get('keystrokes_total', 0))
                            if keys > 0:
                                has_started_typing = True
                            else:
                                continue
                        except ValueError:
                            pass
                            
                    # Cap latency_variance_ms
                    try:
                        lat_var = float(row.get('latency_variance_ms', 0))
                        if lat_var > 30000.0:
                            row['latency_variance_ms'] = '30000.0'
                    except ValueError:
                        pass
                        
                    # Append Survey Data
                    row['survey_reported_stress'] = survey_stress
                    row['survey_reported_difficulty'] = survey_diff
                    
                    writer.writerow(row)
                    
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    survey_data = load_survey_data()
    print(f"Loaded survey data for {len(survey_data)} students.")
    
    process_ct_folder("1st_ct", survey_data)
    process_ct_folder("2nd_ct", survey_data)
    
    print("Data cleaning complete. Cleaned files saved to data/processed/cleaned_sessions.")
