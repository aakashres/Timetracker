import requests
from .utils import get_url


class TrackerAPIClient:

    def __init__(self, app_token, auth_token=None, email=None, password=None):
        """
        Either auth token must be provided or email and password both
        """
        self._app_token = app_token
        if not auth_token and not (email and password):
            print("Issueeeeeee")  # todo
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
            print(response.json())
            self._auth_token = response.json()["user"]["auth_token"]
        elif response.status_code == 401:
            # Auth error
            pass
        else:
            # Other issue
            pass
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
            print("still issue")
            return

        result = response.json()
        if "error" in result:
            print(response["error"])
            return []
        return result

    def get_organization(self):
        # result = self._requests("GET", get_url("organization"))
        result = {'organizations': [{'id': 302192, 'name': 'rt-bot-191', 'last_activity': '2020-12-23T06:00:00Z'}]}s
        return result["organizations"]

    def get_organization_activities(self):
        pass

    def get_user_list(self):
        pass

    def get_project_list(self):
        pass
