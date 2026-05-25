import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

BASE_DIR = r"f:\CodeBlocks20.03-AnxietyMonitor"
DATA_FILE = os.path.join(BASE_DIR, "data", "processed", "master_dataset.csv")
RESULTS_DIR = os.path.join(BASE_DIR, "results", "visualizations")

os.makedirs(RESULTS_DIR, exist_ok=True)

print("Loading data...")
df = pd.read_csv(DATA_FILE)

# Data Cleaning for analysis
df['survey_reported_stress'] = pd.to_numeric(df['survey_reported_stress'], errors='coerce')
df['anxiety_score'] = pd.to_numeric(df['anxiety_score'], errors='coerce')
df = df.dropna(subset=['survey_reported_stress', 'anxiety_score'])

print(f"Data loaded. Valid rows for analysis: {len(df)}")

# 1. Statistical Correlation
# Aggregate by student to compare their average system score vs their single survey score
student_agg = df.groupby('student_id').agg({
    'anxiety_score': 'mean',
    'survey_reported_stress': 'first',
    'typing_speed_wpm': 'mean',
    'focus_switches': 'max'
}).reset_index()

pearson_corr, p_value_p = pearsonr(student_agg['anxiety_score'], student_agg['survey_reported_stress'])
spearman_corr, p_value_s = spearmanr(student_agg['anxiety_score'], student_agg['survey_reported_stress'])

print("\n--- Statistical Validation ---")
print(f"Pearson Correlation: {pearson_corr:.3f} (p-value: {p_value_p:.4f})")
print(f"Spearman Correlation: {spearman_corr:.3f} (p-value: {p_value_s:.4f})")

with open(os.path.join(BASE_DIR, "results", "statistical_summary.txt"), "w") as f:
    f.write("--- Statistical Validation ---\n")
    f.write(f"Pearson Correlation (Average System Anxiety vs Self-Reported): {pearson_corr:.3f} (p-value: {p_value_p:.4f})\n")
    f.write(f"Spearman Correlation (Average System Anxiety vs Self-Reported): {spearman_corr:.3f} (p-value: {p_value_s:.4f})\n")

# 2. Visualizations
print("\nGenerating Visualizations...")
sns.set_theme(style="whitegrid")

# Plot 1: Scatter plot
plt.figure(figsize=(8, 6))
sns.regplot(x='anxiety_score', y='survey_reported_stress', data=student_agg)
plt.title("System Anxiety Score vs Self-Reported Stress")
plt.xlabel("Average Computed Anxiety Score (0-100)")
plt.ylabel("Self-Reported Stress (1-5)")
plt.savefig(os.path.join(RESULTS_DIR, "anxiety_vs_stress_scatter.png"))
plt.close()

# Plot 2: Correlation Heatmap
numeric_cols = ['typing_speed_wpm', 'latency_variance_ms', 'pause_ratio', 
                'backspace_rate', 'idle_ratio', 'focus_switches', 
                'compile_success_rate', 'session_fragmentation', 
                'anxiety_score', 'survey_reported_stress']

# Convert columns to numeric if needed
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

corr_matrix = df[numeric_cols].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Behavioral Metrics Correlation Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "correlation_heatmap.png"))
plt.close()

print(f"Visualizations saved to {RESULTS_DIR}")
