""" 
This module defines two Flask views for browsing directories and their contents, 
PdsStorageView and StacStorageView. These views inherit from the Flask-AppBuilder 
BaseView class and define the template_folder and DATABASE class attributes.

The PdsStorageView and StacStorageView classes define a method, _make_tree, that 
recursively generates a dictionary representing a directory tree structure. This 
method is called in the list method, which renders the directory tree structure 
in a template using the render_template method.

The views are registered as Flask-AppBuilder views using two dictionaries, 
pds_storage_view_package and stac_storage_view_package, which specify the name, 
category, and view class for each view.
"""
from flask import Flask
from flask import make_response
from flask import render_template
from flask_appbuilder import BaseView as AppBuilderBaseView
from flask_appbuilder import expose
import logging
import os

from airflow.models.variable import Variable


logger = logging.getLogger(__name__)


class StacStorageView(AppBuilderBaseView):
    
    template_folder = "/opt/airflow/plugins/pds_plugin/appbuilderview"

    DATABASE: str = Variable.get(
        "pds_database", default_var="/opt/airflow/database"
    )
    
    STAC_STORAGE = os.path.join(DATABASE, "stac")

    def _make_tree(self, path):
        tree = dict(name=os.path.basename(path), children=[])
        try:
            lst = os.listdir(path)
        except OSError:
            pass  # ignore errors
        else:
            for name in lst:
                fn = os.path.join(path, name)
                if os.path.isdir(fn):
                    tree["children"].append(self._make_tree(fn))
                else:
                    size: int = os.path.getsize(fn)
                    status: str = "fa-solid fa-xmark" if size < 500 else None
                    url = fn.replace(StacStorageView.STAC_STORAGE+"/", "")
                    tree["children"].append(
                        dict(name={"url": url, "value": name, "status": status})
                    )
        return tree

    @expose("/")
    def list(self):
        return self.render_template(
            "dirtree.html", tree=self._make_tree(StacStorageView.STAC_STORAGE)
        )
        
class PdsStorageView(AppBuilderBaseView):
    
    template_folder = "/opt/airflow/plugins/pds_plugin/appbuilderview"

    DATABASE: str = Variable.get(
        "pds_database", default_var="/opt/airflow/database"
    )
    
    PDS_STORAGE = os.path.join(DATABASE, "files")

    def _make_tree(self, path):
        tree = dict(name=os.path.basename(path), children=[])
        try:
            lst = os.listdir(path)
        except OSError:
            pass  # ignore errors
        else:
            for name in lst:
                fn = os.path.join(path, name)
                if os.path.isdir(fn):
                    tree["children"].append(self._make_tree(fn))
                else:
                    size: int = os.path.getsize(fn)
                    status: str = "fa-solid fa-xmark" if size < 500 else None
                    url = fn.replace(PdsStorageView.PDS_STORAGE+"/", "")
                    tree["children"].append(
                        dict(name={"url": url, "value": name, "status": status})
                    )
        return tree

    @expose("/")
    def list(self):
        return self.render_template(
            "dirtree.html", tree=self._make_tree(PdsStorageView.PDS_STORAGE)
        )        
        
pds_storage_view = PdsStorageView()
stac_storage_view = StacStorageView()

stac_storage_view_package = {
    "name": "STAC storage View",
    "category": "Browse directory",
    "view": stac_storage_view,
}

pds_storage_view_package = {
    "name": "PDS storage View",
    "category": "Browse directory",
    "view": pds_storage_view,
}