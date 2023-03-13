import pendulum
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.edgemodifier import Label

from datetime import timedelta
from pds_plugin.operators import PdsBranchOperator, PdsCollExtractOperator, PdsDescExtractOperator, PdsObsExtractOperator, PdsCacheBranchOperator, StacCatalogTranformOperator, StacItemTranformOperator

from string import Template

class BodyExtractionGeneratorDag:
    
    DOC_LIST_COLL = Template("""
## Workflow Name: $dag_id

### Description
This workflow extracts the list of PDS (Planetary Data System) collections 
for a specified body. It checks for new data in the PDS database and if any 
new data is found, it extracts the list of collections for the specified body. 
The list of collections is then passed on to downstream tasks for further 
processing. This workflow is useful for indexing PDS data for a given planetary body.

### Parameters
* dag_id: The ID of the DAG (Directed Acyclic Graph) for this workflow.
* body: The name of the planetary body for which to extract the list of PDS collections.
* args: The default arguments for the DAG.
* schedule_interval: The interval at which to schedule the DAG.
* database: The name of the PDS database.
* nb_workers: The number of workers to use for the PdsCollExtractOperator task.
* time_sleep: The amount of time to sleep between collection extraction tasks.

### Operators
* start_task: A dummy operator that serves as the start of the workflow.
* has_new_data_task_in_pds: A custom operator that checks for new data in the PDS database for the specified body. If new data is found, it triggers the collections_task, otherwise it triggers the stop_task.
* collections_task: A custom operator that extracts the list of PDS collections for the specified body.
* notification_task: A dummy operator that serves as a notification for downstream tasks.
* stop_task: A dummy operator that serves as the end of the workflow.

### Workflow Steps
1. The start_task is triggered to begin the workflow.
2. The has_new_data_task_in_pds operator checks for new data in the PDS database for the specified body. If new data is found, it triggers the collections_task, otherwise it triggers the stop_task.
3. The collections_task operator extracts the list of PDS collections for the specified body. The number of workers and sleep time are configurable.
4. The notification_task is triggered to notify downstream tasks that the collection extraction is complete.
4. The stop_task is triggered to end the workflow.

### DAG Settings
* dag_id: The ID of the DAG.
* description: A brief description of the DAG.
* default_args: The default arguments for the DAG.
* max_active_runs: The maximum number of active DAG runs.
* tags: The tags for the DAG.
* schedule_interval: The interval at which to schedule the DAG.
* catchup: Whether to backfill past DAG runs.
    """)
    
    DOC_DATA = Template("""
## Workflow Name: $dag_id

### Description
Extraction of PDS data from both ODE webservice and ODE DataSetExplorer for $body

### Parameters
* dag_id: The ID of the DAG (Directed Acyclic Graph) for this workflow.
* body: The name of the planetary body for which to extract the list of PDS collections.
* args: The default arguments for the DAG.
* schedule_interval: The interval at which to schedule the DAG.
* database: The name of the PDS database.
* nb_workers: The number of workers to use for the PdsCollExtractOperator task.
* time_sleep: The amount of time to sleep between collection extraction tasks.

### Operators
1. Start: This is a dummy task that marks the start of the DAG.
2. catalog_description_extraction: This task extracts catalog descriptions for the PDS data from the ODE webservice.
3. sample_observation_extraction: This task extracts a sample of the PDS observations from the ODE DataSetExplorer.
4. observation_extraction: This task extracts all the PDS observations from the ODE DataSetExplorer.
5. Notification: This is a dummy task that marks the completion of the data extraction process.
6. Stop: This is a dummy task that marks the end of the DAG.

### DAG Settings
* dag_id: The ID of the DAG.
* description: A brief description of the DAG.
* default_args: The default arguments for the DAG.
* max_active_runs: The maximum number of active DAG runs.
* tags: The tags for the DAG.
* schedule_interval: The interval at which to schedule the DAG.
* catchup: Whether to backfill past DAG runs.
    """)
    
    @staticmethod
    def generate_list_collections_extraction(dag_id, body: str, database: str, schedule_interval: str ="@monthly", retries: int = 2, retry_delay: timedelta = timedelta(hours=1), *args, **kwargs):
        args = {
            "owner": "pdssp-crawler",
            "start_date": pendulum.datetime(2023, 1, 1, tz='Europe/Paris'),
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
            "retries": retries,
            "retry_delay": retry_delay,
        }

        with DAG(
            dag_id,
            description=f"Extraction of the list of PDS collections for the body {body}",
            default_args=args,
            max_active_runs=1,
            tags=["production", "PDS", "indexing", body],
            schedule_interval=schedule_interval,            
            catchup=False,
        ) as dag:    
            dag.doc_md = BodyExtractionGeneratorDag.DOC_LIST_COLL.substitute(dag_id = dag_id)
            start_task = DummyOperator(task_id="Start")
            has_new_data_task_in_pds = PdsBranchOperator(task_id='Has_new_data_in_pds', database=database, body=body, next="pds_list_collection", otherwise="Stop")
            collections_task = PdsCollExtractOperator(task_id="pds_list_collection", database=database, body=body)    
            collections_task.nb_workers = int(kwargs.get("nb_workers", "3"))
            collections_task.time_sleep = int(kwargs.get("time_sleep", "2"))            
            notification_task = DummyOperator(task_id='Notification')
            stop_task = DummyOperator(task_id="Stop")   
            start_task >> has_new_data_task_in_pds
            has_new_data_task_in_pds >> Label("New data was found in PDS") >> collections_task >> notification_task >> stop_task
            has_new_data_task_in_pds >> Label("No new data was found") >> stop_task
            
    @staticmethod
    def generate_data_extraction(dag_id, body: str, database: str, schedule_interval: str = None, retries: int = 2, retry_delay: timedelta = timedelta(hours=1), nb_records_per_page: int = 5000, *args, **kwargs):
        args = {
            "owner": "pdssp-crawler",
            "start_date": pendulum.datetime(2023, 1, 1, tz='Europe/Paris'),
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
            "retries": retries,
            "retry_delay": retry_delay,
        }

        with DAG(
            dag_id,
            description=f"Extraction of PDS data from both ODE webservice and ODE DataSetExplorer for the body {body}",
            default_args=args,
            max_active_runs=1,
            tags=["production", "PDS", "extraction", body],
            schedule_interval=schedule_interval,            
            catchup=False,
        ) as dag:  
            dag.doc_md = BodyExtractionGeneratorDag.DOC_DATA.substitute(dag_id = dag_id, body = body)          
            start_task = DummyOperator(task_id="Start")
            catalog_task = PdsDescExtractOperator(task_id='catalog_description_extraction', database=database, body=body)
            items_sample_task = PdsObsExtractOperator(task_id='sample_observation_extraction', database=database, body=body)
            items_sample_task.nb_workers = int(kwargs.get("nb_workers", "3"))
            items_sample_task.time_sleep = int(kwargs.get("time_sleep", "2"))            
            items_sample_task.is_sample = True
            items_sample_task.nb_records_per_page = nb_records_per_page
            items_task = PdsObsExtractOperator(task_id='observation_extraction', database=database, body=body)
            items_task.nb_records_per_page = nb_records_per_page
            items_task.nb_workers = int(kwargs.get("nb_workers", "3"))
            items_task.time_sleep = int(kwargs.get("time_sleep", "2"))            
            notification_task = DummyOperator(task_id='Notification')
            stop_task = DummyOperator(task_id="Stop")   
            start_task >> items_sample_task >> [items_task, catalog_task] >> notification_task >> stop_task        
            
class BodyTransformationGeneratorDag:      
    DOC_STAC = Template("""
## Workflow Name: $dag_id

### Description
STAC transformation of PDS collections for $body

### Parameters
* dag_id: The ID of the DAG (Directed Acyclic Graph) for this workflow.
* body: The name of the planetary body for which to transform data to STAC.
* args: The default arguments for the DAG.
* schedule_interval: The interval at which to schedule the DAG.
* database: The name of the PDS database.

### Operators
1. Start: This is a dummy task that marks the start of the DAG.
5. Notification: This is a dummy task that marks the completion of the data extraction process.
6. Stop: This is a dummy task that marks the end of the DAG.

### DAG Settings
* dag_id: The ID of the DAG.
* description: A brief description of the DAG.
* default_args: The default arguments for the DAG.
* max_active_runs: The maximum number of active DAG runs.
* tags: The tags for the DAG.
* schedule_interval: The interval at which to schedule the DAG.
* catchup: Whether to backfill past DAG runs.
    """)       
       
    @staticmethod
    def generate_data_transformation(dag_id, body: str, database: str, schedule_interval: str = None, retries: int = 2, retry_delay: timedelta = timedelta(hours=1), nb_records_per_page: int = 5000, *args, **kwargs):
        args = {
            "owner": "pdssp-crawler",
            "start_date": pendulum.datetime(2023, 1, 1, tz='Europe/Paris'),
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
            "retries": retries,
            "retry_delay": retry_delay,
        }

        with DAG(
            dag_id,
            description=f"STAC transformation of PDS data for {body}",
            default_args=args,
            max_active_runs=1,
            tags=["production", "PDS", "transformation", body],
            schedule_interval=schedule_interval,            
            catchup=False,
        ) as dag:  
            dag.doc_md = BodyTransformationGeneratorDag.DOC_STAC.substitute(dag_id = dag_id, body = body)          
            start_task = DummyOperator(task_id="Start")
            has_new_collection = PdsCacheBranchOperator(task_id='Has_new_collection_to_transform', database=database, body=body, next="stac_transform_catalogs", otherwise="Stop")
            stac_catalog = StacCatalogTranformOperator(task_id='stac_transform_catalogs', database=database, body=body)
            stac_item = StacItemTranformOperator(task_id='stac_stransform_items', database=database, body=body)          
            notification_task = DummyOperator(task_id='Notification')
            stop_task = DummyOperator(task_id="Stop")   
            start_task >> has_new_collection >> [stac_catalog, notification_task]
            stac_catalog >> stac_item >> notification_task >> stop_task      