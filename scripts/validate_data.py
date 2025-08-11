# validate.py

expected_schema = {
    'Date': 'int64',
    'Month': 'int64',
    'Year': 'int64',
    'Holidays_Count': 'int64',
    'Days': 'int64',
    'PM2.5': 'float64',
    'PM10': 'float64',
    'NO2': 'float64',
    'SO2': 'float64',
    'CO': 'float64',
    'Ozone': 'float64',
    'AQI': 'int64'
}

def validate_dataframe(df):
    errors = []

    missing = [col for col in expected_schema if col not in df.columns]
    if missing:
        errors.append(f"Missing columns: {missing}")

    if df.isnull().any().any():
        errors.append("Contains null values.")

    for col, expected_type in expected_schema.items():
        if col in df.columns:
            actual_type = str(df[col].dtype)
            if actual_type != expected_type:
                errors.append(
                    f"Column '{col}' has type '{actual_type}', expected '{expected_type}'"
                )

    return errors
