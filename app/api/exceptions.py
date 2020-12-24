class TrackerError(Exception):
    """
        Raises when API endpoint returns unexpected response format.

        :param str message: (optional) custom error message
    """

    message = "API error"

    def __init__(self, message):
        super(TrackerError, self).__init__(message or self.message)


class TrackerAuthError(TrackerError):
    message = "Authentication Error"
