from typing import Optional

from pytenno.models.enums import OrderType, Platform, Subtype
from pytenno.models.items import ItemFull, ItemInOrder
from pytenno.models.orders import OrderCommon, OrderCreated, OrderRow
from pytenno.utils import _from_data

from .core import BackendAdapter


class ProfileBackend(BackendAdapter):
    async def _create_order(
        self,
        item_id: str,
        order_type: OrderType,
        platinum: int,
        quantity: int,
        visible: bool,
        subtype: Subtype,
        rank: Optional[int] = None,
    ):
        url = "/profile/orders"
        response = await self._backend._request(
            url,
            method="post",
            json={
                "item_id": item_id,
                "order_type": order_type.name,
                "platinum": platinum,
                "quantity": quantity,
                "visible": visible,
                "subtype": subtype.name,
                "rank": rank,
            },
        )
        order = response["payload"]["order"]
        return _from_data(OrderCreated, order)
