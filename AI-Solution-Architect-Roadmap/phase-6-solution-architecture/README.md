# Phase 6: AI Solution Architecture

> **Duration:** 8–12 weeks (ongoing practice)  
> **Prerequisite:** Phases 1–5 complete  
> **Goal:** Design, document, and defend end-to-end AI system architectures for real business problems

---

## What Makes an Applied AI Solution Architect

You are not primarily a model trainer — that's a Data Scientist. You are not primarily an ML infrastructure engineer — that's an MLOps Engineer. 

You are the person who:

1. **Understands the business problem** deeply enough to identify where AI helps (and where it doesn't)
2. **Designs the full system** — data pipelines, models, serving, monitoring, UX, governance
3. **Communicates across layers** — speaks to executives about ROI, to engineers about architecture, to data scientists about model selection
4. **Makes build vs. buy vs. fine-tune decisions** for every AI component
5. **Owns the non-functional requirements** — latency, cost, reliability, privacy, compliance, fairness
6. **Anticipates failure modes** — hallucinations, model drift, data quality issues, adversarial inputs

---

## Module 6.1 — AI Architecture Patterns

### Pattern 1: Direct API Call (Simplest)

```
User → Your App → LLM API → Response
```

**When to use:** Simple text tasks, internal tools, prototypes  
**Limitations:** No private data, no memory, cost per call, latency

### Pattern 2: RAG (Retrieval-Augmented Generation)

```
User Query → Embedding → Vector DB → Retrieved Context + Query → LLM → Response
```

**When to use:** Q&A over private docs, knowledge bases, customer support  
**Limitations:** Retrieval quality depends on chunking and embedding; complex queries may not find the right context

### Pattern 3: Fine-tuned Model

```
Your Data → Fine-tune Base Model → Serve Fine-tuned Model
```

**When to use:** Consistent output format, domain-specific vocabulary, tone/style control, cost reduction at scale  
**Limitations:** Training cost, data requirements, harder to update

### Pattern 4: Agent with Tools

```
User → Agent (LLM + Planning) → Tool Calls → Results → Synthesis → Response
```

**When to use:** Multi-step tasks, requires real-time data, needs to take actions  
**Limitations:** Reliability — agents can loop, hallucinate tool calls, fail unpredictably

### Pattern 5: Multi-Agent System

```
Orchestrator Agent
├── Research Agent (web search, RAG)
├── Analysis Agent (code execution, data)
├── Writing Agent (drafting)
└── Review Agent (fact-checking)
```

**When to use:** Complex workflows requiring specialization, parallel processing  
**Limitations:** Complexity, debugging difficulty, compounding errors

### Pattern 6: Hybrid Classical + LLM

```
Tabular Data → XGBoost → Risk Score
                                  ↘
                                    LLM → Human-readable explanation
                                  ↗
User Context → Embedding → Vector → 
```

**When to use:** Regulated industries (explanation required), high-volume low-cost path + LLM fallback, confidence thresholds

---

## Module 6.2 — The Architecture Decision Framework

For every AI system component, ask these questions:

### Build vs. Buy vs. Fine-tune vs. RAG vs. Prompt

| Approach | When | Cost | Time |
|----------|------|------|------|
| Zero-shot prompting | Generic task, small volume | Lowest | Fastest |
| Few-shot prompting | Specific format needed | Low | Fast |
| RAG | Private knowledge base | Medium | 2-4 weeks |
| Fine-tuning | Consistent style/format, high volume | Medium | 4-8 weeks |
| Train from scratch | Unique domain, massive data | Highest | Months |
| Buy API | Fast to market, no ML team | Per-call cost | Fastest |
| Open-source model (self-hosted) | Data privacy, cost at scale | Infra cost | 2-6 weeks |

### Model Selection Decision Tree

```
Is data privacy required?
├── YES → Use open-source (Llama, Mistral, Phi) on your infra
└── NO  → Can you use an API?
           ├── YES → Is accuracy critical?
           │         ├── YES → GPT-4o / Claude 3.5 Sonnet
           │         └── NO  → GPT-4o-mini / Claude Haiku (10x cheaper)
           └── NO  → Fine-tune an open-source model
```

### Latency Requirements

| Latency Budget | Architecture |
|---------------|-------------|
| <100ms | On-device model (TFLite/CoreML) |
| 100-500ms | Cached inference, small model |
| 500ms-2s | Standard API call, streaming |
| 2-10s | Complex reasoning, agent with 1-2 tool calls |
| >10s | Multi-step agent, fine-grained analysis |

---

## Module 6.3 — Designing AI Systems for Mobile

This is your unique advantage. You understand the mobile context that most AI architects don't.

### Mobile AI Architecture Stack

```
┌─────────────────────────────────────────┐
│           Mobile App (iOS/Android)       │
│                                         │
│  ┌─────────────┐    ┌─────────────────┐ │
│  │  On-Device  │    │  Cloud AI Layer  │ │
│  │  AI Engine  │    │  (via REST API)  │ │
│  │ (CoreML/    │    │                 │ │
│  │  TFLite)    │    │  LLM / ML APIs  │ │
│  └─────────────┘    └─────────────────┘ │
│         ↕                   ↕           │
│  ┌──────────────────────────────────┐   │
│  │       Intelligence Router         │   │
│  │  - On-device if offline/fast     │   │
│  │  - Cloud if complex/connected    │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
              ↕
┌─────────────────────────────────────────┐
│         Backend AI Services              │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │  Feature  │ │  Model   │ │  RAG    │ │
│  │  Store   │ │ Serving  │ │ Service │ │
│  └──────────┘ └──────────┘ └─────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ Telemetry │ │  A/B    │ │ Drift   │ │
│  │ Pipeline │ │  Router  │ │Monitor  │ │
│  └──────────┘ └──────────┘ └─────────┘ │
└─────────────────────────────────────────┘
```

### Mobile AI Use Case Matrix

| Use Case | On-Device? | Model Type | Key Consideration |
|----------|-----------|------------|-------------------|
| Face unlock | Yes | MobileFaceNet | Privacy, <100ms |
| Live caption | Yes | Whisper tiny | Latency, battery |
| Photo categorization | Yes | MobileNetV3 | Storage (<50MB) |
| Smart reply suggestions | Hybrid | Small LLM + rules | Latency vs quality |
| Search | Cloud | Embedding + LLM | Context window |
| Customer support chat | Cloud | RAG + LLM | Accuracy, grounding |
| Personalization | Cloud | Collaborative filtering | Privacy, freshness |
| Crash prediction | Cloud (background) | XGBoost | Batch, non-real-time |

---

## Module 6.4 — AI Governance, Ethics, and Compliance

This is what separates a junior practitioner from a senior architect.

### Responsible AI Checklist

**Fairness:**
- [ ] Has the model been evaluated for performance across demographic groups (age, gender, geography)?
- [ ] Is there training data bias that could be amplified?
- [ ] What is the impact of false positives vs false negatives on different user groups?

**Transparency:**
- [ ] Can the model explain its decisions? (SHAP, LIME, LLM reasoning)
- [ ] Is there a model card documenting training data, performance, and limitations?
- [ ] Do users know when they're interacting with AI?

**Privacy:**
- [ ] Does the model training use PII? Is it anonymized?
- [ ] Are API calls sending user data to third parties?
- [ ] GDPR/CCPA compliance for data used in training
- [ ] Right to be forgotten — can we retrain without a user's data?

**Security:**
- [ ] Is the model protected against prompt injection attacks?
- [ ] Are outputs validated before being shown to users or used in decisions?
- [ ] Is the model API rate-limited and authenticated?
- [ ] Can the model be used to generate harmful content?

**Reliability:**
- [ ] What happens when the model is unavailable? (fallback plan)
- [ ] What happens when the model is confidently wrong?
- [ ] Is there a human-in-the-loop for high-stakes decisions?

### AI Risk Matrix

```
                    HIGH STAKES
                         │
    Explainable          │         Human Review
    required             │         required
    (Regulatory)         │         (High impact)
                         │
────────────────────────────────────────── VISIBILITY
    Fully automated      │         A/B test +
    acceptable           │         Monitoring
    (Low stakes)         │         required
                         │
                    LOW STAKES
```

---

## Module 6.5 — AI Cost Architecture

Understanding AI economics is a core architect skill.

### LLM Cost Estimation

```python
def estimate_llm_costs(
    daily_requests: int,
    avg_input_tokens: int,
    avg_output_tokens: int,
    model: str = "gpt-4o"
) -> dict:
    
    pricing = {
        "gpt-4o":          {"input": 2.50/1_000_000,  "output": 10.00/1_000_000},
        "gpt-4o-mini":     {"input": 0.15/1_000_000,  "output": 0.60/1_000_000},
        "claude-3.5-sonnet":{"input": 3.00/1_000_000,  "output": 15.00/1_000_000},
        "claude-3-haiku":   {"input": 0.25/1_000_000,  "output": 1.25/1_000_000},
    }
    
    p = pricing[model]
    daily_cost = (
        daily_requests * avg_input_tokens * p["input"] +
        daily_requests * avg_output_tokens * p["output"]
    )
    
    return {
        "daily_cost_usd": daily_cost,
        "monthly_cost_usd": daily_cost * 30,
        "annual_cost_usd": daily_cost * 365,
        "cost_per_request_usd": daily_cost / daily_requests
    }

# Example: Customer support chatbot
costs = estimate_llm_costs(
    daily_requests=10_000,
    avg_input_tokens=500,    # System prompt + history + user message
    avg_output_tokens=300,   # Response
    model="gpt-4o"
)
print(f"Monthly cost (GPT-4o): ${costs['monthly_cost_usd']:,.0f}")

costs_mini = estimate_llm_costs(10_000, 500, 300, "gpt-4o-mini")
print(f"Monthly cost (GPT-4o-mini): ${costs_mini['monthly_cost_usd']:,.0f}")
print(f"Savings: {(1 - costs_mini['monthly_cost_usd']/costs['monthly_cost_usd'])*100:.0f}%")
```

### Total Cost of AI Ownership

| Cost Category | Components |
|--------------|-----------|
| **Model costs** | API calls, GPU instances for self-hosted, fine-tuning runs |
| **Infrastructure** | Vector DB hosting, model serving, caching layer |
| **Data costs** | Storage, processing pipelines, labeling |
| **People** | ML engineers, data scientists, AI architects |
| **Monitoring** | Observability tools, alerting |
| **Compliance** | Auditing, explainability tools, legal review |
| **Failure cost** | Model errors → customer impact → churn |

---

## Module 6.6 — Architecture Documentation

Architects communicate through documentation. Master these formats.

### C4 Model for AI Systems

**Level 1 — System Context:**
```
[Mobile User] → interacts with → [Smart App]
[Smart App] → uses → [AI Platform]
[AI Platform] → reads from → [Company Data Warehouse]
```

**Level 2 — Container Diagram:**
```
[AI Platform]
├── RAG Service (FastAPI + ChromaDB)
├── ML Model Server (FastAPI + MLflow)
├── LLM Gateway (Rate limiting, caching, routing)
├── Feature Store (Feast)
└── Monitoring Service (Evidently + Prometheus)
```

**Level 3 — Component Diagram:**
```
[RAG Service]
├── Query Processor (tokenization, safety check)
├── Retriever (embedding → vector search → reranker)
├── Prompt Builder (context injection, system prompt)
└── Response Validator (hallucination check, length)
```

### Architecture Decision Records (ADRs)

```markdown
# ADR-001: Use RAG Over Fine-tuning for SDK Documentation Bot

**Status:** Accepted  
**Date:** 2025-03-15  
**Deciders:** Engineering Lead, AI Architect, Product Manager

## Context
We need our mobile SDK chatbot to answer questions about our documentation, 
which is updated every 2 weeks with new releases.

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| Fine-tuning | Fast inference, no retrieval latency | Requires retraining every 2 weeks ($500/run), stale between releases |
| RAG | Always current, explainable sources, no training cost | Retrieval latency (+200ms), depends on chunking quality |
| Prompt stuffing | Simple | Context window limits, expensive, slow |

## Decision
Use RAG with a weekly re-indexing job.

## Consequences
- +200ms latency per response (acceptable per requirement of <2s)
- Need to maintain ChromaDB infrastructure
- Must implement chunking + embedding pipeline
- Users get source citations (positive)
- No retraining needed when docs update (positive)

## Metrics for Review
Re-evaluate if answer quality score drops below 7.5/10 in monthly eval.
```

---

## Module 6.7 — Stakeholder Communication

A brilliant architecture that you can't communicate is worth nothing.

### For Engineering Teams

- Use sequence diagrams for request flows
- Use component diagrams for service dependencies
- Specify contracts: API schemas, latency SLAs, error handling
- Write runbooks for operational procedures

### For Product Teams

- Map AI features to user outcomes: "This reduces support ticket volume by X%"
- Be honest about AI limitations: "The model is 85% accurate — in 15% of cases it will give a wrong answer"
- Set expectations on timelines: "RAG prototype in 2 weeks, production-ready in 6 weeks"

### For Executive Stakeholders

Build a one-page AI Business Case:

```
OPPORTUNITY:    Customer support team handles 50,000 tickets/month
                Average cost per ticket: $12
                Total monthly cost: $600,000

AI SOLUTION:    LLM-powered support assistant
                Expected deflection rate: 40%
                Projected savings: $240,000/month

INVESTMENT:     Build cost: $150,000 (12 weeks, 2 engineers)
                Monthly operating cost: $8,000 (LLM API + infra)
                Annual operating cost: $96,000

ROI:            Annual savings: $2.88M
                Annual cost: $246,000
                Net annual benefit: $2.63M
                Payback period: 0.8 months after launch

RISKS:          Model accuracy may disappoint users (mitigation: human escalation)
                LLM API dependency (mitigation: multi-vendor, fallback)
                Data privacy (mitigation: no PII in prompts, vendor DPA)
```

---

## Module 6.8 — Certifications and Credentials

To formalize your AI architecture expertise:

| Certification | Provider | Focus | Effort |
|--------------|---------|-------|--------|
| AWS Certified Machine Learning — Specialty | AWS | Cloud ML on AWS | 3-4 months |
| Google Professional Machine Learning Engineer | Google | ML on GCP | 3-4 months |
| Azure AI Engineer Associate (AI-102) | Microsoft | Azure AI services | 2-3 months |
| Databricks Certified ML Professional | Databricks | MLOps, feature engineering | 2-3 months |
| Certified AI Practitioner (CAIP) | IAPP | AI governance | 1-2 months |
| DeepLearning.AI specializations | Coursera | Technical foundations | Ongoing |

**Recommended path for you:**
1. AWS Solutions Architect Associate (leverage existing engineering)
2. AWS Certified Machine Learning Specialty
3. DeepLearning.AI MLOps Specialization
4. Build portfolio projects (more valuable than any cert)

---

## Phase 6 Capstone Project

**Project: AI Architecture Design for an AI-Powered Mobile Super-App**

Design (document, diagram, justify — no need to fully build) a complete AI architecture for a fictional mobile super-app with these AI features:

1. **Personalized feed** — ML-based content ranking
2. **AI customer support** — RAG chatbot with human escalation
3. **Smart search** — Semantic search + intent detection
4. **Fraud detection** — Real-time transaction risk scoring
5. **On-device capabilities** — Offline image recognition, smart keyboard suggestions
6. **Analytics dashboard** — AI-generated weekly insights for business users

**Deliverables:**
1. System Context Diagram (C4 Level 1)
2. Container Diagram (C4 Level 2)  
3. Data flow diagrams for each AI feature
4. Model selection justification table (build vs buy vs fine-tune for each)
5. Cost estimate (monthly LLM costs, infrastructure)
6. Governance checklist (fairness, privacy, explainability)
7. 3 ADRs for the most critical architectural decisions
8. Executive one-pager (business case + risks)
9. 10-minute recorded walkthrough (present this like you would to a CTO)

---

## Your Positioning Statement (Write This Once You're Done)

Fill this in when you complete Phase 6:

> "I'm a Principal Engineer with 10+ years of mobile engineering experience, now specializing as an Applied AI Solution Architect. I design and deliver AI-powered systems — from on-device inference pipelines to cloud-scale LLM applications — with deep expertise in mobile AI integration, RAG architectures, and MLOps. I've built [Project 1], [Project 2], [Project 3], and I hold [Certification]."

---

## Phase 6 Completion Checklist

- [ ] Understand and can explain all major AI architecture patterns (RAG, agents, fine-tuning, hybrid)
- [ ] Can make and document build vs buy vs fine-tune decisions with business justification
- [ ] Have designed a mobile AI architecture with on-device and cloud components
- [ ] Have written at least 3 ADRs for real architectural decisions
- [ ] Can estimate AI system costs and build a business case
- [ ] Have applied the AI governance checklist to a real or fictional system
- [ ] Can present an architecture diagram to both technical and non-technical audiences
- [ ] Completed the super-app architecture capstone project
- [ ] Completed at least one certification
- [ ] Have a portfolio of 6 projects (one per phase) on GitHub

**Congratulations — you are now an Applied AI Solution Architect.**
