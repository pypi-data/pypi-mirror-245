"""Module holding the Items interface class."""

from typing import Literal, Optional, overload

from .._backends.items import ItemsBackend
from ..constants import VALID_LANGUAGES
from ..models.droptable import DropSource, DropTable
from ..models.enums import Platform
from ..models.items import ItemFull, ItemShort
from ..models.orders import OrderRow


class Items(ItemsBackend):
    """Class for the items backend."""

    async def get_items(
        self, language: Optional[VALID_LANGUAGES] = None
    ) -> list[ItemShort]:
        """Gets all items.

        Parameters
        ----------
        language : Optional[VALID_LANGUAGES]
            The language of the items. Default: ``None``, meaning the default set during client construction.

        Returns
        -------
        list[ItemShort]

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     items = await pytenno.items.get_items()
        >>>     for item in items:
        >>>         print(item.url_name)
        """
        return await self._get_items(language)

    async def get_item(
        self,
        item_name: str,
        *,
        platform: Optional[Platform] = None,
    ) -> list[ItemFull]:
        """Gets the item with the given name, as well as related items (such as items of the same set).

        The item must be tradeable.

        Parameters
        ----------
        item_name : str
            The name of the item.
        platform : Platform
            The platform of the item. Default: ``None``, meaning the default set when the client was created.

        Returns
        -------
        list[ItemFull]

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     items = await pytenno.items.get_item("mirage prime set")
        >>>     for item in items:
        >>>         print(item.url_name)
        """
        return await self._get_item(item_name, platform)

    @overload
    async def get_orders(
        self,
        item_name: str,
        include_items: Literal[False],
        platform: Optional[Platform] = None,
    ) -> list[OrderRow]:
        ...

    @overload
    async def get_orders(
        self,
        item_name: str,
        include_items: Literal[True],
        platform: Optional[Platform] = None,
    ) -> tuple[list[OrderRow], list[ItemFull]]:
        ...

    async def get_orders(
        self,
        item_name: str,
        include_items: bool,
        platform: Optional[Platform] = None,
    ):
        """Gets the orders of the given item.

        Parameters
        ----------
        item_name : str
            The name of the item.
        include_items : bool
            Whether to include information about the item requested.
        platform : Platform
            The platform of the item. Default: ``None``, meaning the default set when the client was created.

        Returns
        -------
        list[OrderRow] | tuple(list[OrderRow], list[ItemFull])

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     orders, items = await pytenno.items.get_orders("mirage prime set", include_items=True)
        >>>     for order in orders:
        >>>         print(order.user.ingame_name)
        >>>     for item in items:
        >>>         print(item.url_name)
        """
        return await self._get_orders(item_name, include_items, str(platform))

    @overload
    async def get_dropsources(
        self,
        item_name: str,
        include_items: Literal[False],
        language: Optional[VALID_LANGUAGES] = None,
    ) -> list[DropSource]:
        ...

    @overload
    async def get_dropsources(
        self,
        item_name: str,
        include_items: Literal[True],
        language: Optional[VALID_LANGUAGES] = None,
    ) -> tuple[list[DropSource], list[ItemFull]]:
        ...

    async def get_dropsources(
        self,
        item_name: str,
        include_items: bool,
        language: Optional[VALID_LANGUAGES] = None,
    ):
        """Gets where an item can be found.

        Parameters
        ----------
        item_name : str
            The name of the item.
        include_items : bool
            Whether to include information about the item requested.
        language : Optional[VALID_LANGUAGES]
            The language of the droptable. Default: ``None``, meaning the default set during client construction.

        Returns
        -------
        list[DropSource] | tuple(list[DropSource], list[ItemFull])

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     droptable, items = await pytenno.items.get_droptable("frost prime neuroptics", include_items=True)
        >>>     print(droptable.relics, droptable.missions)
        >>>     for item in items:
        >>>         print(item.url_name)

        """
        return await self._get_dropsources(item_name, include_items, language)
