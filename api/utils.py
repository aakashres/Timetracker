def get_url(endpoint, id=None):
    """
        Returns full url for hubstaff endpoint

        :params str endpoint
    """
    BASE_URL = "https://api.hubstaff.com/v1"
    endpoint_url_map = {
        "auth": "auth",
        "organization": "organizations",
        "activity": "activities",
        "user": "organizations/%s/members",
        "project": "organizations/%s/projects",
    }
    if endpoint not in endpoint_url_map:
        return KeyError("Provided endpoint is not valid. Use one of (%s)" % "/".join(endpoint_url_map.keys()))
    end_url = endpoint_url_map.get(endpoint)
    if id:
        end_url = end_url % id
    return f"{BASE_URL}/{end_url}"


if __name__ == "__main__":
    print(get_url("auth"))
    print(get_url("user", 1))
    print(get_url("project", 1))
    print(get_url("s", 1))
