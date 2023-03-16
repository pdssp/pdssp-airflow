"""
## Workflow Name: Installation

### Description
Its purpose is to set some variables for the Airflow environment. It is useful as a starting point
for initializing a new Airflow environment or for setting up some common variables used by other DAGs 
in the environment.
"""
import pendulum

from airflow import DAG
from airflow import settings
from airflow.api.common.mark_tasks import (
    set_dag_run_state_to_success,
)
from airflow.models.variable import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": pendulum.today("UTC").add(days=-2),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
}


def install_variables():
    Variable.set(
        "pds_database",
        "/opt/airflow/database",
        "PDS_crawler_database",
    )
    Variable.set(
        "nb_workers",
        "3",
        "Number of parallel workers per solar body",
    )  
    
    Variable.set(
        "sleep_time",
        "2",
        "sleep time in seconds between 2 sets of parallel downloads",
    )       

def pause_dag(**kwargs):
    from airflow.models import TaskInstance
    from airflow.models import DagModel

    task_instance: TaskInstance = kwargs["ti"]

    session = settings.Session()
    try:
        qry = session.query(DagModel).filter(
            DagModel.dag_id == task_instance.dag_id
        )
        d = qry.first()
        d.is_paused = True
        set_dag_run_state_to_success(
            kwargs["dag"], kwargs["logical_date"], True, session
        )
        session.commit()
    except:  # noqa:E722
        session.rollback()
    finally:
        session.close()


dag = DAG(
    "Installation",
    description="Install the needed variables.",
    default_args=default_args,
    schedule_interval="@once",
    is_paused_upon_creation=False
)


with dag:

    dag.doc = __doc__

    create_variables = PythonOperator(
        task_id="create_variables",
        python_callable=install_variables,
    )

    pause = PythonOperator(
        task_id="pause_dag",
        python_callable=pause_dag,
    )

    (
        create_variables
        >> pause
    )
