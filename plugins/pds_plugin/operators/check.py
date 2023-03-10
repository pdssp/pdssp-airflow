from airflow.operators.branch import BaseBranchOperator
from airflow.utils.context import Context
from pds_crawler.etl import StacETL, CheckUpdateEnum
from pds_crawler.models import PdsRegistryModel
from typing import List, Union, Iterable
import logging

logger = logging.getLogger(__name__)


class AbstractBranchOperator(BaseBranchOperator):
    """
    ## PdsBranchOperator

    #### Purpose
    TODO

    #### TODO
    - N/A

    #### BUG
    - N/A
    """
    
    template_fields = ["database","body","next","otherwise"]
    
    def __init__(
        self,
        database: str,
        body: str,
        next: str,
        otherwise: str,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.doc_md = AbstractBranchOperator.__doc__
        self.log.info(
            f"""
            Inputs of PdsBranchOperator:
            - database: {database}
            - body: {body}
            """
        )    
        self.database = database
        self.body = body
        self.next = next
        self.otherwise = otherwise
        self.type_of_check: CheckUpdateEnum = CheckUpdateEnum.CHECK_PDS  
        
    def choose_branch(self, context: Context) -> Union[str, Iterable[str]]:
        pds_stac = PdsStacEtl(self.database)
        pds_stac.body = self.body
        new, update = pds_stac.check_update(self.type_of_check) 
        branch: str
        if new == 0 and update == 0:
            branch = self.otherwise
        else:
            branch = self.next     
        return branch   
    
class PdsBranchOperator(AbstractBranchOperator):
    """
    ## PdsBranchOperator

    #### Purpose
    TODO

    #### TODO
    - N/A

    #### BUG
    - N/A
    """    
    def __init__(self, database: str, body: str, next: str, otherwise: str, *args, **kwargs):
        super().__init__(database=database, body=body, next=next, otherwise=otherwise, *args, **kwargs)
        self.type_of_check = CheckUpdateEnum.CHECK_PDS     
  
class PdsCacheBranchOperator(AbstractBranchOperator):
    """
    ## PdsCacheBranchOperator

    #### Purpose
    TODO

    #### TODO
    - N/A

    #### BUG
    - N/A
    """    
    def __init__(self, database: str, body: str, next: str, otherwise: str, *args, **kwargs):
        super().__init__(database=database, body=body, next=next, otherwise=otherwise, *args, **kwargs)
        self.type_of_check = CheckUpdateEnum.CHECK_CACHE   
     

class PdsStacEtl(StacETL):    
    
    def __init__(self, full_path_database_name: str) -> None:
        super().__init__(full_path_database_name)
        
    def check_update(self, source: CheckUpdateEnum, *args, **kwargs):
        match source:
            case CheckUpdateEnum.CHECK_CACHE:
                pds_collections: List[
                    PdsRegistryModel
                ] = self.pds_registry.load_pds_collections_from_cache(
                    self.body, self.dataset_id
                )
                nb_to_ingest: int = self._check_collections_to_ingest(
                    pds_collections
                )
                logger.info(
                    f"""Summary:
            {nb_to_ingest} collection(s) to ingest from cache"""
                )
                return (nb_to_ingest, 0)

            case CheckUpdateEnum.CHECK_PDS:
                pds_collections_cache: List[
                    PdsRegistryModel
                ] = self.pds_registry.load_pds_collections_from_cache(
                    self.body, self.dataset_id
                )
                _, pds_collections = self.pds_registry.get_pds_collections(
                    self.body, self.dataset_id
                )
                nb_to_update: int = self._check_updates_from_PDS(
                    pds_collections, pds_collections_cache
                )
                (
                    nb_to_ingest,
                    nb_records,
                ) = self.check_collections_to_ingest_from_pds(
                    pds_collections, pds_collections_cache
                )
                logger.info(
                    f"""Summary:
            - {nb_to_ingest} collection(s) to ingest from PDS, i.e {nb_records} products
            - {nb_to_update} collection(s) to update"""
                )
                return (nb_to_ingest, nb_to_update)

            case _:
                raise NotImplementedError(
                    f"Check update is not implemented for {source}"
                )        
    