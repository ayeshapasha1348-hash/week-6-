# Week6 - Interactive Sales Dashboard
# This script loads sales data,cleans it,creates multiple visualizations,
# and saves the charts into the visualizations folder.

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# -----------------------------
# Step1 : Settings & Folder Setup
# -----------------------------

sns.set_theme(style="whitegrid")  # clean seaborn theme

OUTPUT_DIR = "visualizations"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# Step2 : Load Dataset
# -----------------------------
try:
    df = pd.read_csv("sales_data.csv")
    print("sales_data.csv loaded successfully!")
except FileNotFoundError:
    print("sales_data.csv not found. Please keep it in the same folder as dashboard.py")
    raise

# -----------------------------
# Step 3: Data Cleaning & Preparation
# -----------------------------
# Convert date column to datetime
df["Date"] = pd.to_datetime(df["Date"],errors="coerce")

# Remove rows with invalid dates
df = df.dropna(subset=["Date"])

# Remove duplicates
df = df.drop_duplicates()

# Fill missing numerical values
numeric_cols = ["Quantity","Price","Total_Sales"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col],errors="coerce")
        df[col] = df[col].fillna(0)

# Clean text columns
text_cols = ["Product","Region","Customer_ID"]
for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()

# Feature engineering (Month)
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.month_name()

print("Data cleaning completed!\n")

# -----------------------------
# Step 4: KPI Summary
# -----------------------------
total_revenue = df["Total_Sales"].sum()
avg_order_value = df["Total_Sales"].mean()
top_product = df.groupby("Product")["Total_Sales"].sum().idxmax()

print("KPI SUMMARY")
print("-" * 40)
print(f"Total Revenue      : ₹{total_revenue:,.0f}")
print(f"Average Order Value: ₹{avg_order_value:,.0f}")
print(f"Top Product        : {top_product}")
print("-" * 40, "\n")

# -----------------------------
# Step 5: Visualization 1 - Sales Trend (Line Chart)
# -----------------------------
daily_sales = df.groupby("Date")["Total_Sales"].sum().reset_index()

plt.figure(figsize=(10,5))
plt.plot(daily_sales["Date"],daily_sales["Total_Sales"],marker="o")
plt.title("Sales Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "01_sales_trend_line.png"))
plt.close()

# -----------------------------
# Step 6: Visualization 2 - Sales by Product (Bar Chart)
# -----------------------------
product_sales = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)

plt.figure(figsize=(10,5))
product_sales.plot(kind="bar")
plt.title("Total Sales by Product")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR,"02_sales_by_product_bar.png"))
plt.close()

# -----------------------------
# Step 7: Visualization 3 - Box Plot (Sales Distribution by Region)
# -----------------------------
plt.figure(figsize=(10,5))
sns.boxplot(data=df,x="Region",y="Total_Sales")
plt.title("Sales Distribution by Region(Box Plot)")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR,"03_sales_distribution_box.png"))
plt.close()

# -----------------------------
# Step 8: Visualization 4 - Violin Plot(Sales Distribution by Product)
# -----------------------------
plt.figure(figsize=(10,5))
sns.violinplot(data=df, x="Product",y="Total_Sales")
plt.title("Sales Distribution by Product (Violin Plot)")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR,"04_sales_violin_product.png"))
plt.close()

# -----------------------------
# Step 9: Visualization 5 - Correlation Heatmap
# -----------------------------
corr = df[["Quantity","Price","Total_Sales"]].corr()

plt.figure(figsize=(6,5))
sns.heatmap(corr,annot=True,cmap="Blues")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR,"05_correlation_heatmap.png"))
plt.close()

# -----------------------------
# Step 10: Dashboard Layout (2x2 Grid)
# -----------------------------
fig,axes = plt.subplots(2,2,figsize=(14,10))

# Plot 1: Trend (top-left)
axes[0,0].plot(daily_sales["Date"],daily_sales["Total_Sales"],marker="o")
axes[0,0].set_title("Sales Trend Over Time")
axes[0,0].set_xlabel("Date")
axes[0,0].set_ylabel("Total Sales")

# Plot 2: Product bar (top-right)
product_sales.plot(kind="bar",ax=axes[0,1])
axes[0,1].set_title("Total Sales by Product")
axes[0,1].set_xlabel("Product")
axes[0,1].set_ylabel("Total Sales")

# Plot 3: Boxplot region (bottom-left)
sns.boxplot(data=df,x="Region",y="Total_Sales",ax=axes[1,0])
axes[1,0].set_title("Sales Distribution by Region")
axes[1,0].set_xlabel("Region")
axes[1,0].set_ylabel("Total Sales")

# Plot 4: Heatmap (bottom-right)
sns.heatmap(corr,annot=True, cmap="Blues",ax=axes[1,1])
axes[1,1].set_title("Correlation Heatmap")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR,"06_dashboard_2x2_grid.png"))
plt.close()

# -----------------------------
# Step 11: Interactive Plotly Charts
# -----------------------------
# Interactive bar chart
fig_bar = px.bar(
    product_sales.reset_index(),
    x="Product",
    y="Total_Sales",
    title="Interactive : Total Sales by Product",
)

fig_bar.write_html(os.path.join(OUTPUT_DIR,"07_plotly_sales_by_product.html"))

# Interactive line chart
fig_line = px.line(
    daily_sales,
    x="Date",
    y="Total_Sales",
    title="Interactive : Sales Trend Over Time",
)

fig_line.write_html(os.path.join(OUTPUT_DIR,"08_plotly_sales_trend.html"))

print("All charts are generated and saved successfully!")
print(f"Check the '{OUTPUT_DIR}' folder for outputs.")
