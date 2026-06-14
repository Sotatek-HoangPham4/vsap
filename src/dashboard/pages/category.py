import streamlit as st
import sys
from pathlib import Path
import asyncio

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from src.data.loader import load_labeled_reviews
from src.data.preprocess import DataPreprocessor
from src.dashboard.services.analytics_service import AnalyticsService


@st.cache_data
def load_data():
    return asyncio.run(load_labeled_reviews())


df = DataPreprocessor().transform(load_data())
service = AnalyticsService(df)

st.title("📦 Category Analytics")

cat_df = service.by_category()

st.subheader("Category vs Sentiment")
st.bar_chart(cat_df)