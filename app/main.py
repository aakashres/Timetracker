import os
import time
import logging

from pathlib import Path
from dotenv import load_dotenv
from itertools import groupby
from operator import itemgetter
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta


from api import tracker_api


def init_logging():
    """
        Instantiates directory and log file
    """
    log_path = Path(__file__).resolve().parent.joinpath("logs")
    log_path.mkdir(exist_ok=True)
    logging.basicConfig(filename=log_path.joinpath("app.logs"), filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')


def save_output(data):
    """
        Formats table data into HTML page

        :params list table_header:  List of user name(table header)
        :params list table_rows: List of project and time worked by user on them
    """
    template_dir = Path(__file__).resolve().parent.joinpath("template")
    output_dir = Path(__file__).resolve().parent.joinpath("output")
    output_dir.mkdir(exist_ok=True)

    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template("output_template.html")

    output = template.render(organization_name=data.get("org_name"), date=data.get("data_timestamp"), table_header=data.get("table_header"), table_rows=data.get("table_rows"))
    output_path = output_dir.joinpath("timesheet.html")

    with output_path.open("w") as outfile:
        outfile.write(output)


def format_data(data):
    """
        Compiles data of user projects and activities to properly format it into tablular strucutre
        so that it can be rendered in HTML file

        :params dict data: consists of users, projects, activities, data_timestamp and organization name

        :return dict data: consists of List of user name,
            List of project and time worked by user on them,
            Date of which data is fetched and Name of organization
            of which data is being prepared
    """
    user_id_map = {user["id"]: user["name"] for user in data.get("users")}
    project_id_map = {project["id"]: project["name"] for project in data.get("projects")}

    user_ids, project_ids = [], []
    for activity in data.get("activities"):
        if activity["user_id"] not in user_ids:
            user_ids.append(activity["user_id"])
        if activity["project_id"] not in project_ids:
            project_ids.append(activity["project_id"])

    grouper = itemgetter("project_id", "user_id")
    worked_time_data = {}
    for key, grp in groupby(sorted(data.get("activities"), key=grouper), grouper):
        worked_time_data["{}_{}".format(key[0], key[1])] = time.strftime("%H:%M:%S", time.gmtime(sum(item["tracked"] for item in grp)))

    table_header = ["Projects_Users"] + [user_id_map.get(user_id) for user_id in user_ids]
    table_rows = []
    for project_id in project_ids:
        row = []
        row.append(project_id_map.get(project_id))
        for user_id in user_ids:
            row.append(worked_time_data.get("{}_{}".format(project_id, user_id), "00:00:00"))
        table_rows.append(row)

    data = {
        "table_header": table_header,
        "table_rows": table_rows,
        "data_timestamp": data.get("data_timestamp"),
        "org_name": data.get("org_name")
    }
    return data


def get_data(tracker):
    """
        Fetches all necessary data from Hubstaff api. Fetches data
        of the day before when the script is executed

        :params TrackerAPIClient object tracker: object to get all necessary data

        :return dict data: consists of users, projects, activities, data_date and organization name
    """
    stop_time = datetime.combine(datetime.now().date(), datetime.min.time())
    start_time = stop_time - timedelta(days=1)

    org = tracker.get_organization()
    org_id = org[0]["id"]
    org_name = org[0]["name"]
    users = tracker.get_user_list(org_id)
    projects = tracker.get_project_list(org_id)
    activities = tracker.get_organization_activities(start_time, stop_time, organization_ids=[org[0]["id"]])
    
    data = {
        "users": users,
        "projects": projects,
        "activities": activities,
        "data_timestamp": start_time.date(),
        "org_name": org_name
    }
    return data


def main():
    try:
        init_logging()
        env_file = Path(__file__).resolve().parent.joinpath(".env")
        load_dotenv()

        if os.getenv("HUBSTAFF_AUTH_TOKEN"):
            tracker = tracker_api.TrackerAPIClient(
                app_token=os.getenv("HUBSTAFF_APP_TOKEN"),
                auth_token=os.getenv("HUBSTAFF_AUTH_TOKEN"),
                email=os.getenv("HUBSTAFF_EMAIL"),
                password=os.getenv("HUBSTAFF_PASSWORD")
            )
        else:
            tracker = tracker_api.TrackerAPIClient(
                app_token=os.getenv("HUBSTAFF_APP_TOKEN"),
                email=os.getenv("HUBSTAFF_EMAIL"),
                password=os.getenv("HUBSTAFF_PASSWORD")
            )
            token = tracker.authenticate()
            with env_file.open("a") as outfile:
                outfile.write("\nHUBSTAFF_AUTH_TOKEN={}".format(token))

        data = get_data(tracker)
        data = format_data(data)
        save_output(data)
        # if os.getenv("OUTPUT_MAIL_ADDRESS"):
        #     # in near future, Option to send output in mail might be implemented
        #     email_output(os.getenv("OUTPUT_MAIL_ADDRESS")) # TODO in future add function to send email

    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
