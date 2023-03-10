""" 
In Airflow, Blueprint is a concept borrowed from Flask, the underlying web 
framework used by Airflow. A Blueprint is a way to organize related views 
and other code in a modular way, and can be registered with the Flask 
application to create a complete web application. Blueprints allow developers 
to break up a large application into smaller, more manageable pieces that can 
be developed and tested independently. This also makes it easier to add or 
remove functionality from the application without affecting the rest of the code. 
In Airflow, Blueprints are often used to create custom views for the web interface 
or to extend the functionality of the web server.
"""
from pds_plugin.blueprint.files import bp

__all__ = ["bp"]