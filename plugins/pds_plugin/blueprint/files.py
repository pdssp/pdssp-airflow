""" 
This module defines a Flask blueprint named "serve_files" that serves 
static files from a specified folder. The static folder is set to 
"/opt/airflow/database" and the URL prefix for accessing the static 
files is set to "/files". The static URL path is set to "/static". This 
blueprint can be registered with a Flask application to enable serving of 
static files from the specified folder.
"""
from flask import Blueprint

bp = Blueprint(
    "serve_files",
    __name__,
    url_prefix="/files",
    static_folder="/opt/airflow/database", 
    static_url_path="/static",
)