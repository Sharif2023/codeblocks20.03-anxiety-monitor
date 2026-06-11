import nbformat as nbf
import os

os.makedirs('notebooks', exist_ok=True)
nb = nbf.v4.new_notebook()

with open('scripts/3_eda_and_stats.py', 'r', encoding='utf-8') as f:
    code1 = f.read()

with open('scripts/6_generate_visualizations.py', 'r', encoding='utf-8') as f:
    code2 = f.read()

with open('scripts/7_train_model_10x_cv.py', 'r', encoding='utf-8') as f:
    code3 = f.read()

nb['cells'] = [
    nbf.v4.new_markdown_cell('# Exploratory Data Analysis & Statistics\n\nRun this cell to calculate the Pearson and Spearman correlations.'),
    nbf.v4.new_code_cell(code1),
    nbf.v4.new_markdown_cell('# 10x10 Repeated Cross-Validation Model Training\n\nRun this cell to train the models 100 times each and view the stability.'),
    nbf.v4.new_code_cell(code3),
    nbf.v4.new_markdown_cell('# Generate Visualizations\n\nRun this cell to regenerate the charts used in the thesis.'),
    nbf.v4.new_code_cell(code2)
]

with open('notebooks/Model_Training_Analysis.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook generated successfully!")
