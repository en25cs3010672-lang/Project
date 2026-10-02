import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Electricity Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def process_uci_format(df_raw):
    """Process the UCI Household Power Consumption dataset format"""
    try:
        # Expected UCI columns
        expected_columns = ['Date', 'Time', 'Global_active_power', 'Global_reactive_power',
                           'Voltage', 'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']

        # Create a mapping from expected to actual columns (case-insensitive, whitespace-tolerant)
        actual_cols = {col.strip(): col for col in df_raw.columns}
        col_mapping = {}

        # Find best match for each expected column
        for exp_col in expected_columns:
            exp_col_lower = exp_col.lower()
            found = False
            for actual_col, original_col in actual_cols.items():
                if actual_col.lower() == exp_col_lower:
                    col_mapping[exp_col] = original_col
                    found = True
                    break
            # If exact match not found, try substring match
            if not found:
                for actual_col, original_col in actual_cols.items():
                    if exp_col_lower in actual_col.lower():
                        col_mapping[exp_col] = original_col
                        found = True
                        break

        # Check if we have the minimum required columns
        power_cols_found = sum(1 for col in ['Global_active_power', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']
                              if col in col_mapping)
        if not ('Date' in col_mapping and 'Time' in col_mapping and power_cols_found >= 1):
            return None

        # Create a working dataframe with standardized column names
        df_work = pd.DataFrame()
        for exp_col, actual_col in col_mapping.items():
            df_work[exp_col] = df_raw[actual_col]

        # Process the data
        # Combine Date and Time into timestamp
        df_work['timestamp'] = pd.to_datetime(
            df_work['Date'] + ' ' + df_work['Time'],
            format='%d/%m/%Y %H:%M:%S',
            errors='coerce'
        )

        # Remove rows with invalid timestamps
        df_work = df_work[~df_work['timestamp'].isna()].copy()
        if len(df_work) == 0:
            return None

        # Define power columns (sub-metering as departments)
        power_columns = ['Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']

        # Melt the data to long format
        df_melted = []

        for _, row in df_work.iterrows():
            timestamp = row['timestamp']

            # Add each sub-metering as a department
            for i, col in enumerate(power_columns, 1):
                if col in df_work.columns:
                    val = row[col]
                    # Handle missing values (UCI uses '?')
                    if pd.notna(val) and str(val).strip() != '?':
                        try:
                            power_val = float(val)
                            df_melted.append({
                                'timestamp': timestamp,
                                'department': f'Sub_metering_{i}',
                                'power_kW': power_val
                            })
                        except (ValueError, TypeError):
                            continue

            # Optionally add Global_active_power as a "Total" department
            if 'Global_active_power' in df_work.columns:
                val = row['Global_active_power']
                if pd.notna(val) and str(val).strip() != '?':
                    try:
                        power_val = float(val)
                        df_melted.append({
                            'timestamp': timestamp,
                            'department': 'Total_Consumption',
                            'power_kW': power_val
                        })
                    except (ValueError, TypeError):
                        pass

        if not df_melted:
            return None

        result_df = pd.DataFrame(df_melted)
        # Sort by timestamp for consistency
        result_df = result_df.sort_values('timestamp').reset_index(drop=True)
        return result_df

    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return None

def load_sample_data():
    """Generate sample electricity consumption data"""
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='1H')
    np.random.seed(42)
    
    data = {
        'timestamp': dates,
        'department': np.random.choice(['Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3', 'Total_Consumption'], len(dates)),
        'power_kW': np.abs(np.random.normal(2.0, 0.5, len(dates)))
    }
    
    return pd.DataFrame(data)

def main():
    # Header
    st.title("⚡ Electricity Consumption Analyzer")
    st.markdown("Analyze electricity consumption patterns, detect anomalies, and visualize trends")
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Configuration")
        
        data_source = st.radio(
            "Data Source",
            ["Upload CSV", "Use Sample Data"],
            help="Choose how to load your data"
        )
        
        if data_source == "Upload CSV":
            uploaded_file = st.file_uploader(
                "Choose a CSV file",
                type="csv",
                help="Accepts CSV files with timestamp and power consumption columns"
            )
            
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.success(f"✅ File loaded: {len(df)} rows")
                    df_processed = process_uci_format(df)
                    
                    if df_processed is None:
                        df_processed = pd.DataFrame()
                        st.warning("Could not auto-detect columns. Please check your CSV format.")
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
                    df_processed = pd.DataFrame()
            else:
                df_processed = pd.DataFrame()
        else:
            df_processed = load_sample_data()
            st.info("📌 Using sample data for demonstration")
        
        # Tariff settings
        st.subheader("💰 Tariff Settings")
        base_rate = st.slider("Base Rate ($/kWh)", 0.01, 2.0, 0.15, 0.01)
        use_tod = st.checkbox("Enable Time-of-Day Rates")
        
        if use_tod:
            peak_rate = st.slider("Peak Rate ($/kWh)", 0.01, 2.0, 0.25, 0.01)
            off_peak_rate = st.slider("Off-Peak Rate ($/kWh)", 0.01, 2.0, 0.10, 0.01)
            peak_hours = st.slider("Peak Hours", 0, 23, (9, 21))
        else:
            peak_rate = base_rate
            off_peak_rate = base_rate
            peak_hours = (0, 24)
        
        # Anomaly detection settings
        st.subheader("🔍 Anomaly Detection")
        window_size = st.slider("Rolling Window (hours)", 1, 24, 3)
        z_threshold = st.slider("Z-Score Threshold", 1.0, 5.0, 2.5, 0.1)
    
    # Main content
    if not df_processed.empty:
        # Display data overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Records", len(df_processed))
        with col2:
            st.metric("Date Range", f"{df_processed['timestamp'].min().strftime('%Y-%m-%d')} to {df_processed['timestamp'].max().strftime('%Y-%m-%d')}")
        with col3:
            st.metric("Departments", df_processed['department'].nunique())
        with col4:
            st.metric("Avg Power (kW)", f"{df_processed['power_kW'].mean():.2f}")
        
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "📊 Analysis", "🔍 Anomalies", "📥 Data"])
        
        with tab1:
            st.subheader("Power Consumption Trend")
            fig = px.line(df_processed, x='timestamp', y='power_kW', color='department', 
                         title="Power Consumption Over Time")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("Consumption by Department")
            dept_summary = df_processed.groupby('department')['power_kW'].agg(['mean', 'max', 'min']).reset_index()
            st.dataframe(dept_summary, use_container_width=True)
            
            fig = px.bar(dept_summary, x='department', y='mean', title="Average Power by Department")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Anomaly Detection Results")
            st.info("Anomaly detection using z-score on rolling averages")
            # Placeholder for anomaly detection logic
            st.write("Anomaly detection would be performed here based on z-score threshold")
        
        with tab4:
            st.subheader("Data Preview")
            st.dataframe(df_processed.head(50), use_container_width=True)
            
            # Download button
            csv = df_processed.to_csv(index=False)
            st.download_button(
                label="📥 Download Processed Data",
                data=csv,
                file_name="electricity_data_processed.csv",
                mime="text/csv"
            )
    else:
        st.warning("⚠️ No data loaded. Please upload a CSV file or select sample data.")

if __name__ == "__main__":
    main()
