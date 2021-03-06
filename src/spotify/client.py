import json
import logging
from typing import Dict

import requests


class Client:
    def __init__(self, auth_token):
        self.auth_token = auth_token

    def get_json_request(self, url: str) -> Dict:
        r = self._get_api_request(url)
        request_data = r.json()
        assert r.status_code == 200, f"Bad request: {request_data}"
        return request_data

    def post_json_request(self, url: str, json_body: Dict) -> Dict:
        r = self._post_api_request(url, json_body)
        request_data = r.json()
        assert r.status_code == 201, f"Bad request: {request_data}"
        return request_data

    def _get_api_request(self, url: str) -> requests.Response:
        logging.debug(f"GET: {url}")
        return requests.get(
            url=url,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.auth_token}",
            },
        )

    def _post_api_request(self, url: str, body: Dict) -> requests.Response:
        logging.debug(f"POST: {url}")
        logging.debug(f"BODY: {body}")
        return requests.post(
            url=url,
            data=json.dumps(body),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.auth_token}",
            },
        )
