import os
import glob
import pandas as pd
import logging
from config import load_config
from validate_data import validate_dataframe

# -------- Setup logging --------
logging.basicConfig(
    filename='validation.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# -------- Load config --------
config = load_config()
csv_folder_path = config.get('csv_folder_path')

if not csv_folder_path:
    logging.error("'csv_folder_path' not found in config.")
    exit()

# -------- Find CSV files --------
csv_files = glob.glob(os.path.join(csv_folder_path, '*.csv'))

if not csv_files:
    logging.error("No CSV files found.")
    exit()

logging.info(f"Found {len(csv_files)} CSV file(s).")

# -------- Load & Validate --------
valid_dataframes = []

for file in csv_files:
    try:
        df = pd.read_csv(file)
        filename = os.path.basename(file)

        errors = validate_dataframe(df)

        if not errors:
            logging.info(f"'{filename}' passed all validations.")
            valid_dataframes.append(df)
        else:
            logging.warning(f"'{filename}' failed validation:")
            for err in errors:
                logging.warning(f" - {err}")

    except Exception as e:
        logging.error(f"Failed to read {file}: {str(e)}")

# -------- Terminal Output --------
if valid_dataframes:
    print("\n📊 Preview of valid DataFrames:")
    for i, df in enumerate(valid_dataframes, 1):
        print(f"\n✅ DataFrame {i}:")
        print(df.head())
else:
    print("⚠️ No valid CSVs loaded. Check validation.log for details.")
