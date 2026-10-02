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
        # We need at least Date, Time, and one power column to be useful
        required_cols = ['Date', 'Time', 'Global_active_power', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']
        # Check if we have Date, Time, and at least one of the power columns
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
        # Log the error for debugging (in a real app, you might use st.exception or logging)
        # For now, just return None to fall back to standard CSV reading
        return None