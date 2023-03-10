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

BodyExtractionGeneratorDag.generate_data_extraction(
    dag_id="Mercury_extraction", 
    body="Mercury", 
    database=database,
    nb_workers = int(nb_workers),
    sleep_time = int(sleep_time)    
)
BodyExtractionGeneratorDag.generate_data_extraction(
    dag_id="Venus_extraction", 
    body="Venus", 
    database=database,
    nb_workers = int(nb_workers),
    sleep_time = int(sleep_time)    
)
BodyExtractionGeneratorDag.generate_data_extraction(
    dag_id="Moon_extraction", 
    body="Moon", database=database,
    nb_workers = int(nb_workers),
    sleep_time = int(sleep_time)    
)
BodyExtractionGeneratorDag.generate_data_extraction(
    dag_id="Mars_extraction", 
    body="Mars", 
    database=database,
    nb_workers = int(nb_workers),
    sleep_time = int(sleep_time)    
)