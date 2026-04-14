# Phase 5: MLOps & AI Engineering

> **Duration:** 6–8 weeks  
> **Prerequisite:** Phase 4 complete  
> **Goal:** Build production AI systems with monitoring, CI/CD, versioning, and reliability engineering

---

## Why MLOps Is Non-Negotiable for Architects

A model that works in a notebook is not a product. The gap between "prototype" and "production" in ML is enormous:

| Prototype | Production |
|-----------|-----------|
| Single Jupyter notebook | Modular, testable code |
| Manual training | Automated retraining pipelines |
| No version control for data/models | Data versioning (DVC), Model registry |
| No monitoring | Data drift, model drift, business metric alerts |
| Works on one machine | Containerized, scalable, reproducible |
| No rollback | A/B testing, canary deploys, instant rollback |

As a Solution Architect, you don't need to implement all of this yourself — but you must be able to **design** it, **review** it, and **explain** it to engineering teams.

---

## Module 5.1 — MLOps Lifecycle

```
Data Ingestion & Versioning
         ↓
Feature Engineering & Feature Store
         ↓
Experiment Tracking (train multiple models, log metrics)
         ↓
Model Registry (store versioned models with metadata)
         ↓
CI/CD Pipeline (test → package → deploy)
         ↓
Model Serving (batch or real-time inference)
         ↓
Monitoring (data drift, model drift, latency, business metrics)
         ↓
Retraining Trigger → back to top
```

---

## Module 5.2 — Experiment Tracking with MLflow

Every training run should be logged. This lets you compare models, reproduce results, and justify decisions to stakeholders.

```python
import mlflow
import mlflow.sklearn
import mlflow.pytorch
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
import pandas as pd
import numpy as np

# Start MLflow experiment
mlflow.set_experiment("churn_prediction_v2")

def train_and_log(X_train, y_train, X_test, y_test, params: dict):
    with mlflow.start_run(run_name=f"rf_{params['n_estimators']}trees"):
        
        # Log parameters
        mlflow.log_params(params)
        mlflow.log_param("train_size", len(X_train))
        mlflow.log_param("n_features", X_train.shape[1])
        
        # Train model
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)
        
        # Log metrics
        train_auc = roc_auc_score(y_train, model.predict_proba(X_train)[:,1])
        test_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:,1])
        
        mlflow.log_metric("train_auc", train_auc)
        mlflow.log_metric("test_auc", test_auc)
        mlflow.log_metric("overfit_gap", train_auc - test_auc)
        
        # Log model artifact
        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            registered_model_name="churn_predictor",
            input_example=X_test.iloc[:5]
        )
        
        # Log feature importance plot
        import matplotlib.pyplot as plt
        importances = pd.Series(model.feature_importances_, index=X_train.columns)
        fig, ax = plt.subplots(figsize=(10, 6))
        importances.sort_values().plot(kind='barh', ax=ax)
        ax.set_title('Feature Importance')
        mlflow.log_figure(fig, "feature_importance.png")
        plt.close()
        
        print(f"Run logged. Test AUC: {test_auc:.4f}")
        return test_auc

# Run experiments
param_grid = [
    {"n_estimators": 100, "max_depth": 6, "random_state": 42},
    {"n_estimators": 200, "max_depth": 8, "random_state": 42},
    {"n_estimators": 300, "max_depth": 10, "random_state": 42},
]

for params in param_grid:
    train_and_log(X_train, y_train, X_test, y_test, params)

# Launch UI: mlflow ui → http://localhost:5000
```

---

## Module 5.3 — Data Versioning with DVC

```bash
# Initialize DVC in your project
git init
dvc init

# Track your dataset
dvc add data/training_data.csv
git add data/training_data.csv.dvc .dvcignore
git commit -m "Track training data with DVC"

# Store data in remote (S3, GCS, Azure Blob)
dvc remote add -d myremote s3://my-bucket/dvc-store
dvc push

# On another machine or in CI
dvc pull   # Download the exact dataset version

# When data changes, create a new version
dvc add data/training_data.csv
git add data/training_data.csv.dvc
git commit -m "Update training data: added 50k new examples from Q4"
dvc push

# Roll back to previous data version
git checkout HEAD~1 data/training_data.csv.dvc
dvc checkout
```

---

## Module 5.4 — Model Packaging and Serving

### FastAPI Model Server

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.sklearn
import pandas as pd
import numpy as np
import os
import time

app = FastAPI(title="Churn Prediction API", version="1.0.0")

# Load model at startup
MODEL_URI = os.getenv("MODEL_URI", "models:/churn_predictor/Production")
model = mlflow.sklearn.load_model(MODEL_URI)

class PredictionRequest(BaseModel):
    session_duration_s: float
    memory_mb: float
    crashes_last_week: int
    days_since_install: int
    daily_sessions: float

class PredictionResponse(BaseModel):
    user_id: str
    churn_probability: float
    churn_prediction: bool
    model_version: str
    inference_latency_ms: float

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest, user_id: str):
    start = time.time()
    
    features = pd.DataFrame([request.model_dump()])
    
    try:
        proba = model.predict_proba(features)[0][1]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    latency_ms = (time.time() - start) * 1000
    
    return PredictionResponse(
        user_id=user_id,
        churn_probability=round(float(proba), 4),
        churn_prediction=bool(proba > 0.5),
        model_version=os.getenv("MODEL_VERSION", "unknown"),
        inference_latency_ms=round(latency_ms, 2)
    )

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.get("/metrics")
async def metrics():
    # Expose Prometheus-compatible metrics
    return {"prediction_count": prediction_counter, "avg_latency_ms": avg_latency}
```

### Docker Containerization

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser /app
USER appuser

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]
```

```bash
# Build and run locally
docker build -t churn-model:v1.0.0 .
docker run -p 8080:8080 -e OPENAI_API_KEY=... churn-model:v1.0.0

# Test the containerized model
curl -X POST "http://localhost:8080/predict?user_id=user_123" \
     -H "Content-Type: application/json" \
     -d '{"session_duration_s": 120, "memory_mb": 280, "crashes_last_week": 2, "days_since_install": 45, "daily_sessions": 3.5}'
```

---

## Module 5.5 — CI/CD for ML

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Training & Deployment Pipeline

on:
  push:
    branches: [main]
    paths:
      - 'model/**'
      - 'data/**'
  schedule:
    - cron: '0 2 * * 0'  # Weekly retraining

jobs:
  data-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with: {python-version: '3.11'}
      - run: pip install -r requirements.txt
      - name: Validate data schema
        run: python scripts/validate_data.py
      - name: Check for data drift
        run: python scripts/check_drift.py --threshold 0.05

  train-and-evaluate:
    needs: data-validation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Train model
        run: python train.py --config config/prod.yaml
      - name: Evaluate model
        run: python evaluate.py --min-auc 0.82
      - name: Run unit tests on model
        run: pytest tests/test_model.py -v
      - name: Upload model artifact
        uses: actions/upload-artifact@v3
        with:
          name: model-artifact
          path: artifacts/model.pkl

  integration-tests:
    needs: train-and-evaluate
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker image
        run: docker build -t churn-model:${{ github.sha }} .
      - name: Run integration tests
        run: pytest tests/test_api.py --docker-image churn-model:${{ github.sha }}

  deploy-staging:
    needs: integration-tests
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: |
          docker push $ECR_REGISTRY/churn-model:${{ github.sha }}
          kubectl set image deployment/churn-model churn-model=$ECR_REGISTRY/churn-model:${{ github.sha }}
      - name: Run smoke tests
        run: python tests/smoke_test.py --env staging

  deploy-production:
    needs: deploy-staging
    environment: production
    runs-on: ubuntu-latest
    steps:
      - name: Blue-green deploy to production
        run: kubectl apply -f k8s/production-deploy.yaml
```

---

## Module 5.6 — Model Monitoring

**The most underestimated part of MLOps.** Models degrade in production as data distributions shift.

### Types of Drift

| Drift Type | What Changes | Example |
|-----------|-------------|---------|
| Data drift (covariate) | Input feature distributions | New device types → new memory patterns |
| Label drift (concept drift) | The relationship between X and Y changes | Economic shift changes what causes churn |
| Prediction drift | Output distribution changes | Model starts predicting churn much more |
| Business metric drift | KPIs degrade | Churn rate rises despite "good" model metrics |

```python
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.metrics import DatasetDriftMetric, ColumnDriftMetric
import pandas as pd

# Reference data: what the model was trained on
reference_data = pd.read_parquet("data/training_data.parquet")

# Current data: recent production data
current_data = pd.read_parquet("data/production_last_7days.parquet")

# Column mapping
column_mapping = ColumnMapping(
    target='churned',
    prediction='churn_prediction',
    numerical_features=['session_duration_s', 'memory_mb', 'daily_sessions'],
    categorical_features=['os_version', 'device_type']
)

# Generate drift report
report = Report(metrics=[
    DataDriftPreset(),
    TargetDriftPreset(),
    DatasetDriftMetric()
])

report.run(reference_data=reference_data, current_data=current_data,
           column_mapping=column_mapping)
report.save_html("drift_report.html")

# Programmatic check for alerts
results = report.as_dict()
drift_detected = results['metrics'][0]['result']['dataset_drift']
drift_share = results['metrics'][0]['result']['share_of_drifted_columns']

if drift_detected:
    print(f"ALERT: Data drift detected! {drift_share:.1%} of features drifted.")
    # Trigger retraining workflow
    # Send alert to Slack/PagerDuty
```

### Real-time Monitoring with Prometheus + Grafana

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Prometheus metrics
PREDICTION_COUNTER = Counter('model_predictions_total', 'Total predictions', ['model_version', 'result'])
PREDICTION_LATENCY = Histogram('model_prediction_latency_seconds', 'Prediction latency', buckets=[.01, .05, .1, .25, .5, 1.0])
PREDICTION_SCORE = Histogram('model_prediction_score', 'Distribution of prediction scores', buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
INPUT_DRIFT_GAUGE = Gauge('feature_drift_score', 'Feature drift score', ['feature_name'])

# Start metrics server on port 9090
start_http_server(9090)

def predict_with_monitoring(features: pd.DataFrame, model_version: str) -> float:
    with PREDICTION_LATENCY.time():
        proba = model.predict_proba(features)[0][1]
    
    result = "churn" if proba > 0.5 else "retain"
    PREDICTION_COUNTER.labels(model_version=model_version, result=result).inc()
    PREDICTION_SCORE.observe(proba)
    
    return proba
```

---

## Module 5.7 — Feature Store Concepts

A Feature Store is a centralized repository for computed features — avoiding redundant computation and ensuring training/serving consistency.

```python
# Conceptual architecture of a Feature Store

class SimpleFeatureStore:
    """Simplified feature store — production systems use Feast, Tecton, or Vertex AI Feature Store"""
    
    def __init__(self):
        self.offline_store = {}   # Historical features for training
        self.online_store = {}    # Low-latency features for serving
    
    def compute_user_features(self, user_id: str, as_of: datetime) -> dict:
        """
        Compute features for a user at a specific point in time.
        Critical: training and serving must use the EXACT same logic.
        """
        return {
            "sessions_last_7d": self._count_sessions(user_id, as_of, days=7),
            "sessions_last_30d": self._count_sessions(user_id, as_of, days=30),
            "avg_session_duration_7d": self._avg_duration(user_id, as_of, days=7),
            "crashes_last_7d": self._count_crashes(user_id, as_of, days=7),
            "days_since_last_open": self._days_inactive(user_id, as_of),
            "total_revenue_30d": self._sum_revenue(user_id, as_of, days=30)
        }
```

**Feature Store Benefits:**
- Training-serving skew prevention (same feature code for both)
- Feature reuse across models
- Point-in-time correctness for historical training data
- Low-latency serving (<10ms for online features)

---

## Module 5.8 — A/B Testing for AI Models

```python
import hashlib
import random

class ModelABRouter:
    """Route traffic between model versions for A/B testing"""
    
    def __init__(self, traffic_split: dict):
        # Example: {"model_v1": 0.7, "model_v2": 0.3}
        self.traffic_split = traffic_split
        self.models = {name: load_model(name) for name in traffic_split}
    
    def get_model_for_user(self, user_id: str) -> tuple[str, any]:
        """Deterministic assignment — same user always gets same model"""
        hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16) % 100
        
        cumulative = 0
        for model_name, split in self.traffic_split.items():
            cumulative += split * 100
            if hash_val < cumulative:
                return model_name, self.models[model_name]
        
        return list(self.traffic_split.keys())[-1], list(self.models.values())[-1]
    
    def predict(self, user_id: str, features: pd.DataFrame) -> dict:
        model_name, model = self.get_model_for_user(user_id)
        proba = model.predict_proba(features)[0][1]
        
        # Log which model made this prediction (for analysis)
        self._log_prediction(user_id, model_name, proba)
        
        return {"prediction": proba, "model_version": model_name}

# After running A/B test, use statistical tests to determine winner
from scipy import stats

def evaluate_ab_test(control_conversions, control_n, treatment_conversions, treatment_n):
    """Two-proportion z-test for A/B test evaluation"""
    control_rate = control_conversions / control_n
    treatment_rate = treatment_conversions / treatment_n
    
    _, p_value = stats.proportions_ztest(
        [control_conversions, treatment_conversions],
        [control_n, treatment_n]
    )
    
    lift = (treatment_rate - control_rate) / control_rate * 100
    
    print(f"Control: {control_rate:.3%}")
    print(f"Treatment: {treatment_rate:.3%}")
    print(f"Lift: {lift:+.1f}%")
    print(f"P-value: {p_value:.4f}")
    print(f"Statistically significant: {p_value < 0.05}")
```

---

## Phase 5 Capstone Project

**Project: End-to-End MLOps Pipeline for Churn Prediction**

Build a fully productionized version of your Phase 2 churn model with:

1. **DVC** for data versioning — commit your training data to DVC, push to S3/GCS
2. **MLflow** for experiment tracking — log all training runs with metrics and artifacts
3. **FastAPI** server — serve predictions via REST API with Pydantic validation
4. **Docker** container — package the server, run locally
5. **GitHub Actions** CI/CD — on push, automatically train, evaluate, and build Docker image
6. **Evidently** drift report — generate weekly HTML drift report comparing training vs recent data
7. **Prometheus metrics** — instrument prediction count, latency, and score distribution
8. **Model card** — document the model's purpose, training data, performance, limitations, and bias analysis

**Deliverable:** A GitHub repo where `git push` triggers an automated pipeline, and a README explaining every component of the system.

---

## Phase 5 Completion Checklist

- [ ] Understand the ML lifecycle beyond training — data versioning, serving, monitoring, retraining
- [ ] Set up MLflow experiment tracking on a real training run
- [ ] Built a FastAPI model server with health check and metrics endpoints
- [ ] Containerized the model server with Docker
- [ ] Written a CI/CD pipeline with GitHub Actions that trains and tests a model
- [ ] Generated a drift report using Evidently
- [ ] Implemented a basic A/B testing router
- [ ] Written a Model Card for a model you've built
- [ ] Completed the end-to-end MLOps pipeline capstone

**When all boxes are checked → move to [Phase 6](../phase-6-solution-architecture/README.md)**
