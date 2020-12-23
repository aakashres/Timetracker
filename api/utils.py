def get_url(endpoint):
    BASE_URL = "https://api.hubstaff.com/v1"
    endpoint_url_map = {
        "auth": "auth"
    }
    if endpoint not in endpoint_url_map:
        return False
    return f"{BASE_URL}/{endpoint_url_map.get(endpoint)}"


if __name__ == "__main__":
    print(get_url("auth_endpoint"))
