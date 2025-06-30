import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("Supply Chain Data.csv", encoding='ISO-8859-1')

# Page config
st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")
st.title("📦 Supply Chain Insights Dashboard")
st.markdown("This interactive dashboard provides macro and micro level insights across supply chain operations, tailored for the Vice President - Supply Chain and key stakeholders.")

# Tabs for structured insights
tabs = st.tabs(["Overview", "Shipping & Delivery", "Sales & Profit", "Geographic View", "Customer Insights", "Product Analysis"])

# ---- OVERVIEW ----
with tabs[0]:
    st.header("🔍 General Overview")
    st.markdown("These KPIs offer a quick glance at the overall scale of operations, customer base, and performance.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Orders", f"{df['Order Id'].nunique():,}")
    col2.metric("Unique Customers", f"{df['Customer Id'].nunique():,}")
    col3.metric("Total Sales ($)", f"{df['Sales'].sum():,.2f}")
    col4.metric("Avg Profit per Order ($)", f"{df['Order Profit Per Order'].mean():.2f}")

    st.markdown("---")
    st.markdown("Below is the distribution of order statuses and shipping modes used.")

    col5, col6 = st.columns(2)
    with col5:
        fig1 = px.histogram(df, x="Order Status", color="Order Status", title="Order Status Distribution")
        st.plotly_chart(fig1, use_container_width=True)
    with col6:
        fig2 = px.histogram(df, x="Shipping Mode", color="Shipping Mode", title="Shipping Mode Usage")
        st.plotly_chart(fig2, use_container_width=True)

# ---- SHIPPING & DELIVERY ----
with tabs[1]:
    st.header("🚚 Shipping & Delivery Performance")
    st.markdown("Track delivery risk, days to ship, and late deliveries across different shipping modes.")

    shipping_mode = st.selectbox("Filter by Shipping Mode", df["Shipping Mode"].unique())
    filtered = df[df["Shipping Mode"] == shipping_mode]

    col1, col2 = st.columns(2)
    with col1:
        fig3 = px.box(filtered, x="Shipping Mode", y="Days for shipping (real)", color="Shipping Mode",
                     title="Actual Shipping Days Distribution")
        st.plotly_chart(fig3, use_container_width=True)
    with col2:
        fig4 = px.box(filtered, x="Shipping Mode", y="Days for shipment (scheduled)", color="Shipping Mode",
                     title="Scheduled Shipping Days Distribution")
        st.plotly_chart(fig4, use_container_width=True)

    fig5 = px.histogram(df, x="Late_delivery_risk", color="Shipping Mode",
                        title="Late Delivery Risk by Shipping Mode", barmode="group")
    st.plotly_chart(fig5, use_container_width=True)

# ---- SALES & PROFIT ----
with tabs[2]:
    st.header("💰 Sales & Profit Trends")
    st.markdown("Understand how sales and profits vary over time and by shipping or product category.")

    df['order_date'] = pd.to_datetime(df['order date (DateOrders)'], errors='coerce')
    sales_by_month = df.groupby(df['order_date'].dt.to_period("M")).agg({'Sales':'sum', 'Order Profit Per Order':'sum'}).reset_index()
    sales_by_month['order_date'] = sales_by_month['order_date'].dt.to_timestamp()

    fig6 = px.line(sales_by_month, x='order_date', y='Sales', title='Monthly Sales Trend')
    fig7 = px.line(sales_by_month, x='order_date', y='Order Profit Per Order', title='Monthly Profit Trend')

    st.plotly_chart(fig6, use_container_width=True)
    st.plotly_chart(fig7, use_container_width=True)

# ---- GEOGRAPHIC VIEW ----
with tabs[3]:
    st.header("🗺️ Geographic Analysis")
    st.markdown("Visualize order spread and profit contribution across global markets.")

    geo_df = df.groupby(['Customer Country', 'Customer City']).agg({'Sales':'sum', 'Order Profit Per Order':'sum'}).reset_index()
    fig8 = px.scatter_geo(geo_df, locations="Customer Country", locationmode="country names",
                          color="Sales", hover_name="Customer City", size="Order Profit Per Order",
                          title="Sales & Profit by Country")
    st.plotly_chart(fig8, use_container_width=True)

# ---- CUSTOMER INSIGHTS ----
with tabs[4]:
    st.header("🧑 Customer Segmentation")
    st.markdown("Explore customer behavior across segments and regions.")

    fig9 = px.histogram(df, x="Customer Segment", color="Customer Segment", title="Orders by Customer Segment")
    fig10 = px.box(df, x="Customer Segment", y="Sales per customer", color="Customer Segment",
                   title="Sales per Customer by Segment")

    st.plotly_chart(fig9, use_container_width=True)
    st.plotly_chart(fig10, use_container_width=True)

# ---- PRODUCT ANALYSIS ----
with tabs[5]:
    st.header("📦 Product & Category Insights")
    st.markdown("Review best-selling products, discounts, and price-performance patterns.")

    top_products = df.groupby("Product Name").agg({'Sales':'sum'}).sort_values("Sales", ascending=False).head(10).reset_index()
    fig11 = px.bar(top_products, x="Product Name", y="Sales", title="Top 10 Products by Sales")

    category_perf = df.groupby("Category Name").agg({'Sales':'sum', 'Order Profit Per Order':'sum'}).reset_index()
    fig12 = px.scatter(category_perf, x="Sales", y="Order Profit Per Order", color="Category Name",
                       size="Sales", title="Sales vs Profit by Category")

    st.plotly_chart(fig11, use_container_width=True)
    st.plotly_chart(fig12, use_container_width=True)
