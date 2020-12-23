import os

from dotenv import load_dotenv
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
