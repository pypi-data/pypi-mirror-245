"""Course Progress Authentication Library."""

import logging

from datetime import datetime

import aiohttp
import jwt

from .const import BASE_URL, ENDPOINT_MAP
from .exceptions import HttpException

_LOGGER = logging.getLogger(__name__)


class CourseProgressSession:
    """Authenticator and HTTP functions for Course Progress."""

    def __init__(self, instance_name) -> None:
        """Initialize an instance of Course Progress."""
        self._base_url = BASE_URL.format(INSTANCE_NAME=instance_name)
        self._refresh_token = ""
        self._access_token = ""
        self._expires_at: datetime = None

    @property
    def get_available_member_ids(self) -> list[int]:
        """Returns a list of valid member IDs from the access token."""
        return self._decode_jwt(self._access_token)["children"]

    def _decode_jwt(self, token: str):
        """Decode the JWT into a dict."""
        return jwt.decode(jwt=token, algorithms=["HS256"], options={"verify_signature": False})

    def _headers(self, refresh_token: bool = False) -> dict:
        """Build and return headers."""
        if refresh_token:
            return {
                "Authorization": f"Bearer {self._refresh_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def login(self, username, password):
        """Login to Course Progress."""
        response = await self.send_http_request(
            endpoint="login", refresh_token=True, body={"username": username, "password": password}
        )
        if response["status"] == 200:
            response = response["response"]
            self._access_token = response["token"]
            self._refresh_token = response["refreshToken"]
            decoded = self._decode_jwt(self._access_token)
            self._expires_at = datetime.fromtimestamp(decoded["exp"])

    async def _refresh_access_token(self):
        """Refresh the access token."""
        response = await self.send_http_request(endpoint="refresh", refresh_token=True)
        if response["status"] == 200:
            response = response["response"]
            self._access_token = response["token"]
            self._refresh_token = response["refreshToken"]
            decoded = self._decode_jwt(self._access_token)
            self._expires_at = datetime.fromtimestamp(decoded["exp"])

    async def send_http_request(self, endpoint: str, body: dict = None, refresh_token: bool = False, **kwargs):
        """Sends a HTTP request via aiohttp."""
        request_endpoint = ENDPOINT_MAP.get(endpoint, None)
        if request_endpoint is None:
            raise ValueError(f"Requested endpoint {endpoint} is missing from the endpoint map.")

        if self._expires_at is not None:
            if datetime.now() > self._expires_at and not refresh_token:
                _LOGGER.debug("Access token expired, refreshing.")
                await self._refresh_access_token()

        headers = self._headers(refresh_token)
        if endpoint.upper() == "LOGIN":
            headers = None

        _LOGGER.debug("Built URL %s", self._base_url + request_endpoint.get("endpoint").format(**kwargs))

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=request_endpoint.get("method", "GET"),
                url=self._base_url + request_endpoint.get("endpoint").format(**kwargs),
                headers=headers,
                json=body,
            ) as response:
                output = {"status": response.status, "response": {}}
                _LOGGER.debug("Got return code %s", response.status)
                if response.status >= 400:
                    raise HttpException(response.status, await response.text())
                if response.status == 204:
                    return output
                if response.status >= 200 or response.status < 204:
                    output["response"] = await response.json()
                    return output
                return output
