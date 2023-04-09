# WSGI configuration required to serve up your web app.
from website import create_app
import sys

# add your project directory to the sys.path here
project_home = ''
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import create_app from the website module

# create the Flask app instance
application = create_app()
