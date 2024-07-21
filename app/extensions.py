"""
Extensions Container
=====================
To avoid circular import errors, we have this handy module to instantiate and contain our extensions. 
"""
from authlib.integrations.flask_client import OAuth
from apscheduler.schedulers.background import BackgroundScheduler

oauth = OAuth()
scheduler = BackgroundScheduler()
