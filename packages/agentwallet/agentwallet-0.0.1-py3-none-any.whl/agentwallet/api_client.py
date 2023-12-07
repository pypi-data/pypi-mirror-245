import os
import requests
from urllib.parse import urljoin
from .exceptions import APIException, InvalidCredentialsException

AGENT_WALLET_BASE_URL = os.getenv(
    "AGENT_WALLET_BASE_URL", "https://testwallet.sidekik.ai"
)
REQUEST_TIMEOUT = 10  # seconds


class ApiClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def get(self, url: str) -> dict:
        response = requests.get(
            urljoin(AGENT_WALLET_BASE_URL, url),
            headers=self.headers,
            timeout=REQUEST_TIMEOUT,
        )
        return self._handle_response(response)

    def post(self, url: str, data: dict) -> dict:
        response = requests.post(
            urljoin(AGENT_WALLET_BASE_URL, url),
            headers=self.headers,
            json=data,
            timeout=REQUEST_TIMEOUT,
        )
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> dict:
        if response.ok:
            return response.json()
        else:
            self._handle_error(response)

    def _handle_error(self, response: requests.Response):
        if response.status_code == 401:
            raise InvalidCredentialsException()
        elif response.status_code == 400:
            data = response.json()
            if data.get("response") == "NOK" and "error" in data:
                raise APIException(error_info=data["error"])
        response.raise_for_status()  # Reraises the original HTTPError if not handled above
