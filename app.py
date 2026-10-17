import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Online Retail Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Online Retail Sales Dashboard")
st.caption("Interactive sales analysis using the UCI Online Retail dataset")

@st.cache_data
def load_data():
    if Path("Online_Retail.xlsx").exists():
        df = pd.read_excel("Online_Retail.xlsx")
    elif Path("Online Retail.xlsx").exists():
        df = pd.read_excel("Online Retail.xlsx")
    elif Path("Online_Retail.csv").exists():
        df = pd.read_csv("Online_Retail.csv", encoding="ISO-8859-1")
    else:
        st.error(f"Dataset not found. Files available: {list(Path('.').iterdir())}")
        st.stop()

    df.columns = df.columns.str.strip()

    required = [
        "InvoiceNo", "StockCode", "Description",
        "Quantity", "InvoiceDate", "UnitPrice", "Country"
    ]

    missing = [col for col in required if col not in df.columns]
    if missing:
        st.error(f"Missing columns: {missing}")
        st.stop()

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    )
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

    df = df.dropna(
        subset=["InvoiceNo", "StockCode", "InvoiceDate",
                "Quantity", "UnitPrice", "Country"]
    )

    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df = df[~df["InvoiceNo"].str.startswith("C")]
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df["Description"] = df["Description"].fillna("Unknown product")

    return df


df = load_data()

if df is None:
    st.error(
        "Dataset file not found. Upload Online_Retail.xlsx "
        "or Online_Retail.csv to the same folder as app.py."
    )
    st.stop()

st.sidebar.header("🔎 Dashboard Filters")

min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

countries = sorted(df["Country"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect(
    "Select countries",
    countries,
    default=countries
)

min_quantity = st.sidebar.number_input(
    "Minimum quantity", min_value=1, value=1
)

top_n = st.sidebar.slider(
    "Top products to display", 5, 20, 10
)

filtered = df.copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        (filtered["InvoiceDate"].dt.date >= start_date)
        & (filtered["InvoiceDate"].dt.date <= end_date)
    ]

filtered = filtered[
    filtered["Country"].isin(selected_countries)
    & (filtered["Quantity"] >= min_quantity)
]

if filtered.empty:
    st.warning("No data for the selected filters. Please change the filters.")
    st.stop()

total_revenue = filtered["Revenue"].sum()
total_orders = filtered["InvoiceNo"].nunique()
total_products = filtered["StockCode"].nunique()
total_customers = (
    filtered["CustomerID"].nunique()
    if "CustomerID" in filtered.columns else 0
)
total_units = filtered["Quantity"].sum()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("💰 Total Revenue", f"£{total_revenue:,.2f}")
c2.metric("🧾 Orders", f"{total_orders:,}")
c3.metric("📦 Products", f"{total_products:,}")
c4.metric("👥 Customers", f"{total_customers:,}")
c5.metric("🛒 Units Sold", f"{total_units:,.0f}")

st.divider()

monthly = (
    filtered.set_index("InvoiceDate")
    .resample("MS")
    .agg(Revenue=("Revenue", "sum"))
    .reset_index()
)

quarterly = (
    filtered.set_index("InvoiceDate")
    .resample("QS")
    .agg(Revenue=("Revenue", "sum"))
    .reset_index()
)

left, right = st.columns(2)

with left:
    st.subheader("📈 Monthly Revenue")
    fig = px.line(
        monthly, x="InvoiceDate", y="Revenue",
        markers=True, title="Revenue by Month"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("📊 Quarterly Revenue")
    fig = px.bar(
        quarterly, x="InvoiceDate", y="Revenue",
        title="Revenue by Quarter"
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

product_sales = (
    filtered.groupby(["StockCode", "Description"], as_index=False)
    .agg(Revenue=("Revenue", "sum"),
         Quantity=("Quantity", "sum"))
    .sort_values("Revenue", ascending=False)
    .head(top_n)
)

country_sales = (
    filtered.groupby("Country", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue", ascending=False)
    .head(15)
)

left, right = st.columns(2)

with left:
    st.subheader(f"🏆 Top {top_n} Products")
    fig = px.bar(
        product_sales, x="Revenue", y="Description",
        orientation="h", title="Products by Revenue"
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("🌍 Revenue by Country")
    fig = px.bar(
        country_sales, x="Country", y="Revenue",
        title="Top 15 Countries"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("🔗 Quantity vs Revenue")
scatter_data = filtered.sample(
    n=min(3000, len(filtered)), random_state=42
)
fig = px.scatter(
    scatter_data,
    x="Quantity",
    y="Revenue",
    color="Country",
    hover_data=["Description", "InvoiceNo"],
    title="Relationship Between Quantity and Revenue"
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("📋 Filtered Sales Data")
st.dataframe(filtered, use_container_width=True)

csv_data = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Filtered Data as CSV",
    data=csv_data,
    file_name="online_retail_filtered.csv",
    mime="text/csv"
)

st.caption("CodeNova | Online Retail Data Analysis Dashboard")
