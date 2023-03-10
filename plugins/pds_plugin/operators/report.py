from airflow.models.baseoperator import BaseOperatorLink
from pds_plugin.operators.extract import PdsObsExtractOperator, PdsDescExtractOperator, PdsCollExtractOperator
from airflow.models.taskinstance import TaskInstanceKey
from airflow.models.abstractoperator import AbstractOperator
from airflow.exceptions import AirflowException
import os
from airflow.models.variable import Variable
from typing import Union


class ReportLink(BaseOperatorLink):
    """Create a link to the crawler's result."""

    name = "See report"

    operators = [PdsObsExtractOperator, PdsDescExtractOperator, PdsCollExtractOperator]

    def get_link(self, operator: AbstractOperator , *, ti_key: TaskInstanceKey):
        run_id: str = ti_key.run_id
        name: str = run_id+".md"
        filename = os.path.join(Variable.get("pds_database"), name)
        if os.path.exists(filename):
            result = os.path.join("/files/static",name)
        else:
            result = None
        return result