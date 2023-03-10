from pds_plugin.dags import BodyExtractionGeneratorDag
from airflow.models.variable import Variable

database: str = Variable.get(
    "pds_database", default_var="/tmp/data"
) 

nb_workers: str = Variable.get(
    "nb_workers", default_var="3"
)  

sleep_time: str = Variable.get(
    "sleep_time", default_var="2"
) 

BodyExtractionGeneratorDag.generate_list_collections_extraction(
    dag_id="Mercury_PDS_collection_list", 
    body="Mercury", 
    database=database,
    nb_workers = int(nb_workers),
    sleep_time = int(sleep_time)
)
BodyExtractionGeneratorDag.generate_list_collections_extraction(
    dag_id="Venus_PDS_collection_list", 
    body="Venus", 
    database=database,
    nb_workers = int(nb_workers),
    sleep_time = int(sleep_time)    
)
BodyExtractionGeneratorDag.generate_list_collections_extraction(
    dag_id="Moon_PDS_collection_list", 
    body="Moon", 
    database=database,
    nb_workers = int(nb_workers),
    sleep_time = int(sleep_time)
)
BodyExtractionGeneratorDag.generate_list_collections_extraction(
    dag_id="Mars_PDS_collection_list", 
    body="Mars", 
    database=database,
    nb_workers = int(nb_workers),
    sleep_time = int(sleep_time)
)