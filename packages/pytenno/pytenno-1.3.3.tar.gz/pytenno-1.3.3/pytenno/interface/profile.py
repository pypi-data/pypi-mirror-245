"""Module holding the Profile interface class."""

from typing import Optional

from .._backends.profile import ProfileBackend
from ..models.enums import OrderType, Subtype
from ..models.orders import OrderCreated


class Profile(ProfileBackend):
    """Class for the profile backend."""

    async def create_order(
        self,
        item_id: str,
        order_type: OrderType,
        platinum: int,
        quantity: int,
        visible: bool,
        subtype: Subtype,
        rank: Optional[int] = None,
    ) -> OrderCreated:
        """Creates an order, and returns the order object.

        Parameters
        ----------
        item_id : str
            The ID of the item.
        order_type : OrderType
            The type of order.
        platinum : int
            The amount of platinum per item in the order.
        quantity : int
            How many items to offer to buy / sell.
        visible : bool
            Whether the order is visible to others.
        subtype : Subtype
            The subtype of the item. Must be applicable to the item passed.
        rank : Optional[int]
            The rank of the item. Unnecessary for anything which doesn't have a rank.

        Returns
        -------
        OrderCreated
            The order object.
        """
        return await self._create_order(
            item_id,
            order_type,
            platinum,
            quantity,
            visible,
            subtype,
            rank,
        )
