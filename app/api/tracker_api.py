import requests
from .utils import get_url
from .exceptions import TrackerError, TrackerAuthError


class TrackerAPIClient:

    def __init__(self, app_token, auth_token=None, email=None, password=None):
        """
        Either auth token must be provided or email and password both
        """
        self._app_token = app_token
        if not auth_token and not (email and password):
            raise ValueError("auth_token or (email, password) pair must be set")
        self._email = email
        self._password = password
        self._auth_token = auth_token

    def authenticate(self):
        """
        Authenticates to hubstaff to acquire authentication token

        :return string: Authentication token
        """
        if self._auth_token or (not self._email and not self._password):
            return self._auth_token
        header = {"App-Token": self._app_token}
        data = {"email": self._email, "password": self._password}
        response = requests.post(get_url("auth"), headers=header, data=data)
        if response.status_code == 200:
            self._auth_token = response.json()["user"]["auth_token"]
        elif response.status_code == 401:
            raise TrackerAuthError(response.json()["error"])
        else:
            raise TrackerError(response.json()["error"])
        return self._auth_token

    def _requests(self, method, url, params=None, headers=None, data=None, json=None, refresh_token=False):
        """
            Fetches desired data from hubstaff APIs

            :param str method: rest API method: ``GET`` or ``POST`
            :param str url: URL for the new request
            :param dict params: (optional) query params
            :param dict data: (optional) form data content
            :param dict json: (optional) json data content
            :param dict headers: additional header ``auth_token`` and ``app_token``
            :param refresh_token headers: additionam header auth_token and app_token

            :return list/dict : json data response
        """
        if not self._auth_token or refresh_token:
            self.authenticate()

        headers = headers.copy() if headers else {}
        headers.update({
            "App-Token": self._app_token,
            "Auth-Token": self._auth_token,
        })
        response = requests.request(method, url, params=params, headers=headers, data=data, json=json)

        if response.status_code == 401:
            # false refresh_token denotes first execution. Token can expire. Ask for new in next execution
            if not refresh_token:
                return self._requests(method, url, params=params, headers=headers, data=data, json=json, refresh_token=True)
            raise TrackerAuthError(response.json()["error"])

        result = response.json()
        if "error" in result:
            raise TrackerError(response["error"])
        return result

    def get_organization(self):
        """
            Fetches Organization that user is associated with

            :return list: list of organization user is associated with
        """
        result = self._requests("GET", get_url("organization"))
        # result = {'organizations': [{'id': 302192, 'name': 'rt-bot-191', 'last_activity': '2020-12-23T06:00:00Z'}]}
        if "organizations" not in result:
            raise TrackerError("Data not fetched; get_organization")
        return result["organizations"]

    def get_organization_activities(self, from_, to_, organization_ids=None, project_ids=None, user_ids=None, offset=0):
        """
            Fetches organizational activities from start time to end time

            :params datetime from_: date to fetch activities starting from
            :params datetime to_: date to fetch activities ending upto
            :params list organization_ids: (optional) List of organization IDs
            :params list project_ids: (optional) List of project IDs
            :params list user_ids: (optional) List of user IDs
            :params int offset: (optional) index of the first record returned

            :return list: list of activities within the organizations
        """
        params = {
            "start_time": from_.isoformat(),
            "stop_time": to_.isoformat(),
            "offset": offset
        }
        if organization_ids:
            params["organizations"] = ",".join(map(str, organization_ids))
        if project_ids:
            params["projects"] = ",".join(map(str, project_ids))
        if user_ids:
            params["users"] = ",".join(map(str, user_ids))
        result = self._requests("GET", get_url("activity"), params=params)
        # result = {'activities': [{'id': 1828571999, 'time_slot': '2020-12-22T04:50:00Z', 'starts_at': '2020-12-22T04:50:46Z', 'user_id': 770062, 'project_id': 1312779, 'task_id': None, 'keyboard': 100, 'mouse': 100, 'overall': 200, 'tracked': 200, 'paid': False}, {'id': 1828882920, 'time_slot': '2020-12-22T07:00:00Z', 'starts_at': '2020-12-22T07:04:34Z', 'user_id': 196435, 'project_id': 1312780, 'task_id': None, 'keyboard': 230, 'mouse': 99, 'overall': 286, 'tracked': 326, 'paid': False}, {'id': 1828882997, 'time_slot': '2020-12-22T07:10:00Z', 'starts_at': '2020-12-22T07:10:00Z', 'user_id': 1058189, 'project_id': 1312778, 'task_id': None, 'keyboard': 115, 'mouse': 39, 'overall': 140, 'tracked': 188, 'paid': False}, {'id': 1829311594, 'time_slot': '2020-12-22T09:50:00Z', 'starts_at': '2020-12-22T09:52:59Z', 'user_id': 1058189, 'project_id': 1312778, 'task_id': None, 'keyboard': 9, 'mouse': 33, 'overall': 38, 'tracked': 47, 'paid': False}, {'id': 1829323338, 'time_slot': '2020-12-22T09:50:00Z', 'starts_at': '2020-12-22T09:56:11Z', 'user_id': 1058189, 'project_id': 1312778, 'task_id': None, 'keyboard': 82, 'mouse': 49, 'overall': 110, 'tracked': 124, 'paid': False}, {'id': 1829326285, 'time_slot': '2020-12-22T09:50:00Z', 'starts_at': '2020-12-22T09:59:12Z', 'user_id': 1058189, 'project_id': 1312778, 'task_id': None, 'keyboard': 7, 'mouse': 12, 'overall': 17, 'tracked': 19, 'paid': False}, {'id': 1829343255, 'time_slot': '2020-12-22T10:00:00Z', 'starts_at': '2020-12-22T10:02:27Z', 'user_id': 1058189, 'project_id': 1312778, 'task_id': None, 'keyboard': 67, 'mouse': 74, 'overall': 125, 'tracked': 146, 'paid': False}, {'id': 1829348185, 'time_slot': '2020-12-22T10:00:00Z', 'starts_at': '2020-12-22T10:06:19Z', 'user_id': 1058189, 'project_id': 1312778, 'task_id': None, 'keyboard': 16, 'mouse': 7, 'overall': 22, 'tracked': 24, 'paid': False}, {'id': 1829381523, 'time_slot': '2020-12-22T10:00:00Z', 'starts_at': '2020-12-22T10:07:58Z', 'user_id': 1058189, 'project_id': 1312778, 'task_id': None, 'keyboard': 23, 'mouse': 84, 'overall': 105, 'tracked': 122, 'paid': False}, {'id': 1829383204, 'time_slot': '2020-12-22T10:10:00Z', 'starts_at': '2020-12-22T10:10:00Z', 'user_id': 1058189, 'project_id': 1312778, 'task_id': None, 'keyboard': 291, 'mouse': 344, 'overall': 509, 'tracked': 583, 'paid': False}]}
        if "activities" not in result:
            raise TrackerError("Data not fetched; get_organization_activities")
        return result["activities"]

    def get_user_list(self, organization_id, include_removed=False, offset=0):
        """
            Fetches user of an organization

            :params int organization_id: any organization's id
            :params bool include_removed: (optional) Include users that are removed from the organization
            :params int offset: (optional) index of the first record returned

            :return list: list of  user is associated with any organization
        """
        params = {
            "include_removed": include_removed,
            "offset": offset
        }
        result = self._requests("GET", get_url("user", organization_id), params=params)
        # result = {'users': [{'id': 1058189, 'name': 'Aakash Shrestha', 'last_activity': '2020-12-23T09:50:00Z', 'email': 'aakash.shres@gmail.com', 'membership_status': 'active'}, {'id': 770062, 'name': 'Agata Gąsiorowska', 'last_activity': '2020-10-25T03:30:00Z', 'email': 'agata.gasiorowska@reef.pl', 'membership_status': 'active'}, {'id': 196435, 'name': 'Paweł Polewicz', 'last_activity': '2020-12-23T00:33:30Z', 'email': 'pawel.polewicz@reef.pl', 'membership_status': 'active'}]}
        if "users" not in result:
            raise TrackerError("Data not fetched; get_user_list")
        return result["users"]

    def get_project_list(self, organization_id, offset=0):
        """
            Fetches user of an organization

            :params int organization_id: any organization's id
            :params int offset: (optional) index of the first record returned

            :return list: list of projects is associated with any organization
        """
        params = {
            "offset": offset
        }
        result = self._requests("GET", get_url("project", organization_id), params=params)
        # result = {'projects': [{'id': 1312778, 'name': 'hubstaff bot191', 'last_activity': '2020-12-23T09:50:00Z', 'status': 'Active', 'description': None}, {'id': 1312779, 'name': 'Project A', 'last_activity': '2020-12-23T05:37:47Z', 'status': 'Active', 'description': None}, {'id': 1312780, 'name': 'Project B', 'last_activity': None, 'status': 'Active', 'description': None}]}
        if "projects" not in result:
            raise TrackerError("Data not fetched; get_project_list")
        return result["projects"]
