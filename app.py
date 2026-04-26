import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Dashboard")

# Generate sample data
@st.cache_data
def generate_data():
    products = ["Laptop", "Mobile", "Headphones", "Keyboard", "Mouse"]
    regions = ["North", "South", "East", "West"]
    
    data = []
    start_date = datetime(2024, 1, 1)
    
    for i in range(200):
        date = start_date + timedelta(days=random.randint(0, 180))
        product = random.choice(products)
        region = random.choice(regions)
        quantity = random.randint(1, 10)
        price = random.randint(500, 5000)
        sales = quantity * price
        
        data.append([date, product, region, quantity, price, sales])
    
    df = pd.DataFrame(data, columns=["Date", "Product", "Region", "Quantity", "Price", "Sales"])
    return df

df = generate_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_product = st.sidebar.multiselect("Select Product", df["Product"].unique(), default=df["Product"].unique())
selected_region = st.sidebar.multiselect("Select Region", df["Region"].unique(), default=df["Region"].unique())

# Filter data
filtered_df = df[df["Product"].isin(selected_product) & df["Region"].isin(selected_region)]

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Quantity", f"{filtered_df['Quantity'].sum():,.0f}")
col3.metric("Average Order Value", f"${filtered_df['Sales'].mean():,.0f}")
col4.metric("Total Transactions", len(filtered_df))

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Product")
    product_sales = filtered_df.groupby("Product")["Sales"].sum().sort_values()
    st.bar_chart(product_sales)

with col2:
    st.subheader("Sales by Region")
    region_sales = filtered_df.groupby("Region")["Sales"].sum()
    st.bar_chart(region_sales)

st.subheader("Daily Sales Trend")
daily_sales = filtered_df.groupby("Date")["Sales"].sum()
st.line_chart(daily_sales)

st.subheader("Data Preview")
st.dataframe(filtered_df)