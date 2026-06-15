# 📊 Tiki Sentiment Analysis System

End-to-end system for crawling product reviews, sentiment labeling, machine learning training, topic modeling, and business analytics dashboard.

---

# 🚀 Project Overview

This project includes:

- 🕷️ Data crawling from Tiki reviews
- 🧹 Data preprocessing
- 🧠 Sentiment labeling
- 📊 Business analytics dashboard (Streamlit)
- 🤖 Machine learning pipelines
- 🧩 Topic modeling
- 🔍 Explainability (model interpretation)

---

# 📁 Project Structure (simplified)

```
src/
├── crawlers/
│   └── tiki_sentiment/
│       ├── main.py
│       ├── scripts/
│       └── app/
├── models/
├── topic_modeling/
├── pipelines/
├── dashboard/
└── run_*.py
```

---

# ⚙️ Setup Environment

## 1. Create virtual environment

```bash
python -m venv .venv
```

## 2. Activate environment (Windows PowerShell)

```bash
.\.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

### For crawler module

```bash
pip install -r src/crawlers/tiki_sentiment/requirements.txt
```

### For full project

```bash
pip install -r requirements.txt
```

---

# 🕷️ 1. Crawl Data

```bash
python -m src.crawlers.tiki_sentiment.main
```

---

# 🧱 2. Create Database Tables (Seed)

```bash
python -m src.crawlers.tiki_sentiment.scripts.create_tables
```

---

# 🏷️ 3. Generate Sentiment Labels

```bash
python -m src.crawlers.tiki_sentiment.scripts.generate_labels
```

---

# 📤 4. Export Labeled Data

```bash
python -m src.crawlers.tiki_sentiment.scripts.export_labeled_reviews
```

---

# 📊 5. Run Dashboard

```bash
streamlit run src/dashboard/streamlit_app.py
```

---

# 🧹 6. Preprocessing Pipeline

```bash
python src/run_preprocessing.py
```

---

# 📈 7. Analytics Pipeline

```bash
python src/run_analytics.py
```

---

# 🧠 8. Topic Modeling

```bash
python src/topic_modeling/run_topics.py
```

---

# 🤖 9. Model Training Pipelines

### Train pipeline

```bash
python src/pinelines/train_pipeline.py
```

### Train all models

```bash
python src/pinelines/train_all_models.py
```

---

# 🔥 10. Train PhoBERT Model

```bash
python src/models/phobert/run_train.py
```

---

# 🔍 11. Model Explainability Demo

```bash
python -m src.explainability.run_demo
```

---

# 📊 Key Features

## ✔ Data Pipeline

- Crawl reviews from Tiki
- Store in PostgreSQL
- Upsert-based ingestion

## ✔ Sentiment Analysis

- Rule-based + ML labeling
- Sentiment distribution tracking

## ✔ Business Dashboard

- Total products & categories
- Sentiment KPIs
- Product review analytics
- Category breakdown

## ✔ ML Models

- Traditional ML models
- Deep learning (PhoBERT)
- Ensemble pipelines

## ✔ Topic Modeling

- Business topic extraction
- Category clustering

## ✔ Explainability

- Model interpretation demo
- Feature importance analysis

---

# 📌 Example KPIs in Dashboard

- Total Reviews
- Positive / Negative %
- Total Products
- Products with reviews
- Reviews per product
- Total Categories

---

# ⚠️ Notes

- Ensure PostgreSQL is running before crawling
- Always run `create_tables` before pipeline
- Sentiment labeling must be completed before export dashboard data
- Use consistent Python environment (.venv)

---

# 🚀 Quick Start (Full Pipeline)

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

python -m crawlers.tiki_sentiment.main
python -m crawlers.tiki_sentiment.scripts.create_tables
python -m src.crawlers.tiki_sentiment.scripts.generate_labels
python -m src.crawlers.tiki_sentiment.scripts.export_labeled_reviews

streamlit run dashboard/streamlit_app.py
```

---

# 👨‍💻 Author

Sentiment Analysis System for Business Intelligence  
Built with Python, SQLAlchemy, Streamlit, and Machine Learning pipelines.
