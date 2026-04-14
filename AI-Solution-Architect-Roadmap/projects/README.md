# Portfolio Projects Guide

> Six capstone projects — one per phase — that collectively prove your readiness as an Applied AI Solution Architect

---

## Why Projects Matter More Than Certificates

In AI roles, the first question in any interview is: "What have you built?"

Your portfolio of 6 projects demonstrates:
- Progression from fundamentals to system design
- Ability to apply AI to real mobile engineering problems
- End-to-end thinking (not just model training)
- Code quality and engineering discipline

---

## Project 1: Mobile App Crash Log Analyzer
**Phase:** 1 — Foundations  
**Tech:** Python, NumPy, Pandas, Matplotlib, Seaborn, SciPy

### What You Build
A Python data pipeline that ingests crash log data, performs EDA, and produces an interactive analysis report.

### Starter Code
See [`../phase-1-foundations/project-crash-analyzer.ipynb`](../phase-1-foundations/project-crash-analyzer.ipynb)

### Extension Ideas
- Add anomaly detection using z-scores (flag days with unusually high crash rates)
- Build a CLI tool: `python analyze.py --input crash_logs.csv --output report.html`
- Generate an automated weekly email report (use Python's `smtplib`)

### Portfolio Talking Points
- "I analyzed 5,000 simulated crash events and identified that version 2.3.0 had a 4x higher crash rate than adjacent versions"
- "I applied a two-sample t-test to determine if memory usage was statistically different at crash time"
- "I generated 8 visualizations including time-series crash rate trends and multi-dimensional device analysis"

---

## Project 2: User Churn Prediction System
**Phase:** 2 — Classical ML  
**Tech:** Pandas, Scikit-learn, XGBoost, SHAP, joblib, Optuna

### What You Build
An end-to-end ML pipeline predicting 30-day user churn, with full EDA, feature engineering, model comparison, and serialized model artifact.

### Dataset Options
- [Kaggle: Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- [Kaggle: Mobile App Usage](https://www.kaggle.com/datasets/meetnagadia/mobile-app-usage-data)
- Synthetically generate using `faker` + business rules

### Project Structure
```
churn-prediction/
├── data/
│   ├── raw/            # Original downloaded data
│   └── processed/      # Cleaned, feature-engineered data
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_model_evaluation.ipynb
├── src/
│   ├── features.py     # Feature engineering functions
│   ├── train.py        # Training script
│   └── predict.py      # Prediction function
├── models/
│   └── churn_pipeline.pkl
├── tests/
│   └── test_features.py
└── README.md
```

### Evaluation Criteria
- ROC-AUC ≥ 0.82 on held-out test set
- At least 10 engineered features
- SHAP waterfall plot for 3 example users
- Feature importance ranking documented

### Portfolio Talking Points
- "I compared 3 models and selected XGBoost based on AUC performance and inference speed"
- "I used SHAP values to explain individual predictions — critical for stakeholder trust"
- "I engineered 15 features from raw session data including rolling averages and time-since-event features"

---

## Project 3: Mobile UI Screenshot Classifier + App Review Sentiment
**Phase:** 3 — Deep Learning  
**Tech:** PyTorch, torchvision, Hugging Face Transformers, FastAPI

### Part A: Screenshot Classifier

**Dataset:** Collect/label 50–100 screenshots per class across 5 categories:
- `login_screen`
- `home_feed`
- `checkout`
- `error_state`
- `settings`

Or use a public UI dataset: [Rico Dataset](http://interactionmining.org/rico)

**Model:** MobileNetV3-Large with custom head (transfer learning)

**Target:** >85% validation accuracy

**Outputs:**
- Trained `.pth` model file
- CoreML `.mlpackage` (iOS)
- TFLite `.tflite` (Android)
- FastAPI endpoint: `POST /classify` with image upload

### Part B: App Review Sentiment

**Dataset:** [Google Play Store Reviews](https://www.kaggle.com/datasets/lava18/google-play-store-apps)

**Model:** Fine-tune `distilbert-base-uncased` for 5-class rating prediction

**Endpoint:** `POST /analyze-review` → `{"predicted_stars": 4, "confidence": 0.89, "sentiment_class": "positive"}`

**Evaluation:** Compare DistilBERT accuracy vs Logistic Regression from Phase 2

### Portfolio Talking Points
- "I fine-tuned MobileNetV3 achieving 87% accuracy with only 400 training images — demonstrating transfer learning efficiency"
- "I exported the model to CoreML format for on-device iOS inference, achieving <30ms latency"
- "I compared DistilBERT (91% accuracy) vs Logistic Regression on TF-IDF (78%) for sentiment classification"

---

## Project 4: RAG Chatbot over Mobile SDK Documentation
**Phase:** 4 — Applied AI / GenAI  
**Tech:** OpenAI API, LlamaIndex, ChromaDB, FastAPI, Streamlit/Gradio

### What You Build
A production-quality Q&A chatbot over mobile SDK documentation with semantic search, source citations, and feedback collection.

### Documentation Sources (Pick one)
- [React Native Docs](https://reactnative.dev/docs/getting-started)
- [Flutter Documentation](https://docs.flutter.dev/)
- [Firebase Documentation](https://firebase.google.com/docs)
- Your own company's internal SDK docs (even better for portfolio)

### System Architecture
```
User Input
    ↓
Safety Check (block prompt injection)
    ↓
Query Expansion (LLM generates 3 search variations)
    ↓
Embedding + Vector Search (ChromaDB)
    ↓
Reranking (cross-encoder for precision)
    ↓
Context Injection into Prompt
    ↓
GPT-4o Response Generation
    ↓
Source Citation Extraction
    ↓
Response + Sources → User
```

### Evaluation Framework
Run 25 test questions and grade each response:
- **Answer quality** (1-5): Is it correct and helpful?
- **Groundedness** (1-5): Is it based on the retrieved context?
- **Completeness** (1-5): Does it answer the full question?

Target: Average score ≥ 4.0/5.0

### Portfolio Talking Points
- "I built a RAG system achieving 4.2/5.0 average quality on 25 eval questions"
- "I implemented query expansion — generating 3 semantic variations to improve retrieval recall by 18%"
- "I measured retrieval vs generation quality separately to identify that reranking improved precision from 0.71 to 0.89"

---

## Project 5: End-to-End MLOps Pipeline
**Phase:** 5 — MLOps  
**Tech:** MLflow, DVC, FastAPI, Docker, GitHub Actions, Evidently, Prometheus

### What You Build
Take your Phase 2 churn model and productionize it with full MLOps infrastructure.

### Infrastructure Components

```
GitHub Repository (source + DVC pointers)
    ↓
GitHub Actions CI/CD
    ├── data-validation job (schema check, drift check)
    ├── training job (MLflow logging)
    ├── evaluation job (minimum AUC threshold)
    └── build-and-push Docker image
    ↓
Docker Image (model server)
    ↓
Model Serving (FastAPI on port 8080)
    ├── POST /predict
    ├── GET /health
    └── GET /metrics (Prometheus format)
    ↓
Monitoring
    ├── Weekly drift report (Evidently HTML)
    └── Prometheus + Grafana dashboard
```

### Deliverables
1. `README.md` — full architecture walkthrough
2. GitHub Actions workflow that runs on `git push`
3. MLflow experiment dashboard (screenshot)
4. FastAPI server with Swagger docs (`/docs`)
5. Docker image runnable with single `docker run` command
6. Evidently drift report HTML
7. Model card (PDF or Markdown)

### Portfolio Talking Points
- "I built a CI/CD pipeline that automatically retrains, evaluates, and deploys a new model when data is updated"
- "I implemented Evidently drift monitoring that alerts when >20% of features drift from training distribution"
- "My model card documents training data characteristics, performance metrics, known limitations, and fairness analysis"

---

## Project 6: AI Architecture Design — AI-Powered Mobile Super-App
**Phase:** 6 — Solution Architecture  
**Tech:** Excalidraw/Lucidchart, Markdown, Python (for cost estimation)

### What You Build
A comprehensive architecture design document for a fictional but realistic AI-powered mobile super-app.

### Super-App Features to Architect

**Feature 1: Personalized Content Feed**
- Collaborative filtering model for item recommendations
- Real-time feature serving (user context + item features)
- A/B testing framework for ranking algorithms

**Feature 2: AI Customer Support**
- RAG chatbot with domain-specific documentation
- Confidence scoring + human escalation at threshold <0.7
- Feedback loop for continuous improvement

**Feature 3: Intelligent Search**
- Hybrid search: keyword (BM25) + semantic (embeddings)
- Query intent classification (navigational vs informational vs transactional)
- Spelling correction and query expansion

**Feature 4: Real-time Fraud Detection**
- XGBoost model scoring each transaction in <50ms
- Feature engineering from transaction history + device signals
- Model drift monitoring and weekly retraining

**Feature 5: On-Device Capabilities**
- Document scanner (OCR with CoreML/TFLite)
- Live object recognition (MobileNetV3)
- Smart keyboard suggestions (small language model, <30MB)

**Feature 6: AI Analytics for Business Users**
- Weekly LLM-generated insights from telemetry data
- Natural language querying of metrics ("What caused the DAU drop on Tuesday?")

### Document Structure
```
1. Executive Summary (1 page)
2. Business Context and AI Use Cases
3. System Context Diagram (C4 L1)
4. Container Diagram (C4 L2)
5. Feature-by-Feature Deep Dives
   ├── Architecture decision for each feature
   ├── Model selection justification
   └── Data flow diagram
6. Cross-Cutting Concerns
   ├── Data platform and feature store
   ├── MLOps and model lifecycle
   ├── Monitoring and observability
   └── Cost architecture
7. Governance and Risk
   ├── Responsible AI checklist
   ├── Privacy and compliance
   └── Risk register
8. Roadmap and Prioritization
9. Architecture Decision Records (3 ADRs)
10. Cost Estimate
```

### Presentation
Record a 10-minute Loom video walking through the architecture. This is your CTO pitch.

### Portfolio Talking Points
- "I designed an AI architecture spanning 6 distinct ML use cases with a consistent data platform underneath"
- "I wrote ADRs justifying why we chose RAG over fine-tuning for the support chatbot, saving $500K/year in retraining costs"
- "My governance framework includes bias testing across 4 user demographic groups and a GDPR-compliant data deletion process"

---

## Publishing Your Portfolio

### GitHub Repository Structure
```
your-github-username/
├── ai-portfolio-README.md       # Master portfolio landing page
├── 01-crash-log-analyzer/
├── 02-churn-prediction/
├── 03-mobile-ai-models/
├── 04-rag-sdk-chatbot/
├── 05-mlops-pipeline/
└── 06-superapp-architecture/
```

### Portfolio Landing Page Template

```markdown
# [Your Name] — Applied AI Solution Architect Portfolio

Principal Engineer (10+ yrs mobile) → Applied AI Solution Architect

## Projects

| # | Project | Tech | Key Achievement |
|---|---------|------|-----------------|
| 1 | Crash Log Analyzer | Python, Pandas | Identified v2.3.0 4x crash rate anomaly |
| 2 | Churn Prediction | XGBoost, SHAP | AUC 0.89, 15 engineered features |
| 3 | Mobile Vision + NLP | PyTorch, BERT | 87% CV accuracy, CoreML export |
| 4 | RAG SDK Chatbot | LlamaIndex, GPT-4o | 4.2/5.0 eval score, live demo |
| 5 | MLOps Pipeline | MLflow, Docker, GHA | Full CI/CD with drift monitoring |
| 6 | AI Super-App Architecture | Design Doc | 6 AI features, ADRs, cost model |

## Unique Value
Mobile engineering + AI: the intersection that most architects don't cover.
```

### Where to Share
- LinkedIn (post case studies for each project)
- GitHub (public repos with good READMEs)
- Medium/Substack (write technical posts about what you learned)
- Local AI/ML meetups (5-minute lightning talks on your projects)
- DEV Community, Towards Data Science

---

## Interview Preparation

### Common Applied AI Architect Interview Questions

**Technical:**
1. "Walk me through how you would build a RAG system for our internal knowledge base"
2. "How would you detect if a deployed model is degrading?"
3. "When would you choose fine-tuning over RAG?"
4. "How do you handle hallucinations in production LLM systems?"
5. "Design a real-time fraud detection system for a mobile payments app"

**Architecture:**
6. "What's your approach to model versioning and rollback?"
7. "How would you A/B test two recommendation models fairly?"
8. "What are the trade-offs of on-device vs cloud AI for a mobile app?"
9. "How do you estimate and control LLM costs at scale?"
10. "What's in a good Model Card and why does it matter?"

**Leadership / Communication:**
11. "How do you explain AI limitations to non-technical stakeholders?"
12. "How do you prioritize which AI features to build first?"
13. "How do you build trust in AI systems with end users?"

### Your Unique Answers Leverage
Always connect answers back to your mobile background:
- "Having worked on mobile for 10 years, I understand that latency and battery life are first-class constraints, which changes how I think about on-device vs cloud model placement..."
- "From mobile, I'm used to shipping to millions of devices where a bad update can't be easily rolled back — that same discipline applies to model deployment..."
- "My experience with mobile app instrumentation means I think about telemetry design for AI systems earlier than most — you can't monitor what you haven't measured..."
