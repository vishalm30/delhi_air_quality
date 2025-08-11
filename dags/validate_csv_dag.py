from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import glob
import sys
import shutil

# sys.path.append('../scripts/config.py')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from config import load_config 

config = load_config()
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

CSV_FOLDER = os.path.join(BASE_DIR, config.get('csv_folder_path'))
INVALID_FOLDER = os.path.join(BASE_DIR, config.get('invalid_folder_path'))

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'csv_file_validation_pipeline',
    default_args=default_args,
    description='Validate CSV files and delete invalid files',
    schedule_interval='*/2 * * * *', 
    catchup=False
)


def move_non_csv_to_invalid():
    os.makedirs(INVALID_FOLDER, exist_ok=True)

    files = glob.glob(os.path.join(CSV_FOLDER, '*'))
    for file in files:
        if not file.endswith('.csv'):
            filename = os.path.basename(file)
            dest = os.path.join(INVALID_FOLDER, filename)
            shutil.move(file, dest)
            print(f"Moved non-CSV file to invalid folder: {filename}")

def run_validation_pipeline():
    os.system(
        'source ../env/bin/activate && '
        'python3 ../scripts/load_and_validate.py'
    )


move_task = PythonOperator(
    task_id='move_non_csv_to_invalid',
    python_callable=move_non_csv_to_invalid,
    dag=dag,
)

validate_task = PythonOperator(
    task_id='run_validation_pipeline',
    python_callable=run_validation_pipeline,
    dag=dag,
)

move_task >> validate_task
