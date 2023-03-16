import pendulum
from datetime import timedelta
from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.dummy_operator import DummyOperator

DOC_PDS_COLL = """
## Workflow Name: PDS_Extraction

### Description
This workflow extracts PDS data for the following solar bodies: Mercury, Venus, Moon, Mars

### Operators
* start_task: A dummy operator that serves as the start of the workflow.
* trigger_mercury_coll_dag: Trigger the Mercury_PDS_collection_list DAG.
* trigger_venus_coll_dag: Trigger the Venus_PDS_collection_list DAG.
* trigger_moon_coll_dag: Trigger the Moon_PDS_collection_list DAG.
* trigger_mars_coll_dag: Trigger the Mars_PDS_collection_list DAG.
* trigger_mercury_extraction_dag: Trigger Mercury_extraction DAG.
* trigger_venus_extraction_dag: Trigger Venus_extraction DAG.
* trigger_moon_extraction_dag: Trigger Moon_extraction DAG.
* trigger_mars_extraction_dag: Trigger Mars_extraction DAG.
* stop_task: A dummy operator that serves as the stop of the workflow.

### DAG Settings
* dag_id: The ID of the DAG.
* description: A brief description of the DAG.
* default_args: The default arguments for the DAG.
* max_active_runs: The maximum number of active DAG runs.
* tags: The tags for the DAG.
* schedule_interval: The interval at which to schedule the DAG.
* catchup: Whether to backfill past DAG runs.
* is_paused_upon_creation: Start at creation
"""

args = {
    "owner": "pdssp-crawler",
    "start_date": pendulum.datetime(2023, 1, 1, tz='Europe/Paris'),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=30),
}

with DAG(
    "PDS_Extraction",
    description=f"Extraction of Planetary Data System (PDS)",
    default_args=args,
    max_active_runs=1,
    tags=["production", "PDS", "General_workflow"],
    schedule_interval="@monthly",            
    catchup=False,
    is_paused_upon_creation=False
) as dag: 
    dag.doc_md = DOC_PDS_COLL
    
    start_task = DummyOperator(task_id="Start")
    
    with TaskGroup(group_id="Mercury") as task_gp_mercury:
        trigger_mercury_coll_dag = TriggerDagRunOperator(
            task_id='trigger_mercury_pds_collection_list',
            trigger_dag_id='Mercury_PDS_collection_list',
            wait_for_completion=True,
            dag=dag
        )  
        trigger_mercury_extraction_dag = TriggerDagRunOperator(
            task_id='trigger_mercury_extraction',
            trigger_dag_id='Mercury_extraction',
            wait_for_completion=True,
            dag=dag
        ) 
        
        trigger_mercury_coll_dag >> trigger_mercury_extraction_dag            
    
    with TaskGroup(group_id="Venus") as task_gp_venus:
        trigger_venus_coll_dag = TriggerDagRunOperator(
            task_id='trigger_venus_pds_collection_list',
            trigger_dag_id='Venus_PDS_collection_list',
            wait_for_completion=True,
            dag=dag
        )  
        trigger_venus_extraction_dag = TriggerDagRunOperator(
            task_id='trigger_venus_extraction',
            trigger_dag_id='Venus_extraction',
            wait_for_completion=True,
            dag=dag
        ) 
        
        trigger_venus_coll_dag >> trigger_venus_extraction_dag    
    
    with TaskGroup(group_id="Moon") as task_gp_moon:
        trigger_moon_coll_dag = TriggerDagRunOperator(
            task_id='trigger_moon_pds_collection_list',
            trigger_dag_id='Moon_PDS_collection_list',
            wait_for_completion=True,
            dag=dag
        )  
        trigger_moon_extraction_dag = TriggerDagRunOperator(
            task_id='trigger_moon_extraction',
            trigger_dag_id='Moon_extraction',
            wait_for_completion=True,
            dag=dag
        ) 
        
        trigger_moon_coll_dag >> trigger_moon_extraction_dag         
    
    with TaskGroup(group_id="Mars") as task_gp_mars:
        trigger_mars_coll_dag = TriggerDagRunOperator(
            task_id='trigger_mars_pds_collection_list',
            trigger_dag_id='Mars_PDS_collection_list',
            wait_for_completion=True,
            dag=dag
        )  
        trigger_mars_extraction_dag = TriggerDagRunOperator(
            task_id='trigger_mars_extraction',
            trigger_dag_id='Mars_extraction',
            wait_for_completion=True,
            dag=dag
        ) 
        
        trigger_mars_coll_dag >> trigger_mars_extraction_dag             
    

    stop_task = DummyOperator(task_id="Stop")    
    
    start_task >> [task_gp_mercury, task_gp_venus, task_gp_moon, task_gp_mars] >> stop_task
    
  
DOC_TRANS = """
## Workflow Name: PDS_Transformation

### Description
This workflow transforms the downloaded data to STAC for Mercury, Venus, Moon, Mars

### Operators
* start_task: A dummy operator that serves as the start of the workflow.
* trigger_mercury_extraction_dag: Trigger the Mercury_transformation DAG.
* trigger_venus_extraction_dag: Trigger the Venus_transformation DAG.
* trigger_moon_extraction_dag: Trigger the Moon_transformation DAG.
* trigger_mars_extraction_dag: Trigger the Mars_transformation DAG.
* stop_task: A dummy operator that serves as the stop of the workflow.

### DAG Settings
* dag_id: The ID of the DAG.
* description: A brief description of the DAG.
* default_args: The default arguments for the DAG.
* max_active_runs: The maximum number of active DAG runs.
* tags: The tags for the DAG.
* schedule_interval: The interval at which to schedule the DAG.
* catchup: Whether to backfill past DAG runs.
* is_paused_upon_creation: Start at creation
"""    
with DAG(
    "PDS_Transformation",
    description=f"Transformation of Planetary Data System (PDS)",
    default_args=args,
    max_active_runs=1,
    tags=["production", "PDS", "General_workflow"],
    schedule_interval="@monthly",            
    catchup=False,
    is_paused_upon_creation=False
) as dag: 
    dag.doc_md = DOC_TRANS
    start_task = DummyOperator(task_id="Start")
    
    trigger_mercury_transformation_dag = TriggerDagRunOperator(
        task_id='trigger_mercury_transformation',
        trigger_dag_id='Mercury_transformation',
        wait_for_completion=True,
        dag=dag
    )  
    
    trigger_venus_transformation_dag = TriggerDagRunOperator(
        task_id='trigger_venus_transformation',
        trigger_dag_id='Venus_transformation',
        wait_for_completion=True,
        dag=dag
    ) 
    
    trigger_moon_transformation_dag = TriggerDagRunOperator(
        task_id='trigger_moon_transformation',
        trigger_dag_id='Moon_transformation',
        wait_for_completion=True,
        dag=dag
    )       
    
    trigger_mars_transformation_dag = TriggerDagRunOperator(
        task_id='trigger_mars_transformation',
        trigger_dag_id='Mars_transformation',
        wait_for_completion=True,
        dag=dag
    )          
                
    stop_task = DummyOperator(task_id="Stop")    
    
    start_task >> [trigger_mercury_transformation_dag, trigger_venus_transformation_dag, trigger_moon_transformation_dag, trigger_mars_transformation_dag] >> stop_task    