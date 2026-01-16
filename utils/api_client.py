import requests

from config.configs import API_BASE_URL, OAUTH_TOKEN


class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.token = OAUTH_TOKEN
        if self.token:
            self.session.headers.update({"Authorization": f"OAuth {self.token}"})

    def set_auth(self):
        self.session.headers.update({"Authorization": f"OAuth {self.token}"})

    def set_unauth(self):
        self.session.headers.pop("Authorization", None)

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get(self, endpoint="", params=None, data=None):
        url = f"{self.base_url}/{endpoint}".rstrip("/")
        return self.session.get(url, params=params, data=data)

    def post(self, endpoint="", params=None, data=None):
        url = f"{self.base_url}/{endpoint}".rstrip("/")
        return self.session.post(url, params=params, data=data)

    def put(self, endpoint="", params=None, data=None):
        url = f"{self.base_url}/{endpoint}".rstrip("/")
        return self.session.put(url, params=params, data=data)

    def delete(self, endpoint="", params=None, data=None):
        url = f"{self.base_url}/{endpoint}".rstrip("/")
        return self.session.delete(url, params=params, data=data)
