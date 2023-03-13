from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context
from typing import Any
from pds_crawler.etl import StacETL, PdsSourceEnum, PdsDataEnum
from pds_crawler.report import CrawlerReport
from airflow.models.taskinstance import TaskInstanceKey

class StacCatalogTranformOperator(BaseOperator):
    
    template_fields = ["database","body"]
    
    def __init__(self, database, body, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = database
        self.body = body
        self.progress_bar: bool = False    
        
    
    def execute(self, context: Context) -> Any:
        ti = context['task_instance']
        task_instance_key: TaskInstanceKey = ti.key        
        run_id: str = task_instance_key.run_id        
        stac_etl = StacETL(self.database)
        stac_etl.progress_bar = self.progress_bar
        stac_etl.body = self.body
        report: CrawlerReport = stac_etl.report
        report.name = f"{run_id}.md"         
        report.start_report()         
        stac_etl.transform(PdsDataEnum.PDS_CATALOGS)
        report.close_report()
        
class StacItemTranformOperator(BaseOperator):
    
    template_fields = ["database","body"]
    
    def __init__(self, database, body, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = database
        self.body = body
        self.progress_bar: bool = False    
        
    
    def execute(self, context: Context) -> Any:
        ti = context['task_instance']
        task_instance_key: TaskInstanceKey = ti.key        
        run_id: str = task_instance_key.run_id        
        stac_etl = StacETL(self.database)
        stac_etl.progress_bar = self.progress_bar
        stac_etl.body = self.body
        report: CrawlerReport = stac_etl.report
        report.name = f"{run_id}.md"         
        report.start_report()         
        stac_etl.transform(PdsDataEnum.PDS_RECORDS)
        report.close_report()        