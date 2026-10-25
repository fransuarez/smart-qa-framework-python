"""
Placeholder HTTP client for the Fake Store API.
"""

import logging
import requests
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class APIClient:
    """Simple wrapper around requests.Session with JWT support."""
    def __init__(self, base_url: str, token_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.token_url = token_url
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.jwt_token: Optional[str] = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Obtain JWT token – replace with real auth call later."""
        # TODO: implement real auth request
        logger.debug("Authenticating %s", self.username)
        self.jwt_token = "FAKE_JWT_TOKEN"
        self.session.headers.update({"Authorization": f"Bearer {self.jwt_token}"})

    def _refresh_token(self) -> None:
        """Refresh JWT when expired (placeholder)."""
        logger.debug("Refreshing JWT token")
        self._authenticate()

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug("%s %s", method.upper(), url)
        response = self.session.request(method, url, **kwargs)
        if response.status_code == 401:
            self._refresh_token()
            response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    # Public helpers ---------------------------------------------------------
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        return self._request("get", endpoint, params=params).json()

    def post(self, endpoint: str, json: Optional[Dict] = None) -> Any:
        return self._request("post", endpoint, json=json).json()

    def put(self, endpoint: str, json: Optional[Dict] = None) -> Any:
        return self._request("put", endpoint, json=json).json()

    def delete(self, endpoint: str) -> Any:
        return self._request("delete", endpoint).json()