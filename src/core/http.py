import requests
from requests import Response

class Http:
    def __init__(self, timeout: float = 20.0):
        self.timeout = timeout
        self.headers: dict[str, str] = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/98.0.4758.82 Safari/537.36"
            )
        }

    def execute_get_entry(self, url: str) -> Response:
        resp: Response = requests.get(url, headers=self.headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp

    def execute_post_entry(self, url: str, request_dto: object) -> Response:
        resp: Response = requests.post(url, json=request_dto, headers=self.headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp

    def execute_put_entry(self, url: str, request_dto: object) -> Response:
        resp: Response = requests.put(url, json=request_dto, headers=self.headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp

    def execute_patch_entry(self, url: str, request_dto: object) -> Response:
        resp: Response = requests.patch(url, json=request_dto, headers=self.headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp

    def execute_delete_entry(self, url: str, request_dto: object = None) -> Response:
        resp: Response = requests.delete(url, json=request_dto, headers=self.headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp
