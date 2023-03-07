"""
## DAG PDS Download

#### Purpose

This DAG allows the ingestion of the PDS (Planetary Data Systems) data/

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
from airflow.operators import dummy_operator, python_operator
from datetime import timedelta

DAG_ID_LEVELS = "Export_level1"

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
    description="Export Level1",
    default_args=args,
    schedule_interval="@once",
    max_active_runs=1,
    tags=["production", "export"],
    catchup=False,
) as dag:
    
    start_task = dummy_operator(task_id="Start", dag=dag)
    collections_task = dummy_operator(task_id='Get collections to download', dag=dag)
    mercury_task = dummy_operator(task_id='Retrieve collections for Mercury', dag=dag)
    venus_task = dummy_operator(task_id='Retrieve collections for Venus', dag=dag)
    mars_task = dummy_operator(task_id='Retrieve collections for Mars', dag=dag)
    moon_task = dummy_operator(task_id='Retrieve collections for Moon', dag=dag)
    notification_task = dummy_operator(task_id='Notification', dag=dag)
    stop_task = dummy_operator(task_id="Stop", dag=dag)
    
    
    start_task >> collections_task >> [mercury_task, venus_task, mars_task, moon_task] >> notification_task >> stop_task
    