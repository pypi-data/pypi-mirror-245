from typing import Optional

from ..constants import VALID_LANGUAGES
from ..models.droptable import DropSource, DropTable
from ..models.items import ItemFull, ItemShort
from ..models.orders import OrderFull, OrderRow
from ..utils import format_name, _from_data
from .core import BackendAdapter


class ItemsBackend(BackendAdapter):
    async def _get_items(self, language: str):
        url = "/items"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)

        return [_from_data(ItemShort, node) for node in response["payload"]["items"]]

    async def _get_item(
        self,
        item_name: str,
        platform: str,
    ):
        url = f"/items/{format_name(item_name)}"
        headers = {"Platform": str(platform)}
        response = await self._backend._request(url, headers=headers)
        if response is None:
            return None
        items = response["payload"]["item"]["items_in_set"]

        return [_from_data(ItemFull, node) for node in items]

    async def _get_orders(
        self,
        item_name,
        include_items,
        platform,
    ):
        url = f"/items/{format_name(item_name)}/orders"
        headers = {"Platform": platform}

        if include_items:
            url += "?include=item"

        response = await self._backend._request(url, headers=headers)
        if include_items:
            return (
                [_from_data(OrderRow, node) for node in response["payload"]["orders"]],
                [
                    _from_data(ItemFull, node)
                    for node in response["include"]["item"]["items_in_set"]
                ],
            )
        return [_from_data(OrderRow, node) for node in response["payload"]["orders"]]

    async def _get_dropsources(
        self, item_name, include_items: bool, language: Optional[VALID_LANGUAGES]
    ):
        # url = f"/items/{format_name(item_name)}/droptables"
        url = f"/items/{format_name(item_name)}/dropsources"
        if include_items:
            url += "?include=item"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        if include_items:
            return (
                [DropSource._from_data(d) for d in response["payload"]["dropsources"]],
                [
                    ItemFull._from_data(item)
                    for item in response["include"]["item"]["items_in_set"]
                ],
            )
        return [DropSource._from_data(d) for d in response["payload"]["dropsources"]]
