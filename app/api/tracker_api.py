import requests
from .utils import get_url
from .exceptions import TrackerError, TrackerAuthError


class TrackerAPIClient:

    def __init__(self, app_token, auth_token=None, email=None, password=None):
        """
        Either auth token must be provided or email and password both.
        Initializes necessary tokens and variable

        :params str app_token: Hubstaff v1 app token
        :params str auth_token:
        :params str email: hubstaff registered email
        :params str password: hubstaff registered password
        """
        if not app_token:
            raise ValueError("app_token is must be set. Missing in env file")
        self._app_token = app_token
        if not auth_token and not (email and password):
            raise ValueError("auth_token or (email, password) pair must be set. Missing in env file")
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

            :param str method: rest API method: ``GET`` or ``POST``
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
        if "activities" not in result:
            raise TrackerError("Data not fetched; get_organization_activities")
        return result["activities"]

    def get_user_list(self, organization_id, include_removed=False, offset=0):
        """
            Fetches users of an organization

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
        if "users" not in result:
            raise TrackerError("Data not fetched; get_user_list")
        return result["users"]

    def get_project_list(self, organization_id, offset=0):
        """
            Fetches projects of an organization

            :params int organization_id: any organization's id
            :params int offset: (optional) index of the first record returned

            :return list: list of projects is associated with any organization
        """
        params = {
            "offset": offset
        }
        result = self._requests("GET", get_url("project", organization_id), params=params)
        if "projects" not in result:
            raise TrackerError("Data not fetched; get_project_list")
        return result["projects"]
