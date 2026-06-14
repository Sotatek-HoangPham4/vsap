import sys
from pathlib import Path
import asyncio
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from src.analytics.aggregator import AnalyticsAggregator
from src.data.preprocess import DataPreprocessor
from src.data.loader import load_labeled_reviews


@st.cache_data
def load_data():
    return asyncio.run(load_data_async())


async def load_data_async():
    df = await load_labeled_reviews()
    df = DataPreprocessor().transform(df)
    return df


st.set_page_config(page_title="Sentiment Dashboard", layout="wide")

df = load_data()

agg = AnalyticsAggregator(df)

st.title("📊 Sentiment Analytics Dashboard")

st.metric("Total Reviews", agg.total_reviews())
st.metric("Positive %", agg.positive_ratio())
st.metric("Negative %", agg.negative_ratio())

st.line_chart(agg.sentiment_trend())