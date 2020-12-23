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
