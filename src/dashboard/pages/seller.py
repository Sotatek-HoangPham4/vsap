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

st.title("🏪 Seller Analytics")

seller_df = service.by_seller()

selected = st.selectbox("Select Seller", seller_df.index)

st.subheader(f"Sentiment for Seller: {selected}")
st.bar_chart(seller_df.loc[selected])