"""
## STAC transformation

#### Purpose

This DAG allows the transformation of extracted data from PDS to STAC repository.

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

DAG_ID_LEVELS = "STAC_transformation"

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
    description="STAC transformation from extracted PDS data to the STAC repository",
    default_args=args,
    schedule_interval="@once",
    max_active_runs=1,
    tags=["production", "PDS"],
    catchup=False,
) as dag:
    
    start_task = DummyOperator(task_id="Start", dag=dag)
    has_new_data_task = DummyOperator(task_id='Has_new_data_to_transform', dag=dag)  
    transform_catalog_task = DummyOperator(task_id='STAC_catalog_transform', dag=dag)  
    transform_item_task = DummyOperator(task_id='STAC_item_transform', dag=dag)      
    stop_task = DummyOperator(task_id="Stop", dag=dag)  
    start_task >> has_new_data_task >> transform_catalog_task >>  transform_item_task >> stop_task
    