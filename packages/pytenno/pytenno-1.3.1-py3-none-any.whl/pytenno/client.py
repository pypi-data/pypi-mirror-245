"""The main module for the PyTenno client."""

from types import TracebackType
from typing import Optional, Type

import aiohttp

from ._backends.core import PyTennoBackend
from .constants import VALID_LANGUAGES
from .interface.auction_entries import AuctionEntries
from .interface.auctions import Auctions
from .interface.auth import Auth
from .interface.items import Items
from .interface.liches import Liches
from .interface.misc import Misc
from .interface.profile import Profile
from .interface.rivens import Rivens
from .models.enums import Platform


class PyTenno:
    """The primary class for interaction with the warframe.market API endpoints.
    This must be used in an asynchronous context manager.

    Parameters
    ----------
    default_language : str
        The default language used when communicating with the API.
        See ``VALID_LANGUAGES`` for valid values.
    default_platform : Platform
        The default platform used when communicating with the API.
    silenced_errors  : list[Exception]
        A list of errors that will be silenced when raised by the API.
        Instead of raising the error, the function will return None.

    Example
    -------
    >>> async with PyTenno() as tenno:
    >>>     current_user = await tenno.Auth.login(username="username", password="password")
    >>>     print(current_user.ingame_name)
    """

    def __init__(
        self,
        default_language: Optional[VALID_LANGUAGES] = "en",
        default_platform: Platform = Platform.pc,
        silenced_errors: list[Exception] = [],
    ) -> None:
        self._language = default_language
        """The default language used when communicating with the API."""
        self._platform = default_platform
        """The default platform used when communicating with the API."""

        self._session: aiohttp.ClientSession
        """The session used to communicate with the API."""
        self._silenced = silenced_errors
        """A list of errors that will be silenced when raised by the API."""

        self.auction_entries: AuctionEntries
        """The AuctionEntries interface."""
        self.auctions: Auctions
        """The Auctions interface."""
        self.auth: Auth
        """The Auth interface."""
        self.items: Items
        """The Items interface."""
        self.liches: Liches
        """The Liches interface."""
        self.misc: Misc
        """The Misc interface."""
        self.profile: Profile
        """The Profile interface."""
        self.rivens: Rivens
        """The Rivens interface."""

    async def __aenter__(self):
        headers = {
            "Authorization": "JWT",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "language": self._language,
            "platform": str(self._platform),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
        }
        self._session = aiohttp.ClientSession(headers=headers)
        backend = PyTennoBackend(self._session, self._silenced)

        self.auction_entries = AuctionEntries(backend)
        self.auctions = Auctions(backend)
        self.auth = Auth(backend)
        self.items = Items(backend)
        self.liches = Liches(backend)
        self.misc = Misc(backend)
        self.profile = Profile(backend)
        self.rivens = Rivens(backend)
        return self

    async def __aexit__(
        self,
        exctype: Optional[Type[BaseException]],
        excinst: Optional[BaseException],
        exctb: Optional[TracebackType],
    ) -> bool:
        await self._session.close()
        return False

    async def close(self) -> None:
        """Closes the client's ``aiohttp`` session."""
        await self._session.close()
