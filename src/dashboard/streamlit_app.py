import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd
import plotly.express as px

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


total_reviews = len(df)
positive = (df["sentiment"] == "positive").mean()
neutral = (df["sentiment"] == "neutral").mean()
negative = (df["sentiment"] == "negative").mean()

total_categories = df["category"].nunique() if "category" in df.columns else 0
total_products = df["product_id"].nunique() if "product_id" in df.columns else 0

# =====================
# 2 COLUMNS LAYOUT
# =====================
left_col, right_col = st.columns([2, 1])

# =====================
# COL 1: METRICS
# =====================
with left_col:
    st.subheader("📌 Key Metrics")
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Reviews", total_reviews)
    col2.metric("Total Categories", total_categories)
    col3.metric("Total Products", total_products)

    col4, col5, col6 = st.columns(3)

    col4.metric("Positive %", f"{positive:.2%}")
    col5.metric("Neutral %", f"{neutral:.2%}")
    col6.metric("Negative %", f"{negative:.2%}")

# =====================
# COL 2: CHART
# =====================
with right_col:
    
    sent = df["sentiment"].value_counts().reset_index()
    sent.columns = ["sentiment", "count"]

    fig = px.pie(sent, names="sentiment", values="count", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)






import pandas as pd
import streamlit as st
import plotly.express as px

# =====================
# CHECK COLUMN
# =====================
if "category" in df.columns:

    # =====================
    # CATEGORY STATS
    # =====================
    category_stats = (
        df.groupby("category")["sentiment"]
        .value_counts(normalize=True)
        .unstack()
        .fillna(0)
    )

    # đảm bảo đủ cột
    for col in ["positive", "neutral", "negative"]:
        if col not in category_stats.columns:
            category_stats[col] = 0

    if category_stats.empty:
        st.warning("⚠️ Không có dữ liệu category")
        st.stop()

    categories = category_stats.index.tolist()

    # =====================
    # HEADER (TITLE + SELECT CATEGORY)
    # =====================
    title_col, spacer, action_col = st.columns([2, 1, 2], vertical_alignment="center")

    with title_col:
        st.subheader("📦 Category Sentiment Analysis")

    with action_col:
        selected_category = st.selectbox(
            "",
            options=categories,
            index=0
        )

    # =====================
    # LAYOUT
    # =====================
    left_col, gap, right_col = st.columns([1.2, 0.2, 2])

    # =====================
    # LEFT: TABLE
    # =====================
    with right_col:
    
        st.dataframe(
            category_stats.style.format("{:.2%}"),
            use_container_width=True
        )

    # =====================
    # RIGHT: CHART
    # =====================
    with left_col:

       

        selected_data = category_stats.loc[selected_category]

        chart_df = pd.DataFrame({
            "sentiment": selected_data.index,
            "value": selected_data.values
        })

        order = ["positive", "neutral", "negative"]
        chart_df["sentiment"] = pd.Categorical(
            chart_df["sentiment"],
            categories=order,
            ordered=True
        )
        chart_df = chart_df.sort_values("sentiment")

        fig = px.bar(
            chart_df,
            x="sentiment",
            y="value",
            text_auto=".2%",
            color="sentiment",
          
        )

        fig.update_layout(
            showlegend=False,
            yaxis_title="Proportion",
            margin=dict(l=20, r=20, t=30, b=20)
        )

     

        st.plotly_chart(fig, use_container_width=True)
       

else:
    st.warning("⚠️ Chưa có cột category")













# =====================
# PRODUCT ANALYSIS
# =====================
import pandas as pd
import streamlit as st
import plotly.express as px

# =====================
# SIDEBAR FILTER (PUT FIRST)
# =====================
st.sidebar.header("Filters")

category = st.sidebar.selectbox(
    "Category",
    ["All"] + list(df["category"].dropna().unique())
)

if category != "All":
    df = df[df["category"] == category]

# =====================
# SENTIMENT STATUS
# =====================
df["status"] = df["sentiment"].map({
    "positive": "Closed",
    "neutral": "Open",
    "negative": "Backlog"
})

# =====================
# TOP PRODUCTS
# =====================
st.subheader("🧾 Top Products")

top = (
    df["product_name"]
    .value_counts()
    .head(10)
    .reset_index()
)

top.columns = ["product", "count"]

# =====================
# BAR CHART
# =====================
fig = px.bar(
    top,
    x="count",
    y="product",
    orientation="h",
    text_auto=True,
    color="count",
    color_continuous_scale="Blues"
)

fig.update_layout(
    xaxis_title="Review Count",
    yaxis_title="Product",
    showlegend=False,
    margin=dict(l=20, r=20, t=30, b=20)
)

st.plotly_chart(fig, use_container_width=True)

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





import streamlit as st
import pandas as pd
import plotly.express as px

# =====================
# CATEGORY → PRODUCT COUNT
# =====================
st.subheader("📊 Top Categories by Unique Products")

if "category" in df.columns and "product_id" in df.columns:

    category_product_stats = (
        df.groupby("category")["product_id"]
        .nunique()
        .reset_index(name="unique_products")
        .sort_values("unique_products", ascending=False)
        .head(10)   # 🔥 TAKE TOP 10
    )

    # =====================
    # LAYOUT (TABLE + CHART OPTIONAL)
    # =====================
    left_col, gap, right_col = st.columns([1.2, 0.1, 2])

    # =====================
    # LEFT: TABLE
    # =====================
    with left_col:
  

        st.dataframe(
            category_product_stats,
            use_container_width=True
        )

    # =====================
    # RIGHT: BAR CHART
    # =====================
    with right_col:
  

        fig = px.bar(
            category_product_stats,
            x="unique_products",
            y="category",
            orientation="h",
            text_auto=True,
            color="unique_products",
          
        )

        fig.update_layout(
            xaxis_title="Unique Products",
            yaxis_title="Category",
            showlegend=False,
            margin=dict(l=20, r=20, t=30, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("⚠️ Thiếu category hoặc product_id")





# # =====================
# # SELLER ANALYSIS (SAFE)
# # =====================
# st.subheader("🏪 Seller Analysis")

# if "seller" in df.columns:

#     seller_stats = (
#         df.groupby("seller")["sentiment"]
#         .value_counts(normalize=True)
#         .unstack()
#         .fillna(0)
#     )

#     st.dataframe(seller_stats)

# else:
#     st.warning("⚠️ Chưa có seller name → fallback seller_id")

#     if "seller_id" in df.columns:
#         seller_stats = (
#             df.groupby("seller_id")["sentiment"]
#             .value_counts(normalize=True)
#             .unstack()
#             .fillna(0)
#         )

#         st.dataframe(seller_stats)