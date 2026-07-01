# AI Firewall IDS
# 🛡️ AI Firewall IDS

A Machine Learning powered Intrusion Detection System built using FastAPI, Streamlit, CatBoost, and SHAP explainability.

The project focuses on accurate detection and classification of network intrusions using a two stage machine learning pipeline while maintaining interpretability and deployment readiness.

---

# Table of Contents

- Overview
- Motivation
- Architecture
- Features
- Supported Attacks
- Technology Stack
- Design Decisions
- Why CatBoost?
- Why a Two Stage Pipeline?
- Why SHAP?
- Why Not Deep Learning?
- Project Structure
- Running the API
- Running the Dashboard
- API Endpoints
- Model Pipeline
- Explainability
- Current Limitations
- Future Roadmap
- Dataset
- License

---

# Overview

AI Firewall IDS is an intrusion detection system designed to classify malicious network traffic using supervised machine learning models trained on the CIC IDS 2017 dataset.

The system currently supports:

- Single flow prediction
- Batch CSV analysis
- SHAP based explainability
- FastAPI inference services
- Interactive Streamlit dashboards

The long term vision is to evolve into a fully product ready AI powered firewall solution with:

- PostgreSQL persistence
- Authentication
- Docker deployment
- Continuous learning
- Live monitoring
- Unknown threat detection
- CI/CD pipelines

---

# Motivation

Traditional signature based systems struggle to detect modern attack patterns and require constant manual rule updates.

This project aims to combine:

- High accuracy supervised learning
- Explainable AI
- Practical deployment
- Human guided continuous improvement

to build a trustworthy and extensible intrusion detection platform.

---

# Current Architecture

```text
                    Network Flow
                           │
                           ▼
                Feature Engineering
                 (78 CICIDS Features)
                           │
                           ▼
         ┌────────────────────────────────┐
         │ Binary CatBoost Classifier     │
         │ BENIGN vs MALICIOUS            │
         └────────────────────────────────┘
                           │
                   ┌───────┴───────┐
                   │               │
                   ▼               ▼
               BENIGN         MALICIOUS
                                   │
                                   ▼
         ┌────────────────────────────────┐
         │ Multiclass CatBoost Model      │
         │                                │
         │ DDoS                           │
         │ DoS                            │
         │ PortScan                       │
         │ Bot                            │
         │ BruteForce                     │
         │ WebAttack                      │
         │ Heartbleed                     │
         │ Infiltration                   │
         └────────────────────────────────┘
                                   │
                                   ▼
                         SHAP Explainability
                                   │
                                   ▼
                          FastAPI REST API
                                   │
                                   ▼
                        Streamlit Dashboard
```

---

# Features

## Backend

- FastAPI based inference API
- Pydantic request validation
- Health monitoring endpoints
- Batch prediction support
- Demo attack endpoints

## Machine Learning

- Binary CatBoost intrusion detector
- Multiclass CatBoost attack classifier
- Feature importance analysis
- Confusion matrices
- Detection rate evaluation

## Dashboard

### Single Flow Prediction

Upload a single network flow and obtain:

- Attack prediction
- Confidence score
- Color coded threat indicators

### Batch CSV Analysis

Analyze large collections of flows:

- Attack distribution charts
- Summary statistics
- Downloadable predictions
- Interactive visualizations

### SHAP Explainability

Understand why the model produced a prediction:

- Top contributing features
- SHAP importance plots
- Confidence metrics
- Human interpretable explanations

---

# Supported Attacks

| Attack Type | Supported |
|-------------|------------|
| DDoS | ✅ |
| DoS | ✅ |
| PortScan | ✅ |
| Bot | ✅ |
| BruteForce | ✅ |
| WebAttack | ✅ |
| Heartbleed | ✅ |
| Infiltration | ✅ |

---

# Technology Stack

| Layer | Technology |
|--------|-------------|
| Backend | FastAPI |
| Dashboard | Streamlit |
| ML Models | CatBoost |
| Explainability | SHAP |
| Visualization | Plotly |
| Data Processing | Pandas |
| Numerical Computing | NumPy |
| API Validation | Pydantic |
| Model Serialization | CatBoost CBM |

---

# Design Decisions

---

## Why CIC IDS 2017?

The CIC IDS 2017 dataset was chosen because it provides:

- Realistic modern attack scenarios
- Multiple attack categories
- Flow based features
- Academic credibility
- Standard benchmarking capabilities

Alternative datasets considered:

### UNSW NB15

Pros:

- Newer dataset
- Rich feature space

Cons:

- Less adoption in academic IDS research

### KDD99

Pros:

- Historical importance

Cons:

- Outdated attack patterns
- Unrealistic modern relevance

Decision:

✅ CIC IDS 2017

---

# Why CatBoost?

CatBoost was selected after evaluating:

- Random Forest
- XGBoost
- LightGBM
- Neural Networks

Reasons:

### Advantages

- Excellent performance on tabular data
- Minimal preprocessing requirements
- Strong generalization
- Robust against overfitting
- Fast inference
- Native feature importance support

---

## Why Not XGBoost?

Although extremely powerful:

- Requires more tuning
- Sensitive preprocessing
- Larger engineering overhead

---

## Why Not LightGBM?

While fast:

- More prone to overfitting
- Less stable on smaller security datasets

---

## Why Not Deep Learning?

Deep learning was intentionally avoided.

Reasons:

### LSTMs

Problems:

- Require significantly larger datasets
- Harder interpretability
- Slower deployment

### Transformers

Problems:

- Computationally expensive
- Excessive complexity for structured network flows

### Autoencoders

Problems:

- Better suited for anomaly detection
- Poor multiclass classification capabilities

Decision:

✅ CatBoost offered the best balance between:

- Accuracy
- Explainability
- Maintainability
- Deployment simplicity

---

# Why a Two Stage Pipeline?

Instead of training a single multiclass model:

```text
Traffic
↓
DDoS
DoS
Bot
BENIGN
...
```

the project uses:

```text
Traffic
↓
Binary Detection
↓
Multiclass Classification
```

Advantages:

- Reduced false positives
- Better class separation
- Faster inference
- Improved maintainability
- Easier debugging

This mirrors industrial IDS architectures where malicious detection is separated from attack attribution.

---

# Why SHAP?

Explainability is critical in cybersecurity.

Instead of relying on LLM generated explanations:

```text
Prediction
↓
Language Model
↓
Generated Explanation
```

the project uses SHAP.

Advantages:

- Mathematically grounded
- Reproducible
- Offline operation
- No cloud dependencies
- No hallucinations
- Strong academic support

This enables analysts to understand:

- Which features contributed most
- Why a prediction was made
- How confident the model is

---

# Project Structure

```text
AI-Firewall-Attack-Detection/

api/
├── app.py
├── inference.py
├── schemas.py
├── requirements.txt

dashboard/
├── app.py
└── pages/
    ├── 1_Single_Prediction.py
    ├── 2_Batch_Analysis.py
    └── 3_SHAP_Explainability.py

models/
├── anomaly/
├── autoencoder/
├── autogluon/
└── catboost/
    ├── firewall_binary_ids_catboost.cbm
    ├── firewall_multiclass_catboost.cbm
    └── features.json

scripts/
├── preprocessing/
├── training/
├── evaluation/
└── inspection/

docs/

README.md
.gitignore
Dockerfile
docker-compose.yml
```

---

# Running the API

```bash
python -m uvicorn api.app:app --reload
```

API:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

# Running the Dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard:

```text
http://localhost:8501
```

---

# API Endpoints

## Health Check

```text
GET /health
```

---

## Model Information

```text
GET /model-info
```

---

## Single Prediction

```text
POST /predict
```

---

## Batch Prediction

```text
POST /batch-predict
```

---

## Demo Attacks

```text
GET /demo/ddos

GET /demo/portscan

GET /demo/bot
```

---

# Model Pipeline

## Stage 1

Binary CatBoost:

```text
BENIGN
vs
MALICIOUS
```

---

## Stage 2

Multiclass CatBoost:

```text
DDoS
DoS
PortScan
Bot
BruteForce
Heartbleed
WebAttack
Infiltration
```

---

# Explainability

The project uses SHAP to generate:

- Feature importance rankings
- Local explanations
- Prediction reasoning
- Confidence interpretation

This allows analysts to understand not only what the model predicts, but why it predicts it.

---

# Current Limitations

Current version limitations include:

- No authentication
- No PostgreSQL persistence
- No Docker deployment in production
- No continuous learning pipeline
- No live packet capture
- No unknown threat detection
- No CI/CD workflows

These features are planned for future releases.

---

# Future Roadmap

## Version 1.1

- PostgreSQL integration
- Logging infrastructure
- Authentication
- Prediction history
- User management

---

## Version 1.2

- Isolation Forest integration
- Unknown threat detection
- Human feedback system
- Model versioning
- Champion challenger evaluation

---

## Version 2.0

- Docker deployment
- CI/CD pipelines
- React dashboard
- Live monitoring
- Real packet capture
- Prometheus metrics
- Grafana dashboards

---

# Dataset

This project uses:

**CIC IDS 2017**

The dataset includes:

- 2.8 million network flows
- Modern attack scenarios
- Flow based features
- Realistic enterprise traffic patterns

---

# License

MIT License

---

# Author

Shaurya Handu

BTech Computer Science Engineering

Machine Learning and Cybersecurity Enthusiast
