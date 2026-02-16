import sys
import logging

# Enable Apache Errorss
logging.basicConfig(stream=sys.stderr)

# Flask path
PROJECT_DIR = '/var/www/html/flaskapp'
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

# Import app from flaskapp.py
from flaskapp import app as application
