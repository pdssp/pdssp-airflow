""" 
In Airflow, AppBuilderView is a class that extends Flask's MethodView. 
It is a base class that allows users to define their own views by 
subclassing it and implementing methods that handle specific HTTP methods 
(e.g., GET, POST, etc.) for a particular URL endpoint.

AppBuilderView is used in Airflow's FlaskAppBuilder module, which provides 
a framework for building web applications on top of Flask. This module is 
used to create and manage a Flask app and register views, which can then be 
accessed through the app's URL routes.

Using AppBuilderView in Airflow can be useful for creating custom views that 
extend the functionality of Airflow's web UI.
"""
from pds_plugin.appbuilderview.dirview import stac_storage_view_package, pds_storage_view_package

__all__ = [
    "stac_storage_view_package", "pds_storage_view_package"
]