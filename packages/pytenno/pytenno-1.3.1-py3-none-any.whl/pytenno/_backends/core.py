from typing import Union

import aiohttp

from ..constants import API_ROOT
from ..utils import _raise_error_code


class PyTennoBackend:
    def __init__(
        self, session: aiohttp.ClientSession, silenced: list[Exception]
    ) -> None:
        self._session = session
        self.silenced = silenced

    async def _request(
        self, url: str, **kwargs
    ) -> dict[str, str | int | dict | list] | None:
        url = f"{API_ROOT}{url}"
        mode: Union[aiohttp.ClientSession.get, aiohttp.ClientSession.post] = getattr(
            self._session, kwargs.pop("method", "get")
        )

        kwargs.setdefault("headers", {})

        if kwargs["headers"].get("Language", None) is None:
            kwargs["headers"]["Language"] = self._session.headers["Language"]

        if kwargs["headers"].get("Platform", None) is None:
            kwargs["headers"]["Platform"] = self._session.headers["Platform"]

        response: aiohttp.ClientResponse = await mode(url, **kwargs)
        if response.status != 200:
            return _raise_error_code(response, self.silenced)

        return await response.json()


class BackendAdapter:
    def __init__(self, backend: PyTennoBackend) -> None:
        self._backend = backend
