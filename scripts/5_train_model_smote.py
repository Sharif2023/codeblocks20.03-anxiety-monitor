import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import cross_validate, LeaveOneOut
from sklearn.preprocessing import StandardScaler

# Import imblearn pipeline instead of sklearn pipeline to prevent data leakage
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE

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

print("Loading data for SMOTE ML comparison...")
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

# Define Models
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
results = []

# Because we only have 5 samples of the minority class, k_neighbors must be <= 4.
smote = SMOTE(k_neighbors=3, random_state=42)

print("\nEvaluating models using LOOCV with SMOTE data balancing...")
for name, model in models.items():
    # Pipeline ensures SMOTE is only applied to the training data in each LOOCV fold
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('smote', smote),
        ('classifier', model)
    ])
    
    cv_results = cross_validate(pipeline, X, y_class, cv=loo, scoring=['accuracy'])
    acc = np.mean(cv_results['test_accuracy'])
    
    results.append({'Model': name, 'LOOCV Accuracy (SMOTE)': acc})
    print(f"{name}: {acc:.3f}")

results_df = pd.DataFrame(results).sort_values(by='LOOCV Accuracy (SMOTE)', ascending=False)

# Save Text Results
with open(os.path.join(RESULTS_DIR, "smote_ml_comparison.txt"), "w") as f:
    f.write("--- Machine Learning Classification Comparison (WITH SMOTE) ---\n")
    f.write("Evaluation Method: Leave-One-Out Cross-Validation (LOOCV)\n")
    f.write("Data Balancing: SMOTE applied inside the cross-validation loop to prevent data leakage.\n\n")
    f.write(results_df.to_string(index=False) + "\n\n")
    f.write("Note: By balancing the classes during training, the models are forced to learn true behavioral patterns ")
    f.write("instead of simply guessing the majority class. Any accuracy achieved here is much more scientifically valid.")

# Generate Visualization
plt.figure(figsize=(12, 6))
sns.barplot(x='LOOCV Accuracy (SMOTE)', y='Model', data=results_df, color='#4c72b0')
plt.title("Machine Learning Models Comparison (LOOCV Accuracy with SMOTE Balancing)")
plt.xlabel("Cross-Validation Accuracy")
plt.ylabel("Algorithm")
plt.axvline(x=0.5, color='red', linestyle='--', label='Random Guessing Baseline (50%)')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "smote_model_comparison_bar.png"))
plt.close()

print(f"\nComparison complete. Results saved to {RESULTS_DIR}")
