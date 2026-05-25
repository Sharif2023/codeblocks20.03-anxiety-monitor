import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import cross_validate, LeaveOneOut
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Machine Learning Models
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

BASE_DIR = r"f:\CodeBlocks20.03-AnxietyMonitor"
DATA_FILE = os.path.join(BASE_DIR, "data", "processed", "master_dataset.csv")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
VIS_DIR = os.path.join(RESULTS_DIR, "visualizations")

os.makedirs(VIS_DIR, exist_ok=True)

print("Loading data for comprehensive ML comparison...")
df = pd.read_csv(DATA_FILE)

# Clean and prepare
df['survey_reported_stress'] = pd.to_numeric(df['survey_reported_stress'], errors='coerce')
df = df.dropna(subset=['survey_reported_stress'])

features = ['typing_speed_wpm', 'latency_variance_ms', 'pause_ratio', 
            'backspace_rate', 'idle_ratio', 'focus_switches', 
            'compile_success_rate', 'session_fragmentation']

for col in features:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=features)

# Aggregate by student
student_agg = df.groupby('student_id').agg({
    'typing_speed_wpm': 'mean',
    'latency_variance_ms': 'mean',
    'pause_ratio': 'mean',
    'backspace_rate': 'mean',
    'idle_ratio': 'mean',
    'focus_switches': 'max',
    'compile_success_rate': 'mean',
    'session_fragmentation': 'mean',
    'survey_reported_stress': 'first'
}).reset_index()

X = student_agg[features]
y = student_agg['survey_reported_stress']

# Binary Classification: High Stress (>= 4) vs Low/Moderate (< 4)
y_class = (y >= 4).astype(int)

print(f"Dataset ready. Total Students: {len(X)}")
print(f"High Stress cases: {sum(y_class == 1)}, Low/Mod Stress cases: {sum(y_class == 0)}")

# Define Models for Comparison
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

# Since we have a small dataset (31), Leave-One-Out Cross-Validation (LOOCV) is the most robust metric.
loo = LeaveOneOut()

results = []

print("\nEvaluating models using Leave-One-Out Cross-Validation (LOOCV)...")
for name, model in models.items():
    # It's vital to scale features, especially for SVM, KNN, and Logistic Regression
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', model)
    ])
    
    cv_results = cross_validate(pipeline, X, y_class, cv=loo, scoring=['accuracy'])
    acc = np.mean(cv_results['test_accuracy'])
    
    results.append({'Model': name, 'LOOCV Accuracy': acc})
    print(f"{name}: {acc:.3f}")

results_df = pd.DataFrame(results).sort_values(by='LOOCV Accuracy', ascending=False)

# Save Text Results
with open(os.path.join(RESULTS_DIR, "comprehensive_ml_comparison.txt"), "w") as f:
    f.write("--- Comprehensive Machine Learning Classification Comparison ---\n")
    f.write("Evaluation Method: Leave-One-Out Cross-Validation (LOOCV)\n")
    f.write("Task: Predicting High Stress (>=4) vs Low/Mod Stress (<4)\n\n")
    f.write(results_df.to_string(index=False) + "\n\n")
    
    f.write("Note: Because the dataset has class imbalance (more High Stress than Low), ")
    f.write("a baseline model always predicting 'High Stress' would get around ~74% accuracy.\n")
    f.write("Models scoring higher than the baseline have successfully learned behavioral patterns.")

# Generate Visualization
plt.figure(figsize=(12, 6))
sns.barplot(x='LOOCV Accuracy', y='Model', data=results_df, palette='viridis')
plt.title("Machine Learning Models Comparison (Leave-One-Out Accuracy)")
plt.xlabel("Cross-Validation Accuracy")
plt.ylabel("Algorithm")
plt.axvline(x=sum(y_class == 1)/len(y_class), color='red', linestyle='--', label='Baseline (Always predict High Stress)')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "model_comparison_bar.png"))
plt.close()

print(f"\nComparison complete. Results saved to {RESULTS_DIR}")
