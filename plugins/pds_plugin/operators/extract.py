from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context
from typing import Any
from pds_crawler.etl import StacETL, PdsSourceEnum
from pds_crawler.report import CrawlerReport
from airflow.models.taskinstance import TaskInstanceKey

class PdsCollExtractOperator(BaseOperator):
    
    template_fields = ["database","body"]
    
    def __init__(self, database, body, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = database
        self.body = body
    
    def execute(self, context: Context) -> Any:
        ti = context['task_instance']
        task_instance_key: TaskInstanceKey = ti.key        
        run_id: str = task_instance_key.run_id        
        stac_etl = StacETL(self.database)
        stac_etl.body = self.body
        report: CrawlerReport = stac_etl.report
        report.name = f"{run_id}.md"         
        report.start_report()         
        stac_etl.extract(PdsSourceEnum.COLLECTIONS_INDEX_SAVE)
        report.close_report()
        
class PdsObsExtractOperator(BaseOperator):
    
    template_fields = ["database","body"]
    
    def __init__(self, database, body, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = database
        self.body: str = body
        self.nb_workers:int = 3
        self.time_sleep: int = 2  
        self.is_sample: bool = False
        self.nb_records_per_page: int = 5000  
        self.progress_bar: bool = False    
    
    def execute(self, context: Context) -> Any:
        ti = context['task_instance']
        task_instance_key: TaskInstanceKey = ti.key        
        run_id: str = task_instance_key.run_id
        task_id: str = task_instance_key.task_id
        stac_etl = StacETL(self.database)       
        stac_etl.nb_workers = self.nb_workers
        stac_etl.time_sleep = self.time_sleep         
        stac_etl.is_sample = self.is_sample
        stac_etl.body = self.body
        stac_etl.nb_records_per_page = self.nb_records_per_page  
        stac_etl.progress_bar = self.progress_bar      
        report: CrawlerReport = stac_etl.report
        report.name = f"{task_id}_{run_id}.md" 
        report.start_report()        
        stac_etl.extract(PdsSourceEnum.PDS_RECORDS)           
        report.close_report()
        
class PdsDescExtractOperator(BaseOperator):
    
    template_fields = ["database","body"]
    
    def __init__(self, database, body, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = database
        self.body = body
        self.nb_workers:int = 3
        self.time_sleep = 2
        self.progress_bar: bool = False
        
    def execute(self, context: Context) -> Any:
        ti = context['task_instance']
        task_instance_key: TaskInstanceKey = ti.key
        run_id: str = task_instance_key.run_id   
        task_id: str = task_instance_key.task_id               
        stac_etl = StacETL(self.database)
        stac_etl.nb_workers = self.nb_workers
        stac_etl.time_sleep = self.time_sleep
        stac_etl.body = self.body
        stac_etl.progress_bar = self.progress_bar              
        report: CrawlerReport = stac_etl.report        
        report.name = f"{task_id}_{run_id}.md" 
        report.start_report()         
        stac_etl.extract(PdsSourceEnum.PDS_CATALOGS) 
        report.close_report()            
    
    
