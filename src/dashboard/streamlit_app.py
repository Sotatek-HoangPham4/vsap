import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sentiment Analytics", layout="wide")

st.title("📊 Business Analytics Dashboard")

# =====================
# LOAD DATA
# =====================
df = pd.read_csv("data/interim/dashboard_data.csv")

# =====================
# CLEAN DATA
# =====================
df["sentiment"] = df["sentiment"].fillna("unknown")

# =====================
# KPI SECTION
# =====================
st.subheader("📌 Key Metrics")

total_reviews = len(df)
positive = (df["sentiment"] == "positive").mean()
negative = (df["sentiment"] == "negative").mean()

total_categories = df["category"].nunique() if "category" in df.columns else 0
total_products = df["product_id"].nunique() if "product_id" in df.columns else 0

col1, col2, col3 = st.columns(3)

col1.metric("Total Reviews", total_reviews)
col2.metric("Positive %", f"{positive:.2%}")
col3.metric("Negative %", f"{negative:.2%}")

col4, col5 = st.columns(2)

col4.metric("Total Categories", total_categories)
col5.metric("Total Products", total_products)

# =====================
# CATEGORY ANALYSIS
# =====================
st.subheader("📦 Category Sentiment Analysis")

if "category" in df.columns:
    category_stats = (
        df.groupby("category")["sentiment"]
        .value_counts(normalize=True)
        .unstack()
        .fillna(0)
    )

    st.dataframe(category_stats)

else:
    st.warning("⚠️ Chưa có cột category")

# =====================
# PRODUCT ANALYSIS
# =====================
st.subheader("🧾 Reviewed Products")

if "product_id" in df.columns:

    if "product_name" in df.columns:
        product_stats = (
            df.groupby(["product_id", "product_name"])
            .size()
            .reset_index(name="review_count")
            .sort_values("review_count", ascending=False)
        )
    else:
        product_stats = (
            df.groupby("product_id")
            .size()
            .reset_index(name="review_count")
            .sort_values("review_count", ascending=False)
        )

    st.dataframe(product_stats)

else:
    st.warning("⚠️ Thiếu product_id")

# =====================
# CATEGORY → PRODUCT COUNT
# =====================
st.subheader("📊 Products per Category")

if "category" in df.columns and "product_id" in df.columns:

    category_product_stats = (
        df.groupby("category")["product_id"]
        .nunique()
        .reset_index(name="unique_products")
        .sort_values("unique_products", ascending=False)
    )

    st.dataframe(category_product_stats)

else:
    st.warning("⚠️ Thiếu category hoặc product_id")

# =====================
# SELLER ANALYSIS (SAFE)
# =====================
st.subheader("🏪 Seller Analysis")

if "seller" in df.columns:

    seller_stats = (
        df.groupby("seller")["sentiment"]
        .value_counts(normalize=True)
        .unstack()
        .fillna(0)
    )

    st.dataframe(seller_stats)

else:
    st.warning("⚠️ Chưa có seller name → fallback seller_id")

    if "seller_id" in df.columns:
        seller_stats = (
            df.groupby("seller_id")["sentiment"]
            .value_counts(normalize=True)
            .unstack()
            .fillna(0)
        )

        st.dataframe(seller_stats)