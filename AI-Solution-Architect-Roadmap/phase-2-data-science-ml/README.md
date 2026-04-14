# Phase 2: Classical Machine Learning & Data Science

> **Duration:** 6–8 weeks  
> **Prerequisite:** Phase 1 complete  
> **Goal:** Understand the ML problem-solving loop end-to-end, train and evaluate models, and know when to use which algorithm

---

## The Machine Learning Problem-Solving Loop

```
Define Problem
     ↓
Collect & Understand Data (EDA)
     ↓
Feature Engineering & Preprocessing
     ↓
Choose & Train Model
     ↓
Evaluate Model
     ↓
Improve (tune hyperparameters, add features, fix data)
     ↓
Deploy & Monitor
```

This loop is the same whether you're building a $10K prototype or a $10M production system. The architecture around it changes — the loop doesn't.

---

## Module 2.1 — Types of Machine Learning Problems

### Supervised Learning
Model learns from labeled examples to predict outputs.

| Problem Type | Example | Output |
|-------------|---------|--------|
| Binary Classification | Will this user churn? | 0 or 1 |
| Multi-class Classification | What OS is this device on? | One of N classes |
| Regression | How long will this session last? | Continuous number |
| Ranking | Which app feature is most relevant? | Ordered list |

### Unsupervised Learning
Model finds structure in data without labels.

| Problem Type | Example | Output |
|-------------|---------|--------|
| Clustering | Group users by behavior | Cluster assignments |
| Dimensionality Reduction | Compress 1000-feature user vector | Lower-dim representation |
| Anomaly Detection | Flag unusual crash patterns | Anomaly score |

### Reinforcement Learning
Agent learns to take actions to maximize reward.

Examples: Game AI, recommendation systems, ad bidding, robotics.

---

## Module 2.2 — Exploratory Data Analysis (EDA)

EDA is non-negotiable. Never build a model without understanding your data first.

**EDA Checklist:**
- [ ] Shape and data types — how many rows, columns, what types?
- [ ] Missing values — how many, which columns, what pattern?
- [ ] Distributions — is target variable balanced? Are features skewed?
- [ ] Correlations — which features correlate with the target?
- [ ] Outliers — are there extreme values that will corrupt training?
- [ ] Data leakage — are any features actually derived from the target?

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Standard EDA starter
def quick_eda(df, target_col):
    print(f"Shape: {df.shape}")
    print(f"\nData Types:\n{df.dtypes}")
    print(f"\nNull counts:\n{df.isnull().sum()}")
    print(f"\nTarget distribution:\n{df[target_col].value_counts(normalize=True)}")
    
    # Correlation heatmap
    numeric_df = df.select_dtypes(include=[np.number])
    plt.figure(figsize=(12, 8))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', center=0)
    plt.title('Feature Correlation Matrix')
    plt.show()
    
    # Target class distribution
    plt.figure(figsize=(6, 4))
    df[target_col].value_counts().plot(kind='bar')
    plt.title(f'Target Distribution: {target_col}')
    plt.show()
```

---

## Module 2.3 — Feature Engineering

**The most important skill in classical ML.** Good features > complex model every time.

### Feature Types and Transformations

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

# --- Numerical Features ---

# 1. Normalization (scale to 0-1)
df['feature_normalized'] = (df['feature'] - df['feature'].min()) / (df['feature'].max() - df['feature'].min())

# 2. Standardization (zero mean, unit variance) — most common
scaler = StandardScaler()
df[['feature_scaled']] = scaler.fit_transform(df[['feature']])

# 3. Log transform — for right-skewed distributions (income, session length)
df['log_duration'] = np.log1p(df['session_duration'])  # log1p handles zero

# 4. Binning continuous to categorical
df['duration_bucket'] = pd.cut(df['session_duration'], bins=[0, 30, 120, 600, np.inf],
                                 labels=['very_short', 'short', 'medium', 'long'])

# --- Categorical Features ---

# 5. One-hot encoding — for nominal categories (no inherent order)
df_encoded = pd.get_dummies(df, columns=['os_version', 'device_type'])

# 6. Label encoding — for ordinal categories (has natural order)
le = LabelEncoder()
df['priority_encoded'] = le.fit_transform(df['priority'])  # low=0, medium=1, high=2

# 7. Target encoding — replace category with mean of target
target_mean = df.groupby('app_version')['will_crash'].mean()
df['app_version_target_enc'] = df['app_version'].map(target_mean)

# --- Datetime Features ---
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
df['days_since_launch'] = (df['timestamp'] - df['timestamp'].min()).dt.days

# --- Interaction Features ---
df['memory_per_session'] = df['memory_mb'] / (df['session_duration_s'] + 1)
df['crash_rate_x_version'] = df['app_version_target_enc'] * df['memory_normalized']
```

### Handling Missing Values

```python
# Strategy 1: Drop rows with missing values (only if few rows affected)
df_clean = df.dropna(subset=['critical_feature'])

# Strategy 2: Mean/median imputation (numerical)
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='median')
df[['age', 'income']] = imputer.fit_transform(df[['age', 'income']])

# Strategy 3: Mode imputation (categorical)
df['device'].fillna(df['device'].mode()[0], inplace=True)

# Strategy 4: Model-based imputation (advanced)
from sklearn.impute import KNNImputer
knn_imputer = KNNImputer(n_neighbors=5)
df_imputed = knn_imputer.fit_transform(df)
```

---

## Module 2.4 — Core ML Algorithms

### Algorithm 1: Linear Regression

**Use when:** Predicting a continuous number (price, duration, revenue).

**Math intuition:** Draw the best-fit line through your data points.

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Prepare data
X = df[['session_duration_s', 'memory_mb', 'days_since_install']]
y = df['revenue']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = LinearRegression()
model.fit(X_train, y_train)

# Predict & Evaluate
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
print(f"RMSE: {rmse:.2f}")   # Lower is better
print(f"R²: {r2:.3f}")       # Closer to 1 is better

# Interpret coefficients
coef_df = pd.DataFrame({'feature': X.columns, 'coefficient': model.coef_})
print(coef_df.sort_values('coefficient', key=abs, ascending=False))
```

### Algorithm 2: Logistic Regression

**Use when:** Binary classification (will churn: yes/no, is spam: yes/no).

**Math intuition:** Linear regression squashed through a sigmoid function to output probabilities.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

X = df[['session_duration_s', 'memory_mb', 'crashes_last_week', 'days_since_install']]
y = df['churned']  # 0 or 1

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]  # Probability of class 1

print(classification_report(y_test, y_pred))
print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.3f}")

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Not Churned', 'Churned'],
            yticklabels=['Not Churned', 'Churned'])
plt.title('Confusion Matrix')
plt.show()
```

### Algorithm 3: Decision Trees & Random Forest

**Use when:** Tabular data, need interpretability, handle mixed types well.

**Math intuition:** Trees split data on features to maximize information gain. Random Forest = hundreds of trees trained on random subsets, then voted.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import plot_tree

# Random Forest — often best starting point for tabular data
rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)

# Feature importance — critical for understanding your data
importances = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

plt.figure(figsize=(8, 5))
sns.barplot(data=importances, x='importance', y='feature')
plt.title('Random Forest Feature Importance')
plt.show()
```

### Algorithm 4: Gradient Boosting (XGBoost / LightGBM)

**Use when:** Tabular data competitions, highest accuracy on structured data, production models.

**This is the most powerful classical ML algorithm for tabular data.**

```python
import xgboost as xgb
from sklearn.model_selection import cross_val_score

# XGBoost — industry standard for tabular prediction
model = xgb.XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric='logloss',
    early_stopping_rounds=20,
    random_state=42
)

model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=50
)

# Cross-validation — more reliable than single train/test split
cv_scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
print(f"CV AUC: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
```

### Algorithm 5: K-Means Clustering (Unsupervised)

**Use when:** You have no labels and want to discover natural groupings.

**Example use case:** Segment users by behavior — power users vs casual vs at-risk.

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Features for user segmentation
features = ['daily_sessions', 'avg_session_duration', 'features_used', 'days_since_last_open']
X = df[features]

# Scale first (K-means is distance-based, scale matters)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Find optimal k with elbow method
inertias = []
k_range = range(2, 11)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

plt.plot(k_range, inertias, 'bo-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method — Find Optimal k')
plt.show()

# Train with chosen k
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['segment'] = kmeans.fit_predict(X_scaled)

# Interpret segments
print(df.groupby('segment')[features].mean())
```

---

## Module 2.5 — Model Evaluation Deep Dive

### For Classification

| Metric | Formula | When to Use |
|--------|---------|-------------|
| Accuracy | Correct / Total | Only when classes are balanced |
| Precision | TP / (TP + FP) | When false positives are costly (spam filter) |
| Recall | TP / (TP + FN) | When false negatives are costly (disease detection) |
| F1 Score | 2 × (P × R) / (P + R) | Balanced tradeoff |
| ROC-AUC | Area under ROC curve | Best single metric for most classifiers |
| PR-AUC | Precision-Recall curve area | Better for highly imbalanced datasets |

```python
from sklearn.metrics import roc_curve, auc

# ROC Curve
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC Curve (AUC = {roc_auc:.3f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()
```

### For Regression

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

print(f"MAE: {mae:.2f}")    # Average absolute error
print(f"RMSE: {rmse:.2f}")  # Penalizes large errors more
print(f"R²: {r2:.3f}")     # Proportion of variance explained
print(f"MAPE: {mape:.2f}%") # Mean absolute percentage error
```

### Dealing With Imbalanced Data

A very common real-world problem (churn: 2% positive, fraud: 0.1% positive).

```python
from sklearn.utils import class_weight
from imblearn.over_sampling import SMOTE

# Strategy 1: Class weights — tell the model to penalize minority class misses more
weights = class_weight.compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
model = XGBClassifier(scale_pos_weight=weights[1]/weights[0])

# Strategy 2: SMOTE — synthetically oversample minority class
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
print(f"Before SMOTE: {y_train.value_counts().to_dict()}")
print(f"After SMOTE: {pd.Series(y_resampled).value_counts().to_dict()}")
```

---

## Module 2.6 — Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

# Grid Search — exhaustive but slow
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [4, 6, 8],
    'learning_rate': [0.01, 0.05, 0.1]
}

grid_search = GridSearchCV(
    xgb.XGBClassifier(),
    param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)
grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")
print(f"Best AUC: {grid_search.best_score_:.3f}")

# For production: use Optuna (Bayesian optimization, much faster)
import optuna

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0)
    }
    model = xgb.XGBClassifier(**params)
    scores = cross_val_score(model, X_train, y_train, cv=3, scoring='roc_auc')
    return scores.mean()

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)
print(f"Best: {study.best_params}")
```

---

## Module 2.7 — Scikit-learn Pipelines

**Critical for production.** Prevent data leakage between train and test sets.

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

# Define feature groups
numerical_features = ['session_duration_s', 'memory_mb', 'crashes_last_week']
categorical_features = ['os_version', 'device_type']

# Build preprocessing pipelines
numerical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

# Combine preprocessors
preprocessor = ColumnTransformer([
    ('num', numerical_pipeline, numerical_features),
    ('cat', categorical_pipeline, categorical_features)
])

# Full pipeline including model
full_pipeline = Pipeline([
    ('preprocessing', preprocessor),
    ('model', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train, evaluate, save — all preprocessing applied consistently
full_pipeline.fit(X_train, y_train)
print(f"Test AUC: {roc_auc_score(y_test, full_pipeline.predict_proba(X_test)[:,1]):.3f}")

# Save pipeline (includes preprocessor + model)
import joblib
joblib.dump(full_pipeline, 'churn_model.pkl')

# Load and predict in production
pipeline = joblib.load('churn_model.pkl')
new_predictions = pipeline.predict_proba(new_data)
```

---

## Module 2.8 — Model Interpretability

As an architect, you must be able to explain *why* a model made a decision — to stakeholders, regulators, and engineers.

```python
import shap

# SHAP values — game theory-based feature attribution
explainer = shap.TreeExplainer(rf_model)
shap_values = explainer.shap_values(X_test)

# Summary plot — global feature importance
shap.summary_plot(shap_values[1], X_test, feature_names=X.columns)

# Waterfall plot — explain one prediction
shap.waterfall_plot(shap.Explanation(
    values=shap_values[1][0],
    base_values=explainer.expected_value[1],
    data=X_test.iloc[0],
    feature_names=X.columns
))
```

---

## Phase 2 Capstone Project

**Project: User Churn Prediction System**

Build an end-to-end ML system that predicts which mobile app users will churn in the next 30 days.

**Requirements:**
1. Generate or use a public mobile user dataset (e.g., from Kaggle)
2. Perform thorough EDA with at least 8 visualizations
3. Engineer at least 10 new features from raw data
4. Train and compare 3 models: Logistic Regression, Random Forest, XGBoost
5. Evaluate with ROC-AUC, F1, and confusion matrices
6. Interpret the best model using SHAP
7. Build a Scikit-learn pipeline
8. Export the model with joblib and write a `predict(user_features) → churn_probability` function

**Why this project:** Churn prediction is one of the most common ML use cases in mobile apps. Every mobile company has this problem. Being able to say "I built a production-ready churn model for a mobile app" is a concrete, credible deliverable.

---

## Phase 2 Completion Checklist

- [ ] Understand supervised vs unsupervised learning and know which to apply when
- [ ] Can perform thorough EDA on any tabular dataset
- [ ] Can engineer features from raw data (encode, scale, impute, derive)
- [ ] Trained and evaluated Linear Regression, Logistic Regression, Random Forest, XGBoost
- [ ] Understand accuracy vs precision vs recall vs ROC-AUC
- [ ] Know how to handle imbalanced datasets
- [ ] Built a Scikit-learn pipeline (no data leakage)
- [ ] Interpreted a model using SHAP values
- [ ] Completed the churn prediction capstone project

**When all boxes are checked → move to [Phase 3](../phase-3-deep-learning/README.md)**
