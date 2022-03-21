import requests
import logging


class Client:
    def __init__(self, auth_token):
        self.auth_token = auth_token

    # def export_playlist(self):
    #     pass

    def get_json_response(self, url):
        r = self._get_api_request(url)
        request_data = r.json()
        assert r.status_code == 200, f"Bad request: {request_data}"
        return request_data

    def _get_api_request(self, url):
        logging.debug(f"GET: {url}")
        return requests.get(
            url=url,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.auth_token}",
            },
        )

    def _get_post_request(self, url):
        logging.debug(f"GET: {url}")
        return requests.post(
            url=url,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.auth_token}",
            },
        )

