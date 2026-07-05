
from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

from pathlib import Path
import subprocess
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

DRIFT_FILE = DATA_DIR / "drift_summary.csv"

SCRIPT_FILE = BASE_DIR / "airflow" / "scripts" / "retrain_pipeline.py"

def check_drift():

    drift = pd.read_csv(DRIFT_FILE)

    print(drift)

    if drift["DriftDetected"].sum() > 0:

        print("Data Drift Detected")

    else:

        raise Exception("No Drift Found")

def retrain_model():

    subprocess.run(

        ["python", str(SCRIPT_FILE)],

        check=True

    )

default_args = {

    "owner":"Devarsh",

    "start_date":datetime(2026,1,1)

}

with DAG(

    dag_id="online_retail_retraining",

    default_args=default_args,

    schedule="@weekly",

    catchup=False,

    tags=["Retail","MLOps"]

) as dag:

    drift = PythonOperator(

        task_id="check_drift",

        python_callable=check_drift

    )

    retrain = PythonOperator(

        task_id="retrain_model",

        python_callable=retrain_model

    )

    drift >> retrain
