import streamlit as st
import pandas as pd
import plotly.express as px
import json
import urllib.request
from sqlalchemy import create_engine
from streamlit_option_menu import option_menu
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# --- Page Config ---
st.set_page_config(page_title="PhonePe Pulse Data Insights", layout="wide", page_icon="💸")

# --- Database Connection ---
@st.cache_resource
def init_connection():
    db_url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    return create_engine(db_url)

engine = init_connection()

@st.cache_data
def load_data(query):
    return pd.read_sql(query, con=engine)

# --- Load GeoJSON ---
@st.cache_data
def load_geojson():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    return data

india_states = load_geojson()

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f6f9;
    }
    h1 {
        color: #5E17EB; /* PhonePe Purple */
    }
    .css-1d391kg, .css-1v3fvcr { /* Sidebar */
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.image("https://www.logo.wine/a/logo/PhonePe/PhonePe-Logo.wine.svg", width=200)
    selected = option_menu("Navigation", ["Home", "Transaction Analysis", "User Analysis", "Insurance Analysis", "Top Performers"], 
        icons=['house', 'cash-coin', 'people', 'shield-check', 'trophy'], menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#5E17EB", "font-size": "20px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#5E17EB", "color": "white", "icon-color":"white"},
        }
    )
    
    st.markdown("---")
    st.subheader("Filters")
    # Fetch available years and quarters from db (hardcoding for now based on typical PhonePe dataset)
    years = [2018, 2019, 2020, 2021, 2022, 2023]
    quarters = [1, 2, 3, 4]
    
    selected_year = st.selectbox("Select Year", ["All"] + years)
    selected_quarter = st.selectbox("Select Quarter", ["All"] + quarters)

# Filter condition helper
def get_filter_condition():
    conditions = []
    if selected_year != "All":
        conditions.append(f"Year = {selected_year}")
    if selected_quarter != "All":
        conditions.append(f"Quarter = {selected_quarter}")
        
    if conditions:
        return "WHERE " + " AND ".join(conditions)
    return ""

# --- Pages ---
if selected == "Home":
    st.title("PhonePe Pulse Data Insights 💸")
    st.markdown("""
        Welcome to the **PhonePe Pulse Data Visualization Dashboard**.
        
        This application explores transaction, user, and insurance data from PhonePe across India. 
        Use the sidebar navigation to dive into specific analysis areas and apply filters to view data for specific years and quarters.
    """)
    st.image("https://www.phonepe.com/pulse/static/c3506ed7ab97816ed41cfa2d9f43702a/82b6b/pulse-bg.png", use_container_width=True)

elif selected == "Transaction Analysis":
    st.title("Transaction Analysis")
    condition = get_filter_condition()
    
    # 1. Total Amount by State
    st.subheader("Total Transaction Amount by State")
    query1 = f"SELECT State, SUM(transaction_amount) as Total_Amount FROM Aggregated_transaction {condition} GROUP BY State ORDER BY Total_Amount DESC"
    try:
        df1 = load_data(query1)
        fig1 = px.bar(df1, x='State', y='Total_Amount', color='Total_Amount', color_continuous_scale='Purples', title="Transaction Amount vs State")
        st.plotly_chart(fig1, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")

    col1, col2 = st.columns(2)
    with col1:
        # 2. Transaction Types
        st.subheader("Transaction Types Breakdown")
        query2 = f"SELECT transaction_type, SUM(transaction_amount) as Total_Amount FROM Aggregated_transaction {condition} GROUP BY transaction_type"
        try:
            df2 = load_data(query2)
            fig2 = px.pie(df2, names='transaction_type', values='Total_Amount', hole=0.4, title="Distribution of Transaction Types", color_discrete_sequence=px.colors.sequential.Purples_r)
            st.plotly_chart(fig2, use_container_width=True)
        except Exception as e:
             st.error("Data not available")
             
    with col2:
        # 3. Quarterly Trend
        st.subheader("Quarterly Transaction Trend")
        # For trend, we ignore the quarter filter to show the trend
        trend_condition = f"WHERE Year = {selected_year}" if selected_year != "All" else ""
        query3 = f"SELECT Year, Quarter, SUM(transaction_amount) as Total_Amount FROM Aggregated_transaction {trend_condition} GROUP BY Year, Quarter ORDER BY Year, Quarter"
        try:
            df3 = load_data(query3)
            df3['Time'] = df3['Year'].astype(str) + "-Q" + df3['Quarter'].astype(str)
            fig3 = px.line(df3, x='Time', y='Total_Amount', markers=True, title="Transaction Amount Trend", line_shape='spline')
            fig3.update_traces(line_color='#5E17EB', line_width=3)
            st.plotly_chart(fig3, use_container_width=True)
        except Exception as e:
            st.error("Data not available")

    # 4. Choropleth Map
    st.subheader("Geospatial Analysis: Transaction Amount")
    query4 = f"SELECT State, SUM(transaction_amount) as Total_Amount FROM Map_transaction {condition} GROUP BY State"
    try:
        df4 = load_data(query4)
        # Ensure State names match geojson
        fig4 = px.choropleth(df4, 
                             geojson=india_states, 
                             featureidkey='properties.ST_NM',
                             locations='State', 
                             color='Total_Amount',
                             color_continuous_scale='Purples',
                             title="Transaction Amount Map of India",
                             hover_name="State",
                             fitbounds="locations")
        fig4.update_geos(visible=False)
        st.plotly_chart(fig4, use_container_width=True)
    except Exception as e:
        st.error("Data not available for map")

elif selected == "User Analysis":
    st.title("User Analysis")
    condition = get_filter_condition()
    
    col1, col2 = st.columns(2)
    with col1:
        # Registered Users by State
        st.subheader("Registered Users by State")
        query1 = f"SELECT State, SUM(registered_users) as Total_Users FROM Map_user {condition} GROUP BY State ORDER BY Total_Users DESC LIMIT 15"
        try:
            df1 = load_data(query1)
            fig1 = px.bar(df1, x='Total_Users', y='State', orientation='h', color='Total_Users', color_continuous_scale='Blues', title="Top 15 States by Registered Users")
            fig1.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig1, use_container_width=True)
        except Exception as e:
            st.error("Data not available")
            
    with col2:
        # Device Brands
        st.subheader("Users by Device Brand")
        query2 = f"SELECT brand, SUM(user_count) as Total_Users FROM Aggregated_user {condition} GROUP BY brand ORDER BY Total_Users DESC LIMIT 10"
        try:
            df2 = load_data(query2)
            fig2 = px.pie(df2, names='brand', values='Total_Users', title="Top 10 Device Brands", hole=0.3, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig2, use_container_width=True)
        except Exception as e:
            st.error("Data not available")

elif selected == "Insurance Analysis":
    st.title("Insurance Analysis")
    condition = get_filter_condition()
    
    # Insurance Amount by State
    st.subheader("Total Insurance Amount by State")
    query1 = f"SELECT State, SUM(insurance_amount) as Total_Amount FROM Aggregated_insurance {condition} GROUP BY State ORDER BY Total_Amount DESC"
    try:
        df1 = load_data(query1)
        if not df1.empty:
            fig1 = px.bar(df1, x='State', y='Total_Amount', color='Total_Amount', color_continuous_scale='Teal', title="Insurance Amount vs State")
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No insurance data available for the selected filters.")
    except Exception as e:
        st.error(f"Data not available. Make sure the database schema and data are correctly populated.")

elif selected == "Top Performers":
    st.title("Top Performers")
    condition = get_filter_condition()
    
    tabs = st.tabs(["States", "Districts", "Pin Codes"])
    
    with tabs[0]:
        st.subheader("Top 10 States")
        query1 = f"SELECT State, SUM(transaction_amount) as Total_Amount FROM Aggregated_transaction {condition} GROUP BY State ORDER BY Total_Amount DESC LIMIT 10"
        try:
            df1 = load_data(query1)
            fig1 = px.bar(df1, x='State', y='Total_Amount', text_auto='.2s', title="Top 10 States by Transaction Amount", color='Total_Amount', color_continuous_scale='Purples')
            st.plotly_chart(fig1, use_container_width=True)
            st.dataframe(df1, use_container_width=True)
        except:
            st.error("Data not available")
            
    with tabs[1]:
        st.subheader("Top 10 Districts")
        query2 = f"SELECT entity_name as District, SUM(transaction_amount) as Total_Amount FROM Top_transaction WHERE entity_type='district' {'AND ' + condition[6:] if condition else ''} GROUP BY entity_name ORDER BY Total_Amount DESC LIMIT 10"
        try:
            df2 = load_data(query2)
            fig2 = px.bar(df2, x='Total_Amount', y='District', orientation='h', title="Top 10 Districts by Transaction Amount", color='Total_Amount', color_continuous_scale='Purples')
            fig2.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig2, use_container_width=True)
            st.dataframe(df2, use_container_width=True)
        except:
            st.error("Data not available")
            
    with tabs[2]:
        st.subheader("Top 10 Pin Codes")
        query3 = f"SELECT entity_name as Pincode, SUM(transaction_amount) as Total_Amount FROM Top_transaction WHERE entity_type='pincode' {'AND ' + condition[6:] if condition else ''} GROUP BY entity_name ORDER BY Total_Amount DESC LIMIT 10"
        try:
            df3 = load_data(query3)
            fig3 = px.bar(df3, x='Total_Amount', y='Pincode', orientation='h', title="Top 10 Pin Codes by Transaction Amount", color='Total_Amount', color_continuous_scale='Purples')
            fig3.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig3, use_container_width=True)
            st.dataframe(df3, use_container_width=True)
        except:
            st.error("Data not available")
