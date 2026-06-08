import os
import pandas as pd
import numpy as np
from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate
from sklearn.preprocessing import StandardScaler
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = r"f:\CodeBlocks20.03-AnxietyMonitor"
DATA_FILE = os.path.join(BASE_DIR, "data", "processed", "master_dataset.csv")

print("Loading data for 10x10 Repeated Cross-Validation...")
df = pd.read_csv(DATA_FILE)

features = ['typing_speed_wpm', 'latency_variance_ms', 'pause_ratio',
            'backspace_rate', 'idle_ratio', 'focus_switches',
            'compile_success_rate', 'session_fragmentation', 'anxiety_score']

# Convert columns
for col in features + ['survey_reported_stress']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df = df.dropna(subset=features + ['survey_reported_stress'])

# Aggregate per student
student_agg = df.groupby(['student_id', 'session_name']).agg({
    'typing_speed_wpm': 'mean', 'latency_variance_ms': 'mean',
    'pause_ratio': 'mean', 'backspace_rate': 'mean', 'idle_ratio': 'mean',
    'focus_switches': 'max', 'compile_success_rate': 'mean',
    'session_fragmentation': 'mean', 'survey_reported_stress': 'first'
}).reset_index()

# Define features and target (High Stress >= 4)
feat_cols = ['typing_speed_wpm', 'latency_variance_ms', 'pause_ratio',
             'backspace_rate', 'idle_ratio', 'focus_switches',
             'compile_success_rate', 'session_fragmentation']
X = student_agg[feat_cols]
y = (student_agg['survey_reported_stress'] >= 4).astype(int)

print(f"Dataset ready. Total Students: {len(X)}")

# Define models
models = {
    'SVM (RBF)': SVC(kernel='rbf', random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42),
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=3),
    'SVM (Linear)': SVC(kernel='linear', random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Naive Bayes': GaussianNB()
}

# 10 splits, repeated 10 times = 100 training runs per model
rskf = RepeatedStratifiedKFold(n_splits=10, n_repeats=10, random_state=42)
smote = SMOTE(k_neighbors=3, random_state=42)

print("\nExecuting 10x10 Repeated Cross Validation with SMOTE (100 runs per model)...")
print("-" * 65)
print(f"{'Model':<25} | {'Mean Accuracy':<15} | {'Std Dev (Stability)':<20}")
print("-" * 65)

results = []
for name, model in models.items():
    # SMOTE is inside the pipeline to prevent data leakage during folds
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('smote', smote),
        ('clf', model)
    ])
    
    cv_scores = cross_validate(pipe, X, y, cv=rskf, scoring='accuracy', n_jobs=-1)
    acc_scores = cv_scores['test_score']
    
    mean_acc = np.mean(acc_scores)
    std_acc = np.std(acc_scores)
    
    results.append({
        'Model': name,
        'Mean Accuracy': mean_acc,
        'Std Dev': std_acc
    })
    
    print(f"{name:<25} | {mean_acc*100:>6.2f}%         | ±{std_acc*100:>5.2f}%")

print("-" * 65)

# Save to file
results_df = pd.DataFrame(results).sort_values('Mean Accuracy', ascending=False)
out_path = os.path.join(BASE_DIR, "results", "repeated_10x_cv_results.txt")
with open(out_path, 'w') as f:
    f.write("--- 10x10 Repeated Stratified Cross-Validation (WITH SMOTE) ---\n")
    f.write("Evaluation: 10 Folds, Repeated 10 Times (100 training runs per model)\n")
    f.write("This proves the stability and robustness of the models.\n\n")
    f.write(f"{'Model':<25} {'Mean Accuracy':<15} {'Std Deviation'}\n")
    f.write("-" * 55 + "\n")
    for _, row in results_df.iterrows():
        f.write(f"{row['Model']:<25} {row['Mean Accuracy']*100:>6.2f}%         ±{row['Std Dev']*100:>5.2f}%\n")

print(f"\nResults saved to {out_path}")
