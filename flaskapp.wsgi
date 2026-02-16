import sys
import logging

# Configure logging to see errors in the Apache logs
logging.basicConfig(stream=sys.stderr)

# Define the path to your app
PROJECT_DIR = '/var/www/html/flaskapp'
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

# Import the 'app' object from your 'flaskapp.py' file
from flaskapp import app as application
