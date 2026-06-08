import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr
from sklearn.model_selection import cross_validate, LeaveOneOut
from sklearn.preprocessing import StandardScaler
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

BASE_DIR = r"f:\CodeBlocks20.03-AnxietyMonitor"
DATA_FILE = os.path.join(BASE_DIR, "data", "processed", "master_dataset.csv")
VIS_DIR = os.path.join(BASE_DIR, "results", "visualizations")
os.makedirs(VIS_DIR, exist_ok=True)

# Style
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 150,
})

print("Loading data...")
df = pd.read_csv(DATA_FILE)
df['survey_reported_stress'] = pd.to_numeric(df['survey_reported_stress'], errors='coerce')

features = ['typing_speed_wpm', 'latency_variance_ms', 'pause_ratio',
            'backspace_rate', 'idle_ratio', 'focus_switches',
            'compile_success_rate', 'session_fragmentation', 'anxiety_score']
for col in features + ['survey_reported_stress']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=features + ['survey_reported_stress'])

student_agg = df.groupby(['student_id', 'session_name']).agg({
    'typing_speed_wpm': 'mean', 'latency_variance_ms': 'mean',
    'pause_ratio': 'mean', 'backspace_rate': 'mean', 'idle_ratio': 'mean',
    'focus_switches': 'max', 'compile_success_rate': 'mean',
    'session_fragmentation': 'mean', 'anxiety_score': 'mean',
    'survey_reported_stress': 'first'
}).reset_index()

print(f"Total students: {len(student_agg)}")

# ─────────────────────────────────────────────
# CHART 1: Scatter Plot - System Score vs Survey
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 6))
palette = {'1st_ct': '#4C72B0', '2nd_ct': '#DD8452', '3rd_ct': '#55A868'}
for session, grp in student_agg.groupby('session_name'):
    ax.scatter(grp['anxiety_score'], grp['survey_reported_stress'],
               label=session.replace('_', ' ').title(),
               color=palette.get(session, 'gray'), s=80, alpha=0.8, edgecolors='white', linewidth=0.5)

# Regression line
m, b = np.polyfit(student_agg['anxiety_score'], student_agg['survey_reported_stress'], 1)
x_line = np.linspace(student_agg['anxiety_score'].min(), student_agg['anxiety_score'].max(), 100)
ax.plot(x_line, m*x_line + b, color='#c0392b', linewidth=2, linestyle='--', label='Trend Line')

pearson_r, p_p = pearsonr(student_agg['anxiety_score'], student_agg['survey_reported_stress'])
spearman_r, p_s = spearmanr(student_agg['anxiety_score'], student_agg['survey_reported_stress'])

ax.set_title(f'System Anxiety Score vs. Self-Reported Stress\n(N=44 students | Pearson r={pearson_r:.3f}, p={p_p:.4f} | Spearman ρ={spearman_r:.3f}, p={p_s:.4f})', fontsize=12)
ax.set_xlabel('Average Computed Anxiety Score (0–100)')
ax.set_ylabel('Self-Reported Stress Level (1–5)')
ax.set_yticks([1, 2, 3, 4, 5])
ax.legend(title='Session')
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, 'anxiety_vs_stress_scatter.png'), bbox_inches='tight')
plt.close()
print("[OK] Saved: anxiety_vs_stress_scatter.png")

# ─────────────────────────────────────────────
# CHART 2: Correlation Heatmap
# ─────────────────────────────────────────────
heatmap_cols = ['typing_speed_wpm', 'latency_variance_ms', 'pause_ratio',
                'backspace_rate', 'idle_ratio', 'focus_switches',
                'compile_success_rate', 'session_fragmentation',
                'anxiety_score', 'survey_reported_stress']
labels = ['Typing Speed\n(WPM)', 'Latency\nVariance (ms)', 'Pause\nRatio',
          'Backspace\nRate (%)', 'Idle\nRatio', 'Focus\nSwitches',
          'Compile\nSuccess Rate', 'Session\nFragmentation',
          'System\nAnxiety Score', 'Survey\nStress (1-5)']

corr = df[heatmap_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))

fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, vmin=-1, vmax=1, linewidths=0.5,
            xticklabels=labels, yticklabels=labels, ax=ax,
            annot_kws={'size': 9})
ax.set_title('Behavioral Metrics Correlation Heatmap\n(Based on 8,505 rows across 44 students — 3 Class Tests)', fontsize=13)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, 'correlation_heatmap.png'), bbox_inches='tight')
plt.close()
print("[OK] Saved: correlation_heatmap.png")

# ─────────────────────────────────────────────
# CHART 3: ML Model Comparison Bar (No SMOTE)
# ─────────────────────────────────────────────
feat_cols = ['typing_speed_wpm', 'latency_variance_ms', 'pause_ratio',
             'backspace_rate', 'idle_ratio', 'focus_switches',
             'compile_success_rate', 'session_fragmentation']
X = student_agg[feat_cols]
y_class = (student_agg['survey_reported_stress'] >= 4).astype(int)
baseline = y_class.mean()

models = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'SVM (Linear)': SVC(kernel='linear', random_state=42),
    'SVM (RBF)': SVC(kernel='rbf', random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42),
    'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=3),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Naive Bayes': GaussianNB()
}
loo = LeaveOneOut()
results_plain = []
print("\nRunning LOOCV (No SMOTE)...")
for name, model in models.items():
    pipe = Pipeline([('scaler', StandardScaler()), ('clf', model)])
    cv = cross_validate(pipe, X, y_class, cv=loo, scoring=['accuracy'])
    acc = np.mean(cv['test_accuracy'])
    results_plain.append({'Model': name, 'Accuracy': acc})
    print(f"  {name}: {acc:.3f}")

df_plain = pd.DataFrame(results_plain).sort_values('Accuracy', ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#2ecc71' if a > baseline else '#e74c3c' for a in df_plain['Accuracy']]
bars = ax.barh(df_plain['Model'], df_plain['Accuracy'], color=colors, edgecolor='white', height=0.6)
ax.axvline(x=baseline, color='#e74c3c', linestyle='--', linewidth=2, label=f'Imbalanced Baseline ({baseline:.1%})')
for bar, val in zip(bars, df_plain['Accuracy']):
    ax.text(val + 0.005, bar.get_y() + bar.get_height()/2, f'{val:.1%}', va='center', fontsize=10, fontweight='bold')
ax.set_xlabel('LOOCV Accuracy')
ax.set_title('ML Model Comparison — LOOCV Accuracy (Without SMOTE)\n44 Students | 3 Class Tests | Task: Predict High Stress (≥4) vs Low Stress (<4)', fontsize=12)
ax.set_xlim(0, 1.05)
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, 'model_comparison_bar.png'), bbox_inches='tight')
plt.close()
print("[OK] Saved: model_comparison_bar.png")

# ─────────────────────────────────────────────
# CHART 4: ML Model Comparison Bar (SMOTE)
# ─────────────────────────────────────────────
smote = SMOTE(k_neighbors=3, random_state=42)
results_smote = []
print("\nRunning LOOCV (With SMOTE)...")
for name, model in models.items():
    pipe = Pipeline([('scaler', StandardScaler()), ('smote', smote), ('clf', model)])
    cv = cross_validate(pipe, X, y_class, cv=loo, scoring=['accuracy'])
    acc = np.mean(cv['test_accuracy'])
    results_smote.append({'Model': name, 'Accuracy': acc})
    print(f"  {name}: {acc:.3f}")

df_smote = pd.DataFrame(results_smote).sort_values('Accuracy', ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#3498db' if a > 0.5 else '#e74c3c' for a in df_smote['Accuracy']]
bars = ax.barh(df_smote['Model'], df_smote['Accuracy'], color=colors, edgecolor='white', height=0.6)
ax.axvline(x=0.5, color='#e74c3c', linestyle='--', linewidth=2, label='Random Guessing Baseline (50%)')
for bar, val in zip(bars, df_smote['Accuracy']):
    ax.text(val + 0.005, bar.get_y() + bar.get_height()/2, f'{val:.1%}', va='center', fontsize=10, fontweight='bold')
ax.set_xlabel('LOOCV Accuracy')
ax.set_title('ML Model Comparison — LOOCV Accuracy (With SMOTE Balancing)\n44 Students | 3 Class Tests | Balanced Classes | 50% = Random Guessing', fontsize=12)
ax.set_xlim(0, 1.05)
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, 'smote_model_comparison_bar.png'), bbox_inches='tight')
plt.close()
print("[OK] Saved: smote_model_comparison_bar.png")

# ─────────────────────────────────────────────
# CHART 5: Stress Distribution by Session
# ─────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: Distribution of survey stress levels
stress_counts = student_agg['survey_reported_stress'].value_counts().sort_index()
colors_bar = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c', '#c0392b']
axes[0].bar(stress_counts.index, stress_counts.values, color=colors_bar[:len(stress_counts)], edgecolor='white')
axes[0].set_title('Distribution of Self-Reported Stress Levels\n(N=44 students)')
axes[0].set_xlabel('Stress Level (1=Low, 5=High)')
axes[0].set_ylabel('Number of Students')
axes[0].set_xticks([1,2,3,4,5])
for i, v in zip(stress_counts.index, stress_counts.values):
    axes[0].text(i, v + 0.2, str(v), ha='center', fontweight='bold')

# Right: Avg anxiety score by session
session_avg = student_agg.groupby('session_name')['anxiety_score'].mean().reset_index()
session_avg['session_name'] = session_avg['session_name'].str.replace('_', ' ').str.title()
session_colors = ['#4C72B0', '#DD8452', '#55A868']
axes[1].bar(session_avg['session_name'], session_avg['anxiety_score'], color=session_colors, edgecolor='white')
axes[1].set_title('Average System Anxiety Score by Session\n(N=44 students across 3 Class Tests)')
axes[1].set_xlabel('Class Test Session')
axes[1].set_ylabel('Average Anxiety Score (0–100)')
axes[1].set_ylim(0, 100)
for i, v in enumerate(session_avg['anxiety_score']):
    axes[1].text(i, v + 1, f'{v:.1f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, 'stress_distribution_by_session.png'), bbox_inches='tight')
plt.close()
print("[OK] Saved: stress_distribution_by_session.png")

# ─────────────────────────────────────────────
# CHART 6: Feature Importance (Random Forest)
# ─────────────────────────────────────────────
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.preprocessing import StandardScaler as SS

scaler = SS()
X_scaled = scaler.fit_transform(X)
rf = RFC(n_estimators=200, random_state=42)
rf.fit(X_scaled, y_class)
importances = pd.DataFrame({'Feature': feat_cols, 'Importance': rf.feature_importances_})
importances = importances.sort_values('Importance', ascending=True)
feat_labels = {
    'typing_speed_wpm': 'Typing Speed (WPM)',
    'latency_variance_ms': 'Latency Variance (ms)',
    'pause_ratio': 'Pause Ratio',
    'backspace_rate': 'Backspace Rate (%)',
    'idle_ratio': 'Idle Ratio',
    'focus_switches': 'Focus Switches',
    'compile_success_rate': 'Compile Success Rate',
    'session_fragmentation': 'Session Fragmentation'
}
importances['Feature'] = importances['Feature'].map(feat_labels)

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(importances['Feature'], importances['Importance'], color='#3498db', edgecolor='white')
for bar, val in zip(bars, importances['Importance']):
    ax.text(val + 0.002, bar.get_y() + bar.get_height()/2, f'{val:.3f}', va='center', fontsize=10)
ax.set_xlabel('Feature Importance Score')
ax.set_title('Random Forest — Feature Importances for Anxiety Prediction\n(Trained on 44 students | All 3 Class Tests)', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, 'feature_importance.png'), bbox_inches='tight')
plt.close()
print("[OK] Saved: feature_importance.png")

print("[DONE] All visualizations regenerated successfully!")
print(f"Saved to: {VIS_DIR}")
