# phonepe_dashboard_app.py
import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import requests
import json

# --- DB Connection ---
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="phonepe_user",
            password="harish@21",
            database="phonepe_db",
            auth_plugin='mysql_native_password'
        )
    except mysql.connector.Error as err:
        st.error(f"Database connection error: {err}")
        return None

def execute_query(query, params=None):
    try:
        conn = get_db_connection()
        if conn is None:
            return pd.DataFrame()
            
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        conn.close()
        
        df = pd.DataFrame(result)
        
        # FIX: Convert numeric columns to proper data types
        if not df.empty:
            numeric_columns = [
                'TotalTransactions', 'AvgTransactions', 'TotalRevenue', 'AvgRevenue',
                'Transaction_count', 'Transaction_amount', 'RegisteredUser', 'AppOpens',
                'TotalCount', 'Amount', 'Total', 'TotalAmount', 'Users', 'Opens', 'Count',
                'TotalUsers', 'TotalOpens', 'Total_count', 'Total_amount', 'Percentage'
            ]
            
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Convert year/quarter columns
            if 'Years' in df.columns:
                df['Years'] = pd.to_numeric(df['Years'], errors='coerce').fillna(0).astype(int)
            if 'Quarter' in df.columns:
                df['Quarter'] = pd.to_numeric(df['Quarter'], errors='coerce').fillna(0).astype(int)
        
        return df
        
    except mysql.connector.Error as err:
        st.error(f"Error executing query: {err}")
        return pd.DataFrame()

def safe_plotly_chart(fig, message="No data available for visualization"):
    """Safely display plotly chart with error handling"""
    try:
        if fig and hasattr(fig, 'data') and fig.data:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
        else:
            st.info(message)
    except Exception as e:
        st.error(f"Error displaying chart: {e}")

def create_safe_choropleth(df, geo_data, location_col, value_col, title, color_scale="reds"):
    """Safely create choropleth map with proper data validation"""
    try:
        if df.empty or geo_data is None:
            return None
            
        # Create a clean copy and ensure value column is numeric
        df_clean = df.copy()
        df_clean[value_col] = pd.to_numeric(df_clean[value_col], errors='coerce').fillna(0)
        
        # Remove any rows with invalid values
        df_clean = df_clean[df_clean[value_col] >= 0]
        
        if df_clean.empty:
            return None
            
        # Create the choropleth
        fig = px.choropleth(
            df_clean, 
            geojson=geo_data, 
            locations=location_col,
            featureidkey="properties.ST_NM", 
            color=value_col,
            color_continuous_scale=color_scale,
            title=title
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating choropleth: {e}")
        return None

# --- Global Config ---
st.set_page_config(page_title="PhonePe Dashboard", layout="wide")

# Load GeoJSON data with error handling
try:
    GEO_URL = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(GEO_URL, timeout=10)
    response.raise_for_status()
    geo = response.json()
except requests.RequestException as e:
    st.error(f"Failed to load GeoJSON data: {e}")
    geo = None
except json.JSONDecodeError as e:
    st.error(f"Failed to parse GeoJSON data: {e}")
    geo = None

quarter_map = {
    "Q1 (Jan-Mar)": 1,
    "Q2 (Apr-Jun)": 2,
    "Q3 (Jul-Sep)": 3,
    "Q4 (Oct-Dec)": 4
}

# --- Navigation ---
st.sidebar.title("Navigation")
if st.sidebar.button("🏠 Home", use_container_width=True):
    st.session_state.page = "Home"
if st.sidebar.button("📊 Business Case Study", use_container_width=True):
    st.session_state.page = "Business Case Study"
if st.sidebar.button("📈 Case Study Insights", use_container_width=True):
    st.session_state.page = "Case Study Insights"

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Home"

# --- Home ---
if st.session_state.page == "Home":
    st.title("🏠 Home")
    st.markdown("""
        <style>
        .home-title {
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            color: #6C63FF;
        }
        .home-subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #333;
            margin-bottom: 2rem;
        }
        .info-box {
            background-color: #F0F4FF;
            border-left: 6px solid #6C63FF;
            padding: 1rem 1.5rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            font-size: 1rem;
            color: #222;
        }
        .highlight {
            color: #6C63FF;
            font-weight: bold;
        }
        </style>

        <div class="home-title">📱 PhonePe Transaction Insights</div>
        <div class="home-subtitle">Explore India's Digital Economy with Real-time PhonePe Data</div>
        <hr style='border: 1px solid #6C63FF;'>
    """, unsafe_allow_html=True)

    st.markdown("###  What Can You Discover?")

    st.markdown("""
        <div class="info-box"> <span class='highlight'>Aggregated Transactions:</span> View transaction volumes by type, region, and trends over time.</div>
        <div class="info-box"> <span class='highlight'>User Engagement:</span> Explore how users interact with the app across brands, states, and districts.</div>
        <div class="info-box"> <span class='highlight'>Insurance Analytics:</span> Analyze state-wise and district-level adoption of insurance services.</div>
        <div class="info-box"> <span class='highlight'>Interactive Visuals:</span> Choropleths, bar charts, line graphs, and pie charts to bring data to life.</div>
        <div class="info-box"> <span class='highlight'>Custom Filters:</span> Filter insights by year and quarter across the country.</div>
    """, unsafe_allow_html=True)

    st.success("Use the sidebar to explore the full Business Case Study ➡")

# --- Business Case Study ---
elif st.session_state.page == "Business Case Study":
    st.title("📊 Business Case Study")
    
    # Year & Quarter Dropdown (once only)
    years = ["All"] + [str(y) for y in range(2018, 2025)]
    quarters = ["All"] + list(quarter_map.keys())

    col1, col2 = st.columns(2)
    selected_year = col1.selectbox("Select Year", years)
    selected_quarter = col2.selectbox("Select Quarter", quarters)

    year = int(selected_year) if selected_year != "All" else None
    quarter = quarter_map[selected_quarter] if selected_quarter != "All" else None

    conditions = []
    params = []

    if year is not None:
        conditions.append("Years = %s")
        params.append(year)
    if quarter is not None:
        conditions.append("Quarter = %s")
        params.append(quarter)

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    sub_tab = st.radio("Choose Analysis", ["Transaction", "User", "Insurance"])

    if sub_tab == "Transaction":
        st.subheader("💳 Transaction Overview")

        df = execute_query(f"""
            SELECT 
                SUM(Transaction_count) AS TotalTransactions,
                AVG(Transaction_count) AS AvgTransactions,
                SUM(Transaction_amount) AS TotalRevenue,
                AVG(Transaction_amount) AS AvgRevenue
            FROM aggregated_transaction
            {where_clause}
        """, tuple(params))

        if not df.empty and len(df) > 0:
            total_txn = df.iloc[0].get('TotalTransactions', 0) or 0
            avg_tx = df.iloc[0].get('AvgTransactions', 0) or 0
            total_rev = df.iloc[0].get('TotalRevenue', 0) or 0
            avg_rev = df.iloc[0].get('AvgRevenue', 0) or 0

            col1, col2 = st.columns(2)
            col1.metric("Total Transactions", f"{total_txn:,.0f}")
            col1.metric("Average Transactions", f"{avg_tx:,.2f}")
            col2.metric("Total Revenue (₹)", f"₹{total_rev:,.2f}")
            col2.metric("Avg Revenue (₹)", f"₹{avg_rev:,.2f}")
        else:
            st.warning("No transaction data available for selected filters.")

        if geo is not None:
            df_map = execute_query(f"""
                SELECT States, SUM(Transaction_count) AS TotalTransactions
                FROM map_transaction
                {where_clause}
                GROUP BY States
            """, tuple(params))

            if not df_map.empty:
                # FIXED: Use safe choropleth function
                fig = create_safe_choropleth(
                    df_map, geo, "States", "TotalTransactions",
                    "State-wise Total Transactions", "reds"
                )
                if fig:
                    safe_plotly_chart(fig)
                else:
                    st.warning("Could not create transaction map")

                st.markdown("### 📌 Top 10 States by Transaction Volume")
                df_top = df_map.sort_values(by="TotalTransactions", ascending=False).head(10)
                st.dataframe(df_top, use_container_width=True)
            else:
                st.warning("No state-wise transaction data available.")
        else:
            st.warning("Geographical data not available for mapping.")

    elif sub_tab == "User":
        st.subheader("📱 User Engagement and Growth Strategy")

        df_total = execute_query(f"""
            SELECT SUM(RegisteredUser) as TotalUsers, SUM(AppOpens) as TotalOpens 
            FROM map_user {where_clause}
        """, tuple(params))

        if not df_total.empty and len(df_total) > 0:
            total_users = df_total.iloc[0].get('TotalUsers', 0) or 0
            total_opens = df_total.iloc[0].get('TotalOpens', 0) or 0
            st.metric("**🧑‍💻 Total Registered Users**", f"{int(total_users):,}")
            st.metric("**📱 Total App Opens**", f"{int(total_opens):,}")

        tab1, tab2, tab3 = st.tabs(["States", "Districts", "Pincodes"])

        with tab1:
            df_states = execute_query(f"""
                SELECT States, SUM(RegisteredUser) as TotalUsers 
                FROM map_user {where_clause} 
                GROUP BY States ORDER BY TotalUsers DESC LIMIT 10
            """, tuple(params))
            if not df_states.empty:
                st.markdown("#### 🏆 Top 10 States by Registered Users")
                st.dataframe(df_states, use_container_width=True)

        with tab2:
            df_districts = execute_query(f"""
                SELECT Districts, SUM(RegisteredUser) as TotalUsers 
                FROM map_user {where_clause} 
                GROUP BY Districts ORDER BY TotalUsers DESC LIMIT 10
            """, tuple(params))
            if not df_districts.empty:
                st.markdown("#### 🏆 Top 10 Districts by Registered Users")
                st.dataframe(df_districts, use_container_width=True)

        with tab3:
            df_pincodes = execute_query(f"""
                SELECT Pincodes, SUM(RegisteredUser) as TotalUsers 
                FROM top_user {where_clause} 
                GROUP BY Pincodes ORDER BY TotalUsers DESC LIMIT 10
            """, tuple(params))
            if not df_pincodes.empty:
                st.markdown("#### 🏆 Top 10 Pincodes by Registered Users")
                st.dataframe(df_pincodes, use_container_width=True)

    elif sub_tab == "Insurance":
        st.subheader("🛡 Insurance Engagement Insights")

        df_total = execute_query(f"""
            SELECT SUM(Total_count) as TotalTransactions, SUM(Total_amount) as TotalAmount
            FROM aggregated_insurance {where_clause}
        """, tuple(params))

        if not df_total.empty and len(df_total) > 0:
            total_transactions = df_total.iloc[0].get('TotalTransactions', 0) or 0
            total_amount = df_total.iloc[0].get('TotalAmount', 0) or 0

            st.metric("Total Insurance Transactions", f"{int(total_transactions):,}")
            st.metric("Total Insurance Amount (₹)", f"₹{int(total_amount):,}")
        else:
            st.metric("Total Insurance Transactions", "0")
            st.metric("Total Insurance Amount (₹)", "₹0")
            st.info("Insurance data might not be available for the selected filters")

        tab1, tab2, tab3 = st.tabs(["States", "Districts", "Pincodes"])

        with tab1:
            df_states = execute_query(f"""
                SELECT States, SUM(Total_count) as TotalTransactions
                FROM aggregated_insurance {where_clause}
                GROUP BY States ORDER BY TotalTransactions DESC LIMIT 10
            """, tuple(params))
            if not df_states.empty:
                st.markdown("#### 🏆 Top 10 States by Insurance Transactions")
                st.dataframe(df_states, use_container_width=True)
            else:
                st.info("No state-wise insurance data available")

        with tab2:
            df_districts = execute_query(f"""
                SELECT Districts, SUM(Transaction_count) as TotalTransactions
                FROM map_insurance {where_clause}
                GROUP BY Districts ORDER BY TotalTransactions DESC LIMIT 10
            """, tuple(params))
            if not df_districts.empty:
                st.markdown("#### 🏆 Top 10 Districts by Insurance Transactions")
                st.dataframe(df_districts, use_container_width=True)
            else:
                st.info("No district-wise insurance data available")

        with tab3:
            df_pincodes = execute_query(f"""
                SELECT Pincodes, SUM(Transaction_count) as TotalTransactions
                FROM top_insurance {where_clause}
                GROUP BY Pincodes ORDER BY TotalTransactions DESC LIMIT 10
            """, tuple(params))
            if not df_pincodes.empty:
                st.markdown("#### 🏆 Top 10 Pincodes by Insurance Transactions")
                st.dataframe(df_pincodes, use_container_width=True)
            else:
                st.info("No pincode-wise insurance data available")

# --- Case Study Insights ---
elif st.session_state.page == "Case Study Insights":
    st.title("📈 Case Study Insights Dashboard")

    years = ["All"] + [str(y) for y in range(2018, 2025)]
    quarters = ["All"] + list(quarter_map.keys())

    col1, col2 = st.columns(2)
    selected_year = col1.selectbox("Select Year", years, key="insight_year")
    selected_quarter = col2.selectbox("Select Quarter", quarters, key="insight_quarter")

    year = int(selected_year) if selected_year != "All" else None
    quarter = quarter_map[selected_quarter] if selected_quarter != "All" else None

    conditions = []
    params = []

    if year is not None:
        conditions.append("Years = %s")
        params.append(year)
    if quarter is not None:
        conditions.append("Quarter = %s")
        params.append(quarter)

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    case_option = st.selectbox("Select Case Study", [
        "Decoding Transaction Dynamics",
        "Device Dominance and User Engagement",
        "Insurance Penetration and Growth Potential",
        "Transaction Analysis for Market Expansion",
        "User Engagement and Growth Strategy"
    ])

    if case_option == "Decoding Transaction Dynamics":
        df_type = execute_query(f"""
            SELECT Transaction_type, SUM(Transaction_count) AS TotalCount 
            FROM aggregated_transaction 
            {where_clause} 
            GROUP BY Transaction_type
        """, tuple(params))
        if not df_type.empty:
            fig = px.bar(df_type, x="Transaction_type", y="TotalCount", 
                        title="Transactions by Type", color="Transaction_type")
            safe_plotly_chart(fig, "No transaction type data available")

        if geo is not None:
            df_map = execute_query(f"""
                SELECT States, SUM(Transaction_count) AS TotalTransactions 
                FROM map_transaction 
                {where_clause} 
                GROUP BY States
            """, tuple(params))
            if not df_map.empty:
                # FIXED: Use safe choropleth function
                fig_map = create_safe_choropleth(
                    df_map, geo, "States", "TotalTransactions",
                    "State-wise Transaction Volume", "blues"
                )
                if fig_map:
                    safe_plotly_chart(fig_map, "No geographical data available")

        df_trend = execute_query(f"""
            SELECT Years, SUM(Transaction_amount) AS Amount 
            FROM aggregated_transaction 
            {where_clause} 
            GROUP BY Years
        """, tuple(params))
        if not df_trend.empty:
            fig = px.line(df_trend, x="Years", y="Amount", markers=True, 
                         title="Transaction Trend Over Years")
            safe_plotly_chart(fig, "No trend data available")

        df_top = execute_query(f"""
            SELECT States, SUM(Transaction_count) AS TotalCount 
            FROM map_transaction 
            {where_clause} 
            GROUP BY States 
            ORDER BY TotalCount DESC LIMIT 10
        """, tuple(params))
        if not df_top.empty:
            fig = px.bar(df_top, x="States", y="TotalCount", 
                        title="Top 10 States by Transactions")
            safe_plotly_chart(fig, "No top states data available")

    elif case_option == "Device Dominance and User Engagement":
        df_users = execute_query(f"""
            SELECT Brands, SUM(Transaction_count) AS Users 
            FROM aggregate_user 
            {where_clause} 
            GROUP BY Brands
        """, tuple(params))
        if not df_users.empty:
            fig = px.bar(df_users, x="Brands", y="Users", 
                        title="Users by Device Brand")
            safe_plotly_chart(fig, "No user brand data available")

    elif case_option == "Insurance Penetration and Growth Potential":
        df_state = execute_query(f"""
            SELECT States, SUM(Total_count) AS TotalCount 
            FROM aggregated_insurance 
            {where_clause} 
            GROUP BY States
        """, tuple(params))
        
        if not df_state.empty and "TotalCount" in df_state.columns:
            fig = px.bar(df_state.sort_values(by="TotalCount", ascending=False).head(10), 
                        x="States", y="TotalCount", 
                        title="Top States by Insurance Transactions")
            safe_plotly_chart(fig, "No insurance state data available")
        else:
            st.info("No insurance data available for the selected filters")

        df_line = execute_query(f"""
            SELECT Years, SUM(Total_count) AS Count 
            FROM aggregated_insurance 
            {where_clause} 
            GROUP BY Years
        """, tuple(params))
        
        if not df_line.empty and "Count" in df_line.columns:
            fig = px.line(df_line, x="Years", y="Count", markers=True, 
                         title="Insurance Growth Over Time")
            safe_plotly_chart(fig, "No insurance trend data available")
        else:
            st.info("No insurance trend data available")

        if geo is not None:
            df_map_insurance = execute_query(f"""
                SELECT States, SUM(Transaction_count) AS TotalTransactions 
                FROM map_insurance 
                {where_clause} 
                GROUP BY States
            """, tuple(params))
            
            if not df_map_insurance.empty:
                # FIXED: Use safe choropleth function
                fig_insurance = create_safe_choropleth(
                    df_map_insurance, geo, "States", "TotalTransactions",
                    "State-wise Insurance Transactions", "purples"
                )
                if fig_insurance:
                    safe_plotly_chart(fig_insurance, "No insurance geographical data available")

    elif case_option == "Transaction Analysis for Market Expansion":
        df_amount = execute_query(f"""
            SELECT States, SUM(Transaction_amount) AS Amount 
            FROM aggregated_transaction 
            {where_clause} 
            GROUP BY States
        """, tuple(params))
        if not df_amount.empty:
            fig = px.bar(df_amount.sort_values(by="Amount", ascending=False), 
                        x="States", y="Amount", 
                        title="States by Transaction Value")
            safe_plotly_chart(fig, "No transaction amount data available")

        df_yearwise = execute_query(f"""
            SELECT Years, SUM(Transaction_amount) AS Total 
            FROM aggregated_transaction 
            {where_clause} 
            GROUP BY Years
        """, tuple(params))
        if not df_yearwise.empty:
            fig = px.scatter(df_yearwise, x="Years", y="Total", 
                           title="Transaction Value Over Years")
            safe_plotly_chart(fig, "No yearly transaction data available")

        if geo is not None:
            df_map_amt = execute_query(f"""
                SELECT States, SUM(Transaction_amount) AS TotalAmount 
                FROM map_transaction 
                {where_clause} 
                GROUP BY States
            """, tuple(params))
            if not df_map_amt.empty:
                # FIXED: Use safe choropleth function
                fig = create_safe_choropleth(
                    df_map_amt, geo, "States", "TotalAmount",
                    "State-wise Market Value Map", "greens"
                )
                if fig:
                    safe_plotly_chart(fig, "No market value data available")

    elif case_option == "User Engagement and Growth Strategy":
        df_app = execute_query(f"""
            SELECT States, SUM(AppOpens) AS Opens 
            FROM map_user 
            {where_clause} 
            GROUP BY States
        """, tuple(params))
        if not df_app.empty:
            fig = px.bar(df_app.sort_values(by="Opens", ascending=False).head(10), 
                        x="States", y="Opens", title="Top States by App Opens")
            safe_plotly_chart(fig, "No app opens data available")

        df_reg = execute_query(f"""
            SELECT Years, SUM(RegisteredUser) AS Users 
            FROM map_user 
            {where_clause} 
            GROUP BY Years
        """, tuple(params))
        if not df_reg.empty:
            fig = px.line(df_reg, x="Years", y="Users", markers=True, 
                         title="User Registrations Over Time")
            safe_plotly_chart(fig, "No user registration data available")

        df_districts = execute_query(f"""
            SELECT Districts, SUM(RegisteredUser) AS Users 
            FROM map_user 
            {where_clause} 
            GROUP BY Districts 
            ORDER BY Users DESC LIMIT 10
        """, tuple(params))
        if not df_districts.empty:
            fig = px.pie(df_districts, names="Districts", values="Users", 
                        title="Top Districts by Registrations Share")
            safe_plotly_chart(fig, "No district user data available")