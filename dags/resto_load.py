"""
## Load to RESTO

#### Purpose

This DAG allows the loading of STAC repository to RESTO.

#### Outputs

TODO

#### Owner
TODO

#### TODO
- N/A

#### BUG
- N/A
"""
import pendulum
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta

DAG_ID_LEVELS = "STAC_loading"

args = {
    "owner": "airflow",
    "start_date": pendulum.today("UTC").add(days=-2),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "schedule_interval": None,
}

with DAG(
    DAG_ID_LEVELS,
    description="Loading the STAC repository to PDSSP catalog",
    default_args=args,
    schedule_interval="@once",
    max_active_runs=1,
    tags=["production", "PDS"],
    catchup=False,
) as dag:
    
    start_task = DummyOperator(task_id="Start", dag=dag)
    has_new_data_task = DummyOperator(task_id='Has_new_data_to_load', dag=dag)  
    stac_to_resto_task = DummyOperator(task_id='Loads_STAC', dag=dag)  
    stop_task = DummyOperator(task_id="Stop", dag=dag)    
    start_task >> has_new_data_task >> stac_to_resto_task  >> stop_task