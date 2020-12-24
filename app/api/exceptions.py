class TrackerError(Exception):
    """
    """

    message = "API error"

    def __init__(self, message):
        super(TrackerError, self).__init__(message or self.message)


class TrackerAuthError(TrackerError):
    message = "Authentication Error"
