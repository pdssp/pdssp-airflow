from pds_plugin.dags import BodyTransformationGeneratorDag
from airflow.models.variable import Variable

database: str = Variable.get(
    "pds_database", default_var="/tmp/data"
)

BodyTransformationGeneratorDag.generate_data_transformation(
    dag_id="Mercury_transformation", 
    body="Mercury", 
    database=database,
)
BodyTransformationGeneratorDag.generate_data_transformation(
    dag_id="Venus_transformation", 
    body="Venus", 
    database=database   
)
BodyTransformationGeneratorDag.generate_data_transformation(
    dag_id="Moon_transformation", 
    body="Moon", database=database,
    nb_records_per_page = 500    
)
BodyTransformationGeneratorDag.generate_data_transformation(
    dag_id="Mars_transformation", 
    body="Mars", 
    database=database,
)
    