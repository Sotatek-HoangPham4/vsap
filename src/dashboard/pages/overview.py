import streamlit as st
import sys
from pathlib import Path
import asyncio

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.data.preprocess import DataPreprocessor
from src.services.analytics_service import AnalyticsService


# ⚠️ FIX: tránh Streamlit cache async + SQLAlchemy side effect
async def _load_async():
    from src.data.loader import load_labeled_reviews
    return await load_labeled_reviews()


@st.cache_data
def load_data():
    return asyncio.run(_load_async())


df = load_data()

df = DataPreprocessor().transform(df)
service = AnalyticsService(df)

st.title("📊 Overview Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Total Reviews", service.total_reviews())
col2.metric(
    "Positive %",
    round(service.sentiment_ratio().get("positive", 0), 3)
)
col3.metric(
    "Negative %",
    round(service.sentiment_ratio().get("negative", 0), 3)
)

st.subheader("Sentiment Distribution")
st.bar_chart(service.sentiment_ratio())