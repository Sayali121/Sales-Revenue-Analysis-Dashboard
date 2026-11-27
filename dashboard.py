import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Sales & Revenue Dashboard", layout="wide")
st.title("Sales & Revenue Analysis Dashboard")
st.caption("Interactive analysis of sales transactions")
df=pd.read_csv("sales_data.csv")
df["Order_Date"]=pd.to_datetime(df["Order_Date"])
with st.sidebar:
 st.header("Dashboard Filters")
 regions=st.multiselect("Region",sorted(df.Region.unique()),default=list(sorted(df.Region.unique())))
 categories=st.multiselect("Category",sorted(df.Category.unique()),default=list(sorted(df.Category.unique())))
 start=st.date_input("Start date",df.Order_Date.min().date())
 end=st.date_input("End date",df.Order_Date.max().date())
f=df[(df.Region.isin(regions))&(df.Category.isin(categories))&(df.Order_Date.dt.date>=start)&(df.Order_Date.dt.date<=end)]
if f.empty: st.warning("No records match filters.");st.stop()
rev=f.Revenue.sum();orders=f.Order_ID.nunique();units=f.Quantity.sum();aov=rev/orders if orders else 0
a,b,c,d=st.columns(4);a.metric("Total Revenue",f"₹{rev:,.0f}");b.metric("Orders",f"{orders:,}");c.metric("Units Sold",f"{units:,}");d.metric("Average Order Value",f"₹{aov:,.0f}")
f=f.copy();f["Month"]=f.Order_Date.dt.to_period("M").astype(str);monthly=f.groupby("Month",as_index=False).Revenue.sum();region=f.groupby("Region",as_index=False).Revenue.sum().sort_values("Revenue",ascending=False);product=f.groupby("Product",as_index=False).Revenue.sum().sort_values("Revenue",ascending=False).head(10);cat=f.groupby("Category",as_index=False).Revenue.sum()
x,y=st.columns(2);x.plotly_chart(px.line(monthly,x="Month",y="Revenue",markers=True,title="Monthly Revenue Trend"),use_container_width=True);y.plotly_chart(px.bar(region,x="Region",y="Revenue",title="Revenue by Region"),use_container_width=True)
x,y=st.columns(2);x.plotly_chart(px.bar(product,x="Product",y="Revenue",title="Top 10 Products by Revenue"),use_container_width=True);y.plotly_chart(px.pie(cat,names="Category",values="Revenue",title="Revenue Share by Category"),use_container_width=True)
st.subheader("Filtered Transaction Data");st.dataframe(f,use_container_width=True);st.download_button("Download filtered data",f.to_csv(index=False),"filtered_sales.csv","text/csv")
