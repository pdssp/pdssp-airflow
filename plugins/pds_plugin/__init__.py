from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from airflow.plugins_manager import AirflowPlugin
from pds_plugin.appbuilderview import stac_storage_view_package, pds_storage_view_package
from pds_plugin.blueprint import bp
from pds_plugin.operators import ReportLink

# Define the plugin class
class PdsPlugins(AirflowPlugin):
    # Name your AirflowPlugin
    name = "pds_plugin"
    
    appbuilder_views = [
        stac_storage_view_package, pds_storage_view_package
    ]
    flask_blueprints = [bp]  
    operator_extra_links = [
        ReportLink(),
    ]      
