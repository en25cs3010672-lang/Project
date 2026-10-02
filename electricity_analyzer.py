import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import io
import csv

# Page configuration
st.set_page_config(
    page_title="⚡ Electricity Analyzer Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Futuristic CSS with glassmorphism and neon effects
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');
    
    * {
        font-family: 'Space Mono', monospace;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0e27 0%, #16213e 50%, #0f3460 100%);
        color: #00d4ff;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 14, 39, 0.95) 0%, rgba(22, 33, 62, 0.95) 100%);
        border-right: 2px solid #00d4ff;
        box-shadow: inset 0 0 20px rgba(0, 212, 255, 0.1);
    }
    
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(135deg, #00d4ff, #0099ff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 153, 255, 0.05));
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2), inset 0 0 10px rgba(0, 212, 255, 0.05);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.4), inset 0 0 15px rgba(0, 212, 255, 0.1);
        transform: translateY(-5px);
        border-color: #00ff88;
    }
    
    [data-testid="stMetricValue"] {
        color: #00ff88;
        font-size: 2rem !important;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: #00d4ff;
        font-size: 0.95rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: linear-gradient(90deg, rgba(0, 212, 255, 0.05), rgba(0, 153, 255, 0.05));
        border-bottom: 2px solid #00d4ff;
        border-radius: 10px 10px 0 0;
        padding: 0.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d4ff, #0099ff);
        border-radius: 8px;
        color: #0a0e27;
    }
    
    .stTabs [aria-selected="false"] {
        color: #00d4ff;
    }
    
    [data-testid="stFileUploadDropzone"] {
        border: 3px dashed #00d4ff;
        border-radius: 15px;
        background: rgba(0, 212, 255, 0.05);
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploadDropzone"]:hover {
        background: rgba(0, 212, 255, 0.1);
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff, #0099ff);
        color: #0a0e27;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        font-family: 'Orbitron', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00ff88, #00d4ff);
        box-shadow: 0 0 40px rgba(0, 255, 136, 0.5);
        transform: scale(1.05);
    }
    
    .stSlider {
        color: #00d4ff;
    }
    
    .stSlider [data-baseweb="slider"] {
        background: rgba(0, 212, 255, 0.1);
        border-radius: 10px;
    }
    
    .stSelectbox, .stMultiSelect, .stTextInput {
        background: rgba(0, 212, 255, 0.05) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 10px !important;
        color: #00d4ff !important;
    }
    
    .stTextArea {
        background: rgba(0, 212, 255, 0.05) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 10px !important;
        color: #00d4ff !important;
    }
    
    .stCheckbox {
        color: #00d4ff;
    }
    
    .stCheckbox > label {
        color: #00d4ff !important;
    }
    
    .stRadio > label {
        color: #00d4ff !important;
    }
    
    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 10px;
        border-left: 5px solid #00d4ff;
        background: rgba(0, 212, 255, 0.1);
    }
    
    .stDataFrame {
        border: 2px solid #00d4ff;
        border-radius: 10px;
        background: rgba(0, 212, 255, 0.05);
    }
    
    .stPlotlyChart {
        border: 2px solid #00d4ff;
        border-radius: 10px;
        padding: 1rem;
        background: rgba(0, 212, 255, 0.05);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.1);
    }
    
    .futuristic-header {
        text-align: center;
        padding: 2rem 0;
        font-size: 2.5rem;
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(135deg, #00d4ff, #0099ff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
    }
    
    .subheader {
        font-family: 'Orbitron', sans-serif;
        color: #00ff88;
        border-bottom: 2px solid #00d4ff;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    
    .stat-box {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(0, 153, 255, 0.08));
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.25);
        backdrop-filter: blur(10px);
    }
    
    .neon-divider {
        border-top: 2px solid #00d4ff;
        margin: 2rem 0;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    </style>
""", unsafe_allow_html=True)


def detect_separator(text):
    """Try to detect the CSV delimiter."""
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=',;\t|')
        return dialect.delimiter
    except Exception:
        if ';' in sample and ',' not in sample:
            return ';'
        if '\t' in sample and ',' not in sample:
            return '\t'
        return ','


def normalize_dataframe(df):
    """Normalize imported table to the app's expected columns."""
    if df is None or df.empty:
        return None

    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]

    col_map = {str(col).strip().lower(): col for col in df.columns}
    timestamp_col = None
    for name in ['timestamp', 'datetime', 'date', 'time', 'ts', 'date_time']:
        if name in col_map:
            timestamp_col = col_map[name]
            break

    if timestamp_col is None:
        st.error(f"❌ No timestamp column found. Available columns: {list(df.columns)}")
        return None

    df = df.rename(columns={timestamp_col: 'timestamp'})
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp']).copy()
    if df.empty:
        st.error("❌ No valid timestamps found in data")
        return None

    power_candidates = ['power_kw', 'power_kW', 'power', 'consumption_kw', 'consumption', 'value']
    power_col = None
    for candidate in power_candidates:
        if candidate.lower() in col_map:
            power_col = col_map[candidate.lower()]
            break
    if power_col is None:
        st.error(f"❌ No power column found. Available columns: {list(df.columns)}")
        return None

    df = df.rename(columns={power_col: 'power_kW'})

    if 'department' not in df.columns:
        df['department'] = 'Total_Consumption'

    # Keep only the data the app uses
    df = df[['timestamp', 'department', 'power_kW']].copy()
    return df


def process_uci_format(df_raw):
    """Process the UCI Household Power Consumption dataset format"""
    try:
        expected_columns = ['Date', 'Time', 'Global_active_power', 'Global_reactive_power',
                           'Voltage', 'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']

        actual_cols = {col.strip(): col for col in df_raw.columns}
        col_mapping = {}

        for exp_col in expected_columns:
            exp_col_lower = exp_col.lower()
            found = False
            for actual_col, original_col in actual_cols.items():
                if actual_col.lower() == exp_col_lower:
                    col_mapping[exp_col] = original_col
                    found = True
                    break
            if not found:
                for actual_col, original_col in actual_cols.items():
                    if exp_col_lower in actual_col.lower():
                        col_mapping[exp_col] = original_col
                        found = True
                        break

        power_cols_found = sum(1 for col in ['Global_active_power', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']
                              if col in col_mapping)
        if not ('Date' in col_mapping and 'Time' in col_mapping and power_cols_found >= 1):
            return None

        df_work = pd.DataFrame()
        for exp_col, actual_col in col_mapping.items():
            df_work[exp_col] = df_raw[actual_col]

        df_work['timestamp'] = pd.to_datetime(
            df_work['Date'] + ' ' + df_work['Time'],
            format='%d/%m/%Y %H:%M:%S',
            errors='coerce'
        )

        df_work = df_work[~df_work['timestamp'].isna()].copy()
        if len(df_work) == 0:
            return None

        power_columns = ['Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']
        df_melted = []

        for _, row in df_work.iterrows():
            timestamp = row['timestamp']

            for i, col in enumerate(power_columns, 1):
                if col in df_work.columns:
                    val = row[col]
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
        result_df = result_df.sort_values('timestamp').reset_index(drop=True)
        return result_df

    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return None


def parse_text_input(text_input):
    """Parse electricity data from pasted text or CSV content."""
    try:
        text = str(text_input).strip()
        if not text:
            return None

        sep = detect_separator(text)
        df = pd.read_csv(io.StringIO(text), sep=sep, engine='python')
        return normalize_dataframe(df)
    except Exception as e:
        st.error(f"❌ Error parsing text input: {str(e)}")
        return None


def parse_text_file(uploaded_file):
    """Parse electricity data from uploaded text file (.txt)"""
    try:
        raw_text = uploaded_file.read().decode('utf-8', errors='replace').strip()
        if not raw_text:
            st.error("❌ File is empty")
            return None

        sep = detect_separator(raw_text)
        df = pd.read_csv(io.StringIO(raw_text), sep=sep, engine='python')
        return normalize_dataframe(df)
    except Exception as e:
        st.error(f"❌ Error parsing text file: {str(e)}")
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


def calculate_anomalies(df, window_size, z_threshold):
    """Calculate anomalies using z-score"""
    try:
        df_sorted = df.sort_values('timestamp').copy()
        df_sorted['rolling_mean'] = df_sorted['power_kW'].rolling(window=window_size, min_periods=1).mean()
        df_sorted['rolling_std'] = df_sorted['power_kW'].rolling(window=window_size, min_periods=1).std()
        
        df_sorted['z_score'] = (df_sorted['power_kW'] - df_sorted['rolling_mean']) / (df_sorted['rolling_std'] + 1e-8)
        df_sorted['is_anomaly'] = abs(df_sorted['z_score']) > z_threshold
        
        return df_sorted
    except Exception as e:
        st.error(f"Error calculating anomalies: {str(e)}")
        return df


def main():
    # Initialize df_processed in session state
    if 'df_processed' not in st.session_state:
        st.session_state.df_processed = pd.DataFrame()
    
    # Header
    st.markdown('<div class="futuristic-header">⚡ ELECTRICITY ANALYZER PRO</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #00d4ff; font-size: 1.1rem;">Advanced Analytics & Anomaly Detection System</p>', 
                unsafe_allow_html=True)
    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="subheader">📊 DATA SOURCE</div>', unsafe_allow_html=True)
        
        data_source = st.radio(
            "Select Input Method:",
            ["📤 Upload CSV", "📄 Upload Text File", "📝 Text Input", "🎲 Sample Data"],
            help="Choose your data source"
        )
        
        if data_source == "📤 Upload CSV":
            st.markdown('<div class="subheader">CSV Upload</div>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Drop your CSV file here or click to browse",
                type="csv",
                help="Supports standard CSV format with timestamp and power columns"
            )
            
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.success(f"✅ File loaded: {len(df)} rows")
                    df_result = process_uci_format(df)
                    
                    if df_result is not None:
                        st.session_state.df_processed = df_result
                    else:
                        st.warning("⚠️ Could not auto-detect columns. Check your CSV format.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        elif data_source == "📄 Upload Text File":
            st.markdown('<div class="subheader">Text File Upload</div>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Drop your text file here or click to browse",
                type="txt",
                help="Upload a .txt file containing CSV-formatted data"
            )
            
            if uploaded_file is not None:
                df_result = parse_text_file(uploaded_file)
                if df_result is not None:
                    st.success(f"✅ Text file loaded: {len(df_result)} rows")
                    st.session_state.df_processed = df_result
        
        elif data_source == "📝 Text Input":
            st.markdown('<div class="subheader">Text Input</div>', unsafe_allow_html=True)
            text_input = st.text_area(
                "Paste CSV data here:",
                height=150,
                placeholder="datetime,department,power_kW\n2023-01-01 00:00,Sub_metering_1,1.5\n2023-01-01 01:00,Sub_metering_2,2.3\n...",
                help="Enter data in CSV format with columns: timestamp, department, power_kW"
            )
            
            if st.button("🔄 Parse Text Data"):
                if text_input.strip():
                    df_result = parse_text_input(text_input)
                    if df_result is not None:
                        st.success(f"✅ Parsed {len(df_result)} rows successfully!")
                        st.session_state.df_processed = df_result
                else:
                    st.warning("⚠️ Please enter some data")
        
        else:  # Sample Data
            st.session_state.df_processed = load_sample_data()
            st.success("✅ Sample data loaded for demonstration")
        
        # Tariff settings
        st.markdown('<div class="subheader">💰 TARIFF SETTINGS</div>', unsafe_allow_html=True)
        base_rate = st.slider("Base Rate ($/kWh)", 0.01, 2.0, 0.15, 0.01)
        use_tod = st.checkbox("⏰ Enable Time-of-Day Rates", value=False)
        
        if use_tod:
            peak_rate = st.slider("Peak Rate ($/kWh)", 0.01, 2.0, 0.25, 0.01)
            off_peak_rate = st.slider("Off-Peak Rate ($/kWh)", 0.01, 2.0, 0.10, 0.01)
            peak_hours = st.slider("Peak Hours", 0, 23, (9, 21))
        else:
            peak_rate = base_rate
            off_peak_rate = base_rate
            peak_hours = (0, 24)
        
        # Anomaly detection settings
        st.markdown('<div class="subheader">🔍 ANOMALY DETECTION</div>', unsafe_allow_html=True)
        window_size = st.slider("Rolling Window (hours)", 1, 24, 3)
        z_threshold = st.slider("Z-Score Threshold", 1.0, 5.0, 2.5, 0.1)
    
    # Main content
    df_processed = st.session_state.df_processed
    
    if not df_processed.empty:
        st.markdown('<div class="subheader">📈 DATA OVERVIEW</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total Records", len(df_processed), delta="+100%")
        with col2:
            date_range = f"{df_processed['timestamp'].min().strftime('%Y-%m-%d')} → {df_processed['timestamp'].max().strftime('%Y-%m-%d')}"
            st.metric("📅 Date Range", date_range)
        with col3:
            st.metric("🏢 Departments", df_processed['department'].nunique())
        with col4:
            st.metric("⚡ Avg Power (kW)", f"{df_processed['power_kW'].mean():.2f}", delta=f"{df_processed['power_kW'].std():.2f} σ")
        
        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Trends", "📊 Analysis", "🔍 Anomalies", "💾 Data Export", "⚙️ Stats"])
        
        with tab1:
            st.markdown('<div class="subheader">Power Consumption Timeline</div>', unsafe_allow_html=True)
            fig = px.line(
                df_processed, 
                x='timestamp', 
                y='power_kW', 
                color='department',
                title="⚡ Power Consumption Over Time",
                labels={'power_kW': 'Power (kW)', 'timestamp': 'Date/Time'},
                template='plotly_dark'
            )
            fig.update_layout(
                hovermode='x unified',
                plot_bgcolor='rgba(0,20,40,0.5)',
                paper_bgcolor='rgba(10,14,39,0.8)',
                font=dict(color='#00d4ff'),
                title_font=dict(size=20, color='#00ff88')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown('<div class="subheader">Consumption Analysis</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                dept_summary = df_processed.groupby('department')['power_kW'].agg(['mean', 'max', 'min']).reset_index()
                st.markdown('<p style="color: #00ff88; font-weight: bold;">By Department</p>', unsafe_allow_html=True)
                st.dataframe(dept_summary.style.highlight_max(subset=['mean'], color='#00ff88'), use_container_width=True)
                
                fig = px.bar(
                    dept_summary, 
                    x='department', 
                    y='mean', 
                    title="Average Power by Department",
                    template='plotly_dark',
                    labels={'mean': 'Avg Power (kW)'}
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,20,40,0.5)',
                    paper_bgcolor='rgba(10,14,39,0.8)',
                    font=dict(color='#00d4ff'),
                    title_font=dict(size=16, color='#00ff88')
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                df_hourly = df_processed.copy()
                df_hourly['hour'] = df_hourly['timestamp'].dt.hour
                hourly_avg = df_hourly.groupby('hour')['power_kW'].mean()
                
                fig_hourly = px.bar(
                    x=hourly_avg.index,
                    y=hourly_avg.values,
                    title="Average Consumption by Hour",
                    labels={'x': 'Hour of Day', 'y': 'Avg Power (kW)'},
                    template='plotly_dark'
                )
                fig_hourly.update_layout(
                    plot_bgcolor='rgba(0,20,40,0.5)',
                    paper_bgcolor='rgba(10,14,39,0.8)',
                    font=dict(color='#00d4ff'),
                    title_font=dict(size=16, color='#00ff88')
                )
                st.plotly_chart(fig_hourly, use_container_width=True)
        
        with tab3:
            st.markdown('<div class="subheader">Anomaly Detection Results</div>', unsafe_allow_html=True)
            df_anomalies = calculate_anomalies(df_processed, window_size, z_threshold)
            anomaly_count = df_anomalies['is_anomaly'].sum()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🚨 Anomalies Found", anomaly_count, delta=f"{(anomaly_count/len(df_anomalies)*100):.2f}%")
            with col2:
                st.metric("✅ Normal Points", len(df_anomalies) - anomaly_count)
            
            if anomaly_count > 0:
                fig_anomaly = px.scatter(
                    df_anomalies,
                    x='timestamp',
                    y='power_kW',
                    color='is_anomaly',
                    title="Anomaly Detection Visualization",
                    labels={'power_kW': 'Power (kW)', 'is_anomaly': 'Anomaly'},
                    color_discrete_map={True: '#ff0055', False: '#00d4ff'},
                    template='plotly_dark'
                )
                fig_anomaly.update_layout(
                    plot_bgcolor='rgba(0,20,40,0.5)',
                    paper_bgcolor='rgba(10,14,39,0.8)',
                    font=dict(color='#00d4ff'),
                    title_font=dict(size=16, color='#00ff88')
                )
                st.plotly_chart(fig_anomaly, use_container_width=True)
                
                anomalies_df = df_anomalies[df_anomalies['is_anomaly']][['timestamp', 'department', 'power_kW', 'z_score']].head(20)
                st.markdown('<p style="color: #ff0055; font-weight: bold;">⚠️ Top 20 Anomalies</p>', unsafe_allow_html=True)
                st.dataframe(anomalies_df, use_container_width=True)
            else:
                st.success("✅ No anomalies detected - all data points are within normal range!")
        
        with tab4:
            st.markdown('<div class="subheader">Data Export</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df_processed.to_csv(index=False)
                st.download_button(
                    label="📥 Download Processed Data (CSV)",
                    data=csv,
                    file_name=f"electricity_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                from io import BytesIO
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_processed.to_excel(writer, sheet_name='Data', index=False)
                output.seek(0)
                st.download_button(
                    label="📊 Download as Excel",
                    data=output.getvalue(),
                    file_name=f"electricity_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.ms-excel"
                )
            
            st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
            st.markdown('<p style="color: #00ff88; font-weight: bold;">Preview (First 50 Rows)</p>', unsafe_allow_html=True)
            st.dataframe(df_processed.head(50), use_container_width=True)
        
        with tab5:
            st.markdown('<div class="subheader">Statistical Summary</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<p style="color: #00ff88; font-weight: bold;">Overall Statistics</p>', unsafe_allow_html=True)
                stats_dict = {
                    'Mean': f"{df_processed['power_kW'].mean():.4f}",
                    'Median': f"{df_processed['power_kW'].median():.4f}",
                    'Std Dev': f"{df_processed['power_kW'].std():.4f}",
                    'Min': f"{df_processed['power_kW'].min():.4f}",
                    'Max': f"{df_processed['power_kW'].max():.4f}",
                    '25th %ile': f"{df_processed['power_kW'].quantile(0.25):.4f}",
                    '75th %ile': f"{df_processed['power_kW'].quantile(0.75):.4f}"
                }
                
                for label, value in stats_dict.items():
                    st.markdown(f'<div class="stat-box"><span style="color: #00ff88;">{label}</span>: <span style="color: #00d4ff; font-size: 1.2rem;">{value}</span></div>', 
                               unsafe_allow_html=True)
            
            with col2:
                fig_dist = px.histogram(
                    df_processed,
                    x='power_kW',
                    nbins=50,
                    title="Power Consumption Distribution",
                    labels={'power_kW': 'Power (kW)'},
                    template='plotly_dark'
                )
                fig_dist.update_layout(
                    plot_bgcolor='rgba(0,20,40,0.5)',
                    paper_bgcolor='rgba(10,14,39,0.8)',
                    font=dict(color='#00d4ff'),
                    title_font=dict(size=16, color='#00ff88')
                )
                st.plotly_chart(fig_dist, use_container_width=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
                <p style="color: #ff0055; font-size: 1.3rem; font-weight: bold;">NO DATA LOADED</p>
                <p style="color: #00d4ff;">Please select a data source from the sidebar to begin analysis</p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
