from .extensions import oauth, scheduler

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import atexit

from .square_tools import process_daily_orders

def init_auth(app):
    oauth.register(
        "auth0",
        client_id=app.config["AUTH0_CLIENT_ID"],
        client_secret=app.config["AUTH0_CLIENT_SECRET"],
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f'https://{app.config["AUTH0_DOMAIN"]}/.well-known/openid-configuration',
    )

def init_scheduler(app):
    # Schedule job
    scheduler.add_job(
        func=process_daily_orders,
        # trigger=IntervalTrigger(seconds=30),
        trigger=CronTrigger(hour=8, minute=0),  # Run at 12:01 AM
        id='process_daily_orders_job',
        name='Process daily orders and update inventory',
        replace_existing=True)

    # Start the scheduler
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())