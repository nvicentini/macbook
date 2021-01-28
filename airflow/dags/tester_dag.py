"""Datos diarios dag."""


from datetime import datetime
from pathlib import Path

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

import datos_diarios as dd
import json_reader as jr

STORE_DIR = Path(__file__).resolve().parent / 'tmp-files' / 'random-num'
Path.mkdir(STORE_DIR, exist_ok=True, parents=True)



default_args = {'owner': 'Nico', 'retries': 0, 'start_date': datetime(2021, 1, 1)}
with DAG(
    'random_number', default_args=default_args, schedule_interval='0 0 * * *'
) as dag:
    descarga_datos_diarios = PythonOperator(
        task_id='descarga_datos_diarios',
        python_callable=dd.request_diario,
        op_args=[STORE_DIR],
    )
    crear_csv = PythonOperator(
        task_id='crear_csv',
        python_callable=jr.crear_csv,
        op_args=[STORE_DIR],
    )

    descarga_datos_diarios >> crear_csv