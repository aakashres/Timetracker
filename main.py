import os

from dotenv import load_dotenv
from datetime import datetime, timedelta

from api import tracker_api

load_dotenv()

# tracker = tracker_api.TrackerAPIClient(
#     app_token=os.getenv("HUBSTAFF_APP_TOKEN"),
#     email=os.getenv("HUBSTAFF_EMAIL"),
#     password=os.getenv("HUBSTAFF_PASSWORD")
# )

# os.environ["HUBSTAFF_AUTH_TOKEN"] = tracker.authenticate()


tracker = tracker_api.TrackerAPIClient(
    app_token=os.getenv("HUBSTAFF_APP_TOKEN"),
    auth_token=os.getenv("HUBSTAFF_AUTH_TOKEN"),
    email=os.getenv("HUBSTAFF_EMAIL"),
    password=os.getenv("HUBSTAFF_PASSWORD")
)
start_time = datetime.combine(datetime.now().date(), datetime.min.time()) - timedelta(days=1)
stop_time = datetime.combine(datetime.now().date(), datetime.min.time()) - timedelta(minutes=1)
org = tracker.get_organization()
print(tracker.get_organization_activities(start_time, stop_time, organization_ids=[org[0]["id"]]))