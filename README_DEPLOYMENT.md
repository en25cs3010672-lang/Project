# Deployment Guide

## Streamlit Cloud Deployment

The Electricity Consumption Analyzer is deployed on Streamlit Cloud.

### Access the Application

1. Visit [Streamlit Cloud](https://share.streamlit.io)
2. Search for "en25cs3010672-lang/Project"
3. Or use your custom URL once deployed

### How to Deploy

#### Method 1: Streamlit Cloud (Recommended)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Authenticate with your GitHub account
4. Select:
   - **Repository**: `en25cs3010672-lang/Project`
   - **Branch**: `main`
   - **File**: `electricity_analyzer.py`
5. Click **Deploy**

The app will be live in 2-3 minutes!

#### Method 2: Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run electricity_analyzer.py
```

Then open your browser to `http://localhost:8501`

### Features

- ⚡ Upload CSV files with electricity consumption data
- 📊 Analyze patterns by department and shift
- 💰 Configure custom tariff rates
- 🔍 Detect anomalies with adjustable sensitivity
- 📈 Interactive visualizations with Plotly
- 📥 Download processed data

### Data Format

Your CSV should contain:
- Date column (format: DD/MM/YYYY)
- Time column (format: HH:MM:SS)
- Power consumption columns (e.g., Global_active_power, Sub_metering_1-3)
- Optional metadata columns

### Troubleshooting

If deployment fails:
1. Ensure all dependencies in `requirements.txt` are compatible
2. Check Python version (Python 3.8+ recommended)
3. Verify CSV file format matches expected columns
4. Review Streamlit logs in deployment dashboard
